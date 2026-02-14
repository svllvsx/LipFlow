import ctypes
import os
import shutil
import sys
import threading
import time
from ctypes import wintypes
from pathlib import Path

APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from main import create_app

CACHE_DIR = Path(__file__).resolve().parent / "data" / "cef_cache"
WM_CLOSE = 0x0010
WM_NCLBUTTONDOWN = 0x00A1
HTCAPTION = 2
SW_MINIMIZE = 6
SW_MAXIMIZE = 3
SW_RESTORE = 9
GWL_STYLE = -16
GWL_EXSTYLE = -20
WS_POPUP = 0x80000000
WS_CAPTION = 0x00C00000
WS_SYSMENU = 0x00080000
WS_THICKFRAME = 0x00040000
WS_MINIMIZEBOX = 0x00020000
WS_MAXIMIZEBOX = 0x00010000
WS_BORDER = 0x00800000
WS_DLGFRAME = 0x00400000
WS_EX_DLGMODALFRAME = 0x00000001
WS_EX_WINDOWEDGE = 0x00000100
WS_EX_CLIENTEDGE = 0x00000200
WS_EX_STATICEDGE = 0x00020000
SWP_NOSIZE = 0x0001
SWP_NOZORDER = 0x0004
SWP_FRAMECHANGED = 0x0020
MONITOR_DEFAULTTONEAREST = 0x00000002
DWMWA_WINDOW_CORNER_PREFERENCE = 33
DWMWCP_DONOTROUND = 1
DWMWA_NCRENDERING_POLICY = 2
DWMNCRP_DISABLED = 1
GA_ROOT = 2


class MONITORINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("rcMonitor", wintypes.RECT),
        ("rcWork", wintypes.RECT),
        ("dwFlags", wintypes.DWORD),
    ]


class WindowController:
    def __init__(self) -> None:
        self._handle = 0
        self._lock = threading.Lock()
        self._restore_rects = {}

    def attach(self, hwnd: int) -> None:
        with self._lock:
            self._handle = int(hwnd)

    def _hwnd(self) -> int:
        with self._lock:
            return self._handle

    def _resolve_hwnd(self, scope: str = "main") -> int:
        scope = (scope or "main").lower()
        if scope != "active":
            return self._hwnd()
        try:
            user32 = ctypes.windll.user32
            hwnd = int(user32.GetForegroundWindow())
            if not hwnd:
                return self._hwnd()
            root = int(user32.GetAncestor(hwnd, GA_ROOT))
            if root:
                hwnd = root
            pid = os.getpid()
            win_pid = wintypes.DWORD(0)
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(win_pid))
            if int(win_pid.value) != pid:
                return self._hwnd()
            return hwnd
        except Exception:
            return self._hwnd()

    @staticmethod
    def _apply_borderless_hwnd(hwnd: int) -> None:
        if not hwnd:
            return
        user32 = ctypes.windll.user32
        style = user32.GetWindowLongW(hwnd, GWL_STYLE)
        style = style & ~(
            WS_CAPTION
            | WS_SYSMENU
            | WS_THICKFRAME
            | WS_MINIMIZEBOX
            | WS_MAXIMIZEBOX
            | WS_BORDER
            | WS_DLGFRAME
        )
        style = style | WS_POPUP
        user32.SetWindowLongW(hwnd, GWL_STYLE, style)
        ex_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ex_style = ex_style & ~(
            WS_EX_DLGMODALFRAME
            | WS_EX_WINDOWEDGE
            | WS_EX_CLIENTEDGE
            | WS_EX_STATICEDGE
        )
        user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style)
        rect = wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        w = max(100, int(rect.right - rect.left))
        h = max(100, int(rect.bottom - rect.top))
        user32.SetWindowPos(hwnd, 0, int(rect.left), int(rect.top), w, h, SWP_NOZORDER | SWP_FRAMECHANGED)
        try:
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_WINDOW_CORNER_PREFERENCE,
                ctypes.byref(ctypes.c_int(DWMWCP_DONOTROUND)),
                ctypes.sizeof(ctypes.c_int),
            )
        except Exception:
            pass
        try:
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_NCRENDERING_POLICY,
                ctypes.byref(ctypes.c_int(DWMNCRP_DISABLED)),
                ctypes.sizeof(ctypes.c_int),
            )
        except Exception:
            pass

    def apply_borderless(self) -> None:
        hwnd = self._hwnd()
        if hwnd:
            self._apply_borderless_hwnd(hwnd)

    @staticmethod
    def _window_rect(hwnd: int):
        rect = wintypes.RECT()
        if not ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect)):
            return None
        return {
            "left": int(rect.left),
            "top": int(rect.top),
            "right": int(rect.right),
            "bottom": int(rect.bottom),
            "width": int(rect.right - rect.left),
            "height": int(rect.bottom - rect.top),
        }

    @staticmethod
    def _monitor_work_rect(hwnd: int):
        user32 = ctypes.windll.user32
        monitor = user32.MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST)
        if not monitor:
            return None
        mi = MONITORINFO()
        mi.cbSize = ctypes.sizeof(MONITORINFO)
        if not user32.GetMonitorInfoW(monitor, ctypes.byref(mi)):
            return None
        return {
            "left": int(mi.rcWork.left),
            "top": int(mi.rcWork.top),
            "right": int(mi.rcWork.right),
            "bottom": int(mi.rcWork.bottom),
            "width": int(mi.rcWork.right - mi.rcWork.left),
            "height": int(mi.rcWork.bottom - mi.rcWork.top),
        }

    def _toggle_maximize_to_work_area(self, hwnd: int) -> bool:
        user32 = ctypes.windll.user32
        if int(user32.IsIconic(hwnd)):
            user32.ShowWindow(hwnd, SW_RESTORE)
        with self._lock:
            restore = self._restore_rects.get(int(hwnd))
        if restore:
            user32.SetWindowPos(
                hwnd,
                0,
                int(restore["left"]),
                int(restore["top"]),
                max(100, int(restore["width"])),
                max(100, int(restore["height"])),
                SWP_NOZORDER | SWP_FRAMECHANGED,
            )
            with self._lock:
                self._restore_rects.pop(int(hwnd), None)
            return True

        now_rect = self._window_rect(hwnd)
        work_rect = self._monitor_work_rect(hwnd)
        if not now_rect or not work_rect:
            if user32.IsZoomed(hwnd):
                user32.ShowWindow(hwnd, SW_RESTORE)
            else:
                user32.ShowWindow(hwnd, SW_MAXIMIZE)
            return True

        with self._lock:
            self._restore_rects[int(hwnd)] = now_rect
        user32.SetWindowPos(
            hwnd,
            0,
            int(work_rect["left"]),
            int(work_rect["top"]),
            max(100, int(work_rect["width"])),
            max(100, int(work_rect["height"])),
            SWP_NOZORDER | SWP_FRAMECHANGED,
        )
        return True

    def apply_borderless_process_windows(self) -> None:
        pid = os.getpid()
        user32 = ctypes.windll.user32
        enum_cb_t = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

        def _enum_cb(hwnd: int, _lparam: int) -> bool:
            try:
                win_pid = wintypes.DWORD(0)
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(win_pid))
                if int(win_pid.value) != pid:
                    return True
                if not user32.IsWindowVisible(hwnd):
                    return True
                self._apply_borderless_hwnd(int(hwnd))
            except Exception:
                pass
            return True

        cb = enum_cb_t(_enum_cb)
        user32.EnumWindows(cb, 0)

    def action(self, action: str, scope: str = "main") -> bool:
        hwnd = self._resolve_hwnd(scope)
        if not hwnd:
            return False
        user32 = ctypes.windll.user32
        action = action.lower()
        if action == "minimize":
            user32.ShowWindow(hwnd, SW_MINIMIZE)
            return True
        if action == "maximize":
            return self._toggle_maximize_to_work_area(hwnd)
        if action == "close":
            user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)
            return True
        if action == "drag":
            user32.ReleaseCapture()
            user32.SendMessageW(hwnd, WM_NCLBUTTONDOWN, HTCAPTION, 0)
            return True
        return False

    def rect(self, scope: str = "main") -> dict:
        hwnd = self._resolve_hwnd(scope)
        if not hwnd:
            return {"ok": False}
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
        return {
            "ok": True,
            "left": int(rect.left),
            "top": int(rect.top),
            "right": int(rect.right),
            "bottom": int(rect.bottom),
            "width": int(rect.right - rect.left),
            "height": int(rect.bottom - rect.top),
        }

    def move_to(self, left: int, top: int, scope: str = "main") -> bool:
        hwnd = self._resolve_hwnd(scope)
        if not hwnd:
            return False
        ctypes.windll.user32.SetWindowPos(hwnd, 0, int(left), int(top), 0, 0, SWP_NOSIZE | SWP_NOZORDER)
        return True


WINDOW_CTRL = WindowController()


def run_server() -> None:
    app = create_app(
        window_action=WINDOW_CTRL.action,
        window_rect=WINDOW_CTRL.rect,
        window_move=WINDOW_CTRL.move_to,
    )
    app.run(host="127.0.0.1", port=8090, debug=False, threaded=True)


def run_with_cef() -> bool:
    try:
        from cefpython3 import cefpython as cef
    except Exception as exc:
        ctypes.windll.user32.MessageBoxW(
            0,
            f"CEF runtime is not available.\n\nError: {exc}",
            "LipFlow",
            0x10,
        )
        return False

    if CACHE_DIR.exists():
        shutil.rmtree(CACHE_DIR, ignore_errors=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    cef.Initialize(settings={"cache_path": str(CACHE_DIR)})
    stop_borderless = threading.Event()

    def _borderless_worker() -> None:
        while not stop_borderless.is_set():
            try:
                WINDOW_CTRL.apply_borderless_process_windows()
            except Exception:
                pass
            stop_borderless.wait(0.35)

    borderless_thread = threading.Thread(target=_borderless_worker, daemon=True)
    borderless_thread.start()

    try:
        browser = cef.CreateBrowserSync(url=f"http://127.0.0.1:8090/?v={int(time.time())}", window_title="LipFlow")
        hwnd = browser.GetOuterWindowHandle()
        WINDOW_CTRL.attach(hwnd)
        WINDOW_CTRL.apply_borderless()
        cef.PostDelayedTask(cef.TID_UI, 250, WINDOW_CTRL.apply_borderless)
        cef.MessageLoop()
    finally:
        stop_borderless.set()
        borderless_thread.join(timeout=1.0)
        cef.Shutdown()
        shutil.rmtree(CACHE_DIR, ignore_errors=True)
    return True


if __name__ == "__main__":
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    if not run_with_cef():
        sys.exit(1)
