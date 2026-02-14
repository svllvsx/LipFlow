import base64
import json
import os
import queue
import re
import shutil
import subprocess
import threading
import unicodedata
import uuid
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
DATA_DIR = BASE_DIR / "data"
WEB_DIR = BASE_DIR / "web"
VIDEOS_DIR = DATA_DIR / "videos"
AUDIOS_DIR = DATA_DIR / "audios"
OUTPUTS_DIR = DATA_DIR / "outputs"
JOBS_DIR = DATA_DIR / "jobs"
TEMP_DIR = DATA_DIR / "temp"
LOGS_DIR = BASE_DIR / "logs"
FFMPEG_BIN_DIR = BASE_DIR / "bin" / "ffmpeg"
FFMPEG_EXE = FFMPEG_BIN_DIR / "ffmpeg.exe"
FFPROBE_EXE = FFMPEG_BIN_DIR / "ffprobe.exe"

JOBS_FILE = JOBS_DIR / "jobs.json"
VIDEO_INDEX_FILE = DATA_DIR / "video_index.json"
SELECTIONS_FILE = DATA_DIR / "face_selections.json"
TIMELINES_FILE = DATA_DIR / "timelines.json"
TRACKS_FILE = DATA_DIR / "face_tracks.json"
SETTINGS_FILE = DATA_DIR / "runtime_settings.json"

ALLOWED_VIDEO_EXT = {
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".webm",
    ".m4v",
    ".ts",
    ".mts",
    ".m2ts",
    ".flv",
    ".wmv",
    ".mpeg",
    ".mpg",
    ".3gp",
    ".ogv",
}
ALLOWED_AUDIO_EXT = {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg"}

W2L_INFER_CMD = os.getenv("W2L_INFER_CMD", "").strip()
W2L_CMD_TIMEOUT_SEC = int(os.getenv("W2L_CMD_TIMEOUT_SEC", "3600"))
W2L_EXEC_MODE = os.getenv("W2L_EXEC_MODE", "local").strip().lower()
W2L_CHECKPOINT_PATH = os.getenv("W2L_CHECKPOINT_PATH", "").strip()
W2L_USE_BOX = os.getenv("W2L_USE_BOX", "0").strip()
W2L_FACE_DET_BATCH = os.getenv("W2L_FACE_DET_BATCH", "16").strip()
W2L_BATCH = os.getenv("W2L_BATCH", "64").strip()
W2L_PADS = os.getenv("W2L_PADS", "0 10 0 0").strip()
W2L_RESIZE_FACTOR = os.getenv("W2L_RESIZE_FACTOR", "1").strip()
W2L_NOSMOOTH = os.getenv("W2L_NOSMOOTH", "0").strip()
W2L_ENHANCE_SHARPEN = os.getenv("W2L_ENHANCE_SHARPEN", "0").strip()
W2L_ENHANCE_DENOISE = os.getenv("W2L_ENHANCE_DENOISE", "0").strip()
W2L_ENHANCE_COLOR_BOOST = os.getenv("W2L_ENHANCE_COLOR_BOOST", "0").strip()
W2L_ENHANCE_ULTRA = os.getenv("W2L_ENHANCE_ULTRA", "0").strip()
W2L_ENHANCE_EXTREME = os.getenv("W2L_ENHANCE_EXTREME", "0").strip()
W2L_ENHANCE_FACE_RESTORE = os.getenv("W2L_ENHANCE_FACE_RESTORE", "0").strip()
W2L_ENHANCE_TWO_PASS = os.getenv("W2L_ENHANCE_TWO_PASS", "0").strip()
W2L_ENHANCE_QUALITY_GATE = os.getenv("W2L_ENHANCE_QUALITY_GATE", "0").strip()
W2L_ENHANCE_TEMPORAL = os.getenv("W2L_ENHANCE_TEMPORAL", "0").strip()
W2L_ENHANCE_DEBLOCK = os.getenv("W2L_ENHANCE_DEBLOCK", "0").strip()
W2L_ENHANCE_MULTICANDIDATE = os.getenv("W2L_ENHANCE_MULTICANDIDATE", "0").strip()
W2L_ENHANCE_10BIT = os.getenv("W2L_ENHANCE_10BIT", "0").strip()
W2L_ENHANCE_ANTI_FLICKER = os.getenv("W2L_ENHANCE_ANTI_FLICKER", "0").strip()
W2L_ENHANCE_SCENE_CUT = os.getenv("W2L_ENHANCE_SCENE_CUT", "0").strip()


class JsonKeyValueStore:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._lock = threading.Lock()
        self._ensure_file()

    def _ensure_file(self) -> None:
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._db_path.exists():
            self._db_path.write_text("{}", encoding="utf-8")

    def _read(self) -> dict:
        try:
            return json.loads(self._db_path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _write(self, payload: dict) -> None:
        self._db_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def set(self, key: str, record: dict) -> dict:
        with self._lock:
            data = self._read()
            data[key] = record
            self._write(data)
            return record

    def patch(self, key: str, **updates):
        with self._lock:
            data = self._read()
            if key not in data:
                return None
            rec = data[key]
            rec.update(updates)
            rec["updated_at"] = _utc_now()
            data[key] = rec
            self._write(data)
            return rec

    def get(self, key: str):
        with self._lock:
            return self._read().get(key)

    def list_all(self):
        with self._lock:
            data = self._read()
        return list(data.values())

    def delete(self, key: str):
        with self._lock:
            data = self._read()
            rec = data.pop(key, None)
            self._write(data)
            return rec


class FaceProbeEngine:
    def __init__(self) -> None:
        self.mode = "unavailable"
        self._cv2 = None
        self._cascade = None
        self._init_backends()

    def _init_backends(self) -> None:
        try:
            import cv2  # type: ignore

            cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            cascade = cv2.CascadeClassifier(cascade_path)
            if cascade.empty():
                return
            self._cv2 = cv2
            self._cascade = cascade
            self.mode = "opencv_haar"
        except Exception:
            self.mode = "unavailable"

    def probe(self, video_path: Path, ratio: float):
        if self._cv2 is None or self._cascade is None:
            return False, "Face probe backend is unavailable. Install opencv-python.", None

        ratio = max(0.0, min(1.0, float(ratio)))
        cap = self._cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            return False, "Cannot open video for probing.", None
        try:
            frame_count = int(cap.get(self._cv2.CAP_PROP_FRAME_COUNT) or 0)
            if frame_count > 1:
                frame_idx = int(ratio * (frame_count - 1))
                cap.set(self._cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ok, frame = cap.read()
            if not ok or frame is None:
                return False, "Cannot read frame from video.", None

            frame_h, frame_w = frame.shape[:2]
            gray = self._cv2.cvtColor(frame, self._cv2.COLOR_BGR2GRAY)
            detections = self._cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(40, 40),
            )
            faces = []
            for idx, det in enumerate(detections):
                x, y, w, h = [int(v) for v in det]
                faces.append(
                    {
                        "face_id": f"f{idx}",
                        "bbox": {"x": x, "y": y, "w": w, "h": h},
                        "score": 0.5,
                    }
                )

            ok_jpg, enc = self._cv2.imencode(".jpg", frame)
            if not ok_jpg:
                return False, "JPEG encoding failed.", None
            frame_b64 = base64.b64encode(enc.tobytes()).decode("ascii")
            payload = {
                "frame_ratio": ratio,
                "frame_size": {"width": frame_w, "height": frame_h},
                "faces": faces,
                "frame_jpeg_b64": frame_b64,
                "detector_mode": self.mode,
            }
            return True, "", payload
        finally:
            cap.release()


class FaceTrackerEngine:
    def __init__(self, probe_engine: FaceProbeEngine) -> None:
        self.mode = probe_engine.mode
        self._cv2 = probe_engine._cv2
        self._cascade = probe_engine._cascade

    def build_track(self, video_path: Path, seed_bbox: dict, seed_ratio: float, sample_step: int):
        if self._cv2 is None or self._cascade is None:
            return False, "Tracking backend is unavailable. Install opencv-python.", None

        sample_step = max(1, min(30, int(sample_step)))
        cap = self._cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            return False, "Cannot open video for tracking.", None

        try:
            fps = float(cap.get(self._cv2.CAP_PROP_FPS) or 25.0)
            frame_count = int(cap.get(self._cv2.CAP_PROP_FRAME_COUNT) or 0)
            if frame_count <= 0:
                return False, "Video has no frames.", None

            current_bbox = {
                "x": int(seed_bbox.get("x", 0)),
                "y": int(seed_bbox.get("y", 0)),
                "w": int(seed_bbox.get("w", 0)),
                "h": int(seed_bbox.get("h", 0)),
            }
            seed_center = _bbox_center(current_bbox)
            total_samples = 0
            matched_samples = 0
            points = []
            miss_streak = 0
            max_gap = 8

            start_frame = int(max(0.0, min(1.0, float(seed_ratio))) * max(0, frame_count - 1))
            for frame_idx in range(start_frame, frame_count, sample_step):
                cap.set(self._cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ok, frame = cap.read()
                if not ok or frame is None:
                    continue

                total_samples += 1
                gray = self._cv2.cvtColor(frame, self._cv2.COLOR_BGR2GRAY)
                detections = self._cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(40, 40),
                )
                boxes = []
                for det in detections:
                    x, y, w, h = [int(v) for v in det]
                    boxes.append({"x": x, "y": y, "w": w, "h": h})

                chosen = _choose_face_box(boxes, current_bbox, seed_center)
                if chosen is not None:
                    current_bbox = chosen
                    miss_streak = 0
                    matched_samples += 1
                    points.append(
                        {
                            "frame_idx": int(frame_idx),
                            "time_sec": float(frame_idx / max(1e-6, fps)),
                            "bbox": current_bbox,
                            "confidence": 1.0,
                            "interpolated": False,
                        }
                    )
                else:
                    miss_streak += 1
                    if current_bbox is not None and miss_streak <= max_gap:
                        points.append(
                            {
                                "frame_idx": int(frame_idx),
                                "time_sec": float(frame_idx / max(1e-6, fps)),
                                "bbox": current_bbox,
                                "confidence": 0.0,
                                "interpolated": True,
                            }
                        )
                    elif miss_streak > max_gap:
                        current_bbox = None

            payload = {
                "mode": self.mode,
                "sample_step": sample_step,
                "fps": fps,
                "frame_count": frame_count,
                "start_frame": start_frame,
                "total_samples": total_samples,
                "matched_samples": matched_samples,
                "coverage": float(matched_samples / total_samples) if total_samples > 0 else 0.0,
                "points": points,
            }
            return True, "", payload
        finally:
            cap.release()


class JobRunner:
    def __init__(self, job_store: JsonKeyValueStore, get_runtime_settings) -> None:
        self._store = job_store
        self._get_runtime_settings = get_runtime_settings
        self._queue = queue.Queue()
        self._worker = threading.Thread(target=self._loop, daemon=True)
        self._worker.start()

    def enqueue(self, job_id: str) -> None:
        self._queue.put(job_id)

    def queue_size(self) -> int:
        return self._queue.qsize()

    def _loop(self) -> None:
        while True:
            job_id = self._queue.get()
            try:
                self._run_job(job_id)
            except Exception as exc:
                self._store.patch(job_id, status="failed", progress=100, message=f"Unhandled worker error: {exc}")
            finally:
                self._queue.task_done()

    def _run_job(self, job_id: str) -> None:
        job = self._store.get(job_id)
        if not job:
            return
        if str(job.get("status", "")).lower() != "queued":
            return

        video_path = VIDEOS_DIR / job["video_file"]
        audio_path = AUDIOS_DIR / job["audio_file"]
        output_path = OUTPUTS_DIR / job["output_file"]
        job_temp_dir = TEMP_DIR / f"job_{job_id}"
        job_temp_dir.mkdir(parents=True, exist_ok=True)

        target_json_path = job_temp_dir / "target_face.json"
        timeline_json_path = job_temp_dir / "timeline.json"
        track_json_path = job_temp_dir / "target_track.json"
        target_json_path.write_text(json.dumps(job.get("target_face") or {}, ensure_ascii=False, indent=2), encoding="utf-8")
        timeline_json_path.write_text(
            json.dumps(job.get("timeline") or {"segments": []}, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        track_json_path.write_text(
            json.dumps(job.get("tracking") or {"points": []}, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        settings = self._get_runtime_settings()
        infer_command = str(settings.get("infer_command", "") or "")
        timeout_sec = int(settings.get("timeout_sec", W2L_CMD_TIMEOUT_SEC) or W2L_CMD_TIMEOUT_SEC)
        runtime_env = {
            "W2L_CHECKPOINT_PATH": str(settings.get("checkpoint_path", "") or ""),
            "W2L_USE_BOX": "1" if _to_bool_flag(settings.get("use_box", False), default=False) else "0",
            "W2L_FACE_DET_BATCH": str(settings.get("face_det_batch", 16) or 16),
            "W2L_BATCH": str(settings.get("wav2lip_batch", 64) or 64),
            "W2L_PADS": str(settings.get("pads", "0 10 0 0") or "0 10 0 0"),
            "W2L_RESIZE_FACTOR": str(settings.get("resize_factor", 1) or 1),
            "W2L_NOSMOOTH": "1" if _to_bool_flag(settings.get("nosmooth", False), default=False) else "0",
            "W2L_ENHANCE_SHARPEN": "1" if _to_bool_flag(settings.get("enhance_sharpen", False), default=False) else "0",
            "W2L_ENHANCE_DENOISE": "1" if _to_bool_flag(settings.get("enhance_denoise", False), default=False) else "0",
            "W2L_ENHANCE_COLOR_BOOST": "1" if _to_bool_flag(settings.get("enhance_color_boost", False), default=False) else "0",
            "W2L_ENHANCE_ULTRA": "1" if _to_bool_flag(settings.get("enhance_ultra", False), default=False) else "0",
            "W2L_ENHANCE_EXTREME": "1" if _to_bool_flag(settings.get("enhance_extreme", False), default=False) else "0",
            "W2L_ENHANCE_FACE_RESTORE": "1"
            if _to_bool_flag(settings.get("enhance_face_restore", False), default=False)
            else "0",
            "W2L_ENHANCE_TWO_PASS": "1" if _to_bool_flag(settings.get("enhance_two_pass", False), default=False) else "0",
            "W2L_ENHANCE_QUALITY_GATE": "1"
            if _to_bool_flag(settings.get("enhance_quality_gate", False), default=False)
            else "0",
            "W2L_ENHANCE_TEMPORAL": "1" if _to_bool_flag(settings.get("enhance_temporal", False), default=False) else "0",
            "W2L_ENHANCE_DEBLOCK": "1" if _to_bool_flag(settings.get("enhance_deblock", False), default=False) else "0",
            "W2L_ENHANCE_MULTICANDIDATE": "1"
            if _to_bool_flag(settings.get("enhance_multicandidate", False), default=False)
            else "0",
            "W2L_ENHANCE_10BIT": "1" if _to_bool_flag(settings.get("enhance_10bit", False), default=False) else "0",
            "W2L_ENHANCE_ANTI_FLICKER": "1"
            if _to_bool_flag(settings.get("enhance_anti_flicker", False), default=False)
            else "0",
            "W2L_ENHANCE_SCENE_CUT": "1"
            if _to_bool_flag(settings.get("enhance_scene_cut", False), default=False)
            else "0",
        }

        self._store.patch(job_id, status="running", started_at=_utc_now(), progress=15, message="Preparing assets...")

        if infer_command:
            self._store.patch(job_id, status="running", progress=35, message="Running Wav2Lip command...")
            ok, message = self._run_command(
                infer_command=infer_command,
                timeout_sec=timeout_sec,
                video_path=video_path,
                audio_path=audio_path,
                output_path=output_path,
                target_json_path=target_json_path,
                timeline_json_path=timeline_json_path,
                track_json_path=track_json_path,
                runtime_env=runtime_env,
            )
            if ok:
                post_msg = self._postprocess_output(output_path=output_path, settings=settings)
                self._store.patch(
                    job_id,
                    status="done",
                    finished_at=_utc_now(),
                    progress=100,
                    output_url=f"/outputs/{job['output_file']}",
                    message=f"{message} {post_msg}".strip(),
                )
            else:
                self._store.patch(job_id, status="failed", finished_at=_utc_now(), progress=100, message=message)
            return

        shutil.copy2(video_path, output_path)
        post_msg = self._postprocess_output(output_path=output_path, settings=settings)
        self._store.patch(
            job_id,
            status="done",
            finished_at=_utc_now(),
            progress=100,
            output_url=f"/outputs/{job['output_file']}",
            message=f"Stub mode: output is a copy of input video. Configure W2L_INFER_CMD for real inference. {post_msg}".strip(),
        )

    @staticmethod
    def _postprocess_output(output_path: Path, settings: dict) -> str:
        enhance_sharpen = _to_bool_flag(settings.get("enhance_sharpen", False), default=False)
        enhance_denoise = _to_bool_flag(settings.get("enhance_denoise", False), default=False)
        enhance_color_boost = _to_bool_flag(settings.get("enhance_color_boost", False), default=False)
        enhance_ultra = _to_bool_flag(settings.get("enhance_ultra", False), default=False)
        enhance_extreme = _to_bool_flag(settings.get("enhance_extreme", False), default=False)
        enhance_face_restore = _to_bool_flag(settings.get("enhance_face_restore", False), default=False)
        enhance_two_pass = _to_bool_flag(settings.get("enhance_two_pass", False), default=False)
        enhance_quality_gate = _to_bool_flag(settings.get("enhance_quality_gate", False), default=False)
        enhance_temporal = _to_bool_flag(settings.get("enhance_temporal", False), default=False)
        enhance_deblock = _to_bool_flag(settings.get("enhance_deblock", False), default=False)
        enhance_multicandidate = _to_bool_flag(settings.get("enhance_multicandidate", False), default=False)
        enhance_10bit = _to_bool_flag(settings.get("enhance_10bit", False), default=False)
        enhance_anti_flicker = _to_bool_flag(settings.get("enhance_anti_flicker", False), default=False)
        enhance_scene_cut = _to_bool_flag(settings.get("enhance_scene_cut", False), default=False)
        if not (
            enhance_sharpen
            or enhance_denoise
            or enhance_color_boost
            or enhance_ultra
            or enhance_extreme
            or enhance_face_restore
            or enhance_two_pass
            or enhance_quality_gate
            or enhance_temporal
            or enhance_deblock
            or enhance_multicandidate
            or enhance_10bit
            or enhance_anti_flicker
            or enhance_scene_cut
        ):
            return ""

        def _video_bitrate_kbps(path: Path):
            cmd_probe = [
                _resolve_ffprobe_bin(),
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=bit_rate",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ]
            try:
                proc_probe = subprocess.run(cmd_probe, capture_output=True, text=True, timeout=30)
                if proc_probe.returncode != 0:
                    return None
                raw = (proc_probe.stdout or "").strip().splitlines()
                if not raw:
                    return None
                return max(1, int(raw[0]) // 1000)
            except Exception:
                return None

        def _video_duration_sec(path: Path):
            cmd_probe = [
                _resolve_ffprobe_bin(),
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ]
            try:
                proc_probe = subprocess.run(cmd_probe, capture_output=True, text=True, timeout=30)
                if proc_probe.returncode != 0:
                    return None
                raw = (proc_probe.stdout or "").strip().splitlines()
                if not raw:
                    return None
                dur = float(raw[0])
                if dur <= 0:
                    return None
                return dur
            except Exception:
                return None

        def _scene_cut_count(path: Path):
            cmd_probe = [
                _resolve_ffmpeg_bin(),
                "-v",
                "info",
                "-i",
                str(path),
                "-vf",
                "select='gt(scene,0.30)',showinfo",
                "-an",
                "-f",
                "null",
                "-",
            ]
            try:
                proc_probe = subprocess.run(cmd_probe, capture_output=True, text=True, timeout=180)
                log = f"{proc_probe.stderr or ''}\n{proc_probe.stdout or ''}"
                pts = re.findall(r"pts_time:([0-9]+(?:\\.[0-9]+)?)", log)
                if not pts:
                    return 0
                return len(pts)
            except Exception:
                return None

        def _run_ffmpeg_stage(input_path: Path, vf_chain: str, preset: str, crf: str, tag: str, pix_fmt: str = "yuv420p"):
            temp_path = output_path.with_name(f"{output_path.stem}_{tag}{output_path.suffix}")
            cmd_stage = [
                _resolve_ffmpeg_bin(),
                "-y",
                "-i",
                str(input_path),
            ]
            if vf_chain:
                cmd_stage += ["-vf", vf_chain]
            cmd_stage += [
                "-c:v",
                "libx264",
                "-pix_fmt",
                pix_fmt,
                "-preset",
                preset,
                "-crf",
                crf,
            ]
            if enhance_ultra or enhance_extreme:
                cmd_stage += ["-tune", "film"]
            cmd_stage += ["-c:a", "copy", str(temp_path)]
            try:
                proc_stage = subprocess.run(cmd_stage, capture_output=True, text=True, timeout=2400)
            except Exception as exc:
                return False, f"{tag}: {exc}", input_path
            if proc_stage.returncode != 0 or not temp_path.exists():
                err = (proc_stage.stderr or "").strip()
                try:
                    if temp_path.exists():
                        temp_path.unlink()
                except Exception:
                    pass
                return False, f"{tag}: {(err[-220:] if err else 'ffmpeg failed')}", input_path
            return True, "", temp_path

        source_kbps = _video_bitrate_kbps(output_path) if (enhance_quality_gate or enhance_multicandidate) else None
        stage_pix_fmt = "yuv420p10le" if enhance_10bit else "yuv420p"
        scene_note = ""
        anti_flicker_effective = bool(enhance_anti_flicker)
        if enhance_scene_cut and enhance_anti_flicker:
            cut_count = _scene_cut_count(output_path)
            duration_sec = _video_duration_sec(output_path)
            if cut_count is None:
                scene_note = ",scene_guard_probe_fail"
            else:
                cuts_per_min = None
                if duration_sec and duration_sec > 0:
                    cuts_per_min = float(cut_count) / max(0.1, duration_sec / 60.0)
                if cuts_per_min is not None and cuts_per_min >= 6.0:
                    anti_flicker_effective = False
                    scene_note = f",scene_guard_off({cut_count}@{cuts_per_min:.1f}/min)"
                elif cuts_per_min is not None:
                    scene_note = f",scene_guard_on({cut_count}@{cuts_per_min:.1f}/min)"
                elif cut_count >= 8:
                    anti_flicker_effective = False
                    scene_note = f",scene_guard_off({cut_count})"
                else:
                    scene_note = f",scene_guard_on({cut_count})"
        vf = []
        if enhance_denoise:
            vf.append("hqdn3d=1.2:1.2:6:6")
        if enhance_sharpen:
            vf.append("unsharp=5:5:0.55:5:5:0.0")
        if enhance_deblock:
            vf.append("deblock=filter=strong:block=4")
        if enhance_color_boost:
            vf.append("eq=contrast=1.03:saturation=1.05:brightness=0.005")
        if enhance_ultra:
            vf.append("deband=1thr=0.03:2thr=0.03:3thr=0.03:4thr=0.03")
            vf.append("unsharp=7:7:0.9:7:7:0.0")
            vf.append("scale=iw*1.2:ih*1.2:flags=lanczos,scale=iw/1.2:ih/1.2:flags=lanczos")
        if enhance_extreme:
            vf.append("nlmeans=s=1.2:p=7:r=13")
            vf.append("gradfun=0.8:8")
        if enhance_face_restore:
            vf.append("cas=0.75")
            vf.append("unsharp=7:7:0.95:7:7:0.0")
        if enhance_temporal:
            vf.append("atadenoise=0a=0.02:0b=0.04:1a=0.02:1b=0.04")
        if anti_flicker_effective:
            vf.append("tmix=frames=3:weights='1 2 1'")

        current_path = output_path
        if vf:
            ok1, err1, path1 = _run_ffmpeg_stage(
                input_path=current_path,
                vf_chain=",".join(vf),
                preset="placebo" if enhance_extreme else ("veryslow" if enhance_ultra else "slow"),
                crf="12" if enhance_extreme else ("14" if enhance_ultra else "16"),
                tag="enh1",
                pix_fmt=stage_pix_fmt,
            )
            if not ok1:
                return f"[enhance failed: {err1}]"
            current_path = path1

        if enhance_two_pass:
            second_vf = []
            if enhance_temporal:
                second_vf.append("atadenoise=0a=0.015:0b=0.03:1a=0.015:1b=0.03")
            if anti_flicker_effective:
                second_vf.append("tmix=frames=3:weights='1 3 1'")
            second_vf.append("unsharp=5:5:0.45:5:5:0.0")
            if enhance_color_boost:
                second_vf.append("eq=contrast=1.02:saturation=1.03:brightness=0.002")
            if enhance_deblock:
                second_vf.append("deblock=filter=weak:block=4")
            ok2, err2, path2 = _run_ffmpeg_stage(
                input_path=current_path,
                vf_chain=",".join(second_vf),
                preset="placebo" if enhance_extreme else "veryslow",
                crf="11" if enhance_extreme else ("13" if enhance_ultra else "15"),
                tag="enh2",
                pix_fmt=stage_pix_fmt,
            )
            if not ok2:
                return f"[enhance failed: {err2}]"
            try:
                if current_path != output_path and current_path.exists():
                    current_path.unlink()
            except Exception:
                pass
            current_path = path2

        qg_note = ""
        if enhance_quality_gate and source_kbps:
            out_kbps = _video_bitrate_kbps(current_path)
            if out_kbps and out_kbps < int(source_kbps * 0.9):
                ok3, err3, path3 = _run_ffmpeg_stage(
                    input_path=current_path,
                    vf_chain="",
                    preset="placebo" if enhance_extreme else "veryslow",
                    crf="10" if enhance_extreme else ("12" if enhance_ultra else "14"),
                    tag="enhqg",
                    pix_fmt=stage_pix_fmt,
                )
                if ok3:
                    try:
                        if current_path != output_path and current_path.exists():
                            current_path.unlink()
                    except Exception:
                        pass
                    current_path = path3
                    qg_note = ",qgate"
                else:
                    qg_note = f",qgate_fail({err3})"

        mc_note = ""
        if enhance_multicandidate:
            base_crf = "11" if enhance_extreme else ("13" if enhance_ultra else "15")
            ok_a, err_a, path_a = _run_ffmpeg_stage(
                input_path=current_path,
                vf_chain="",
                preset="placebo" if enhance_extreme else "veryslow",
                crf=base_crf,
                tag="enhmc_a",
                pix_fmt=stage_pix_fmt,
            )
            ok_b, err_b, path_b = _run_ffmpeg_stage(
                input_path=current_path,
                vf_chain="unsharp=3:3:0.25:3:3:0.0",
                preset="placebo" if enhance_extreme else "veryslow",
                crf="10" if enhance_extreme else ("12" if enhance_ultra else "14"),
                tag="enhmc_b",
                pix_fmt=stage_pix_fmt,
            )
            if ok_a or ok_b:
                candidates = []
                if ok_a:
                    candidates.append(("a", path_a))
                if ok_b:
                    candidates.append(("b", path_b))
                best_name = ""
                best_path = None
                best_score = -1
                for name, cpath in candidates:
                    score = _video_bitrate_kbps(cpath)
                    if score is None:
                        try:
                            score = max(1, int(cpath.stat().st_size // 1024))
                        except Exception:
                            score = 1
                    if score > best_score:
                        best_score = score
                        best_name = name
                        best_path = cpath
                for name, cpath in candidates:
                    if best_path is None or cpath == best_path:
                        continue
                    try:
                        if cpath.exists():
                            cpath.unlink()
                    except Exception:
                        pass
                try:
                    if current_path != output_path and current_path.exists():
                        current_path.unlink()
                except Exception:
                    pass
                if best_path is not None:
                    current_path = best_path
                    mc_note = f",mc_{best_name}"
            else:
                mc_note = f",mc_fail({err_a or err_b})"

        if enhance_10bit:
            ok10, err10, path10 = _run_ffmpeg_stage(
                input_path=current_path,
                vf_chain="",
                preset="placebo" if enhance_extreme else "veryslow",
                crf="10" if enhance_extreme else ("12" if enhance_ultra else "14"),
                tag="enh10out",
                pix_fmt="yuv420p",
            )
            if ok10:
                try:
                    if current_path != output_path and current_path.exists():
                        current_path.unlink()
                except Exception:
                    pass
                current_path = path10
            else:
                return f"[enhance failed: {err10}]"
        try:
            if current_path != output_path:
                current_path.replace(output_path)
            enabled = []
            if enhance_sharpen:
                enabled.append("sharpen")
            if enhance_denoise:
                enabled.append("denoise")
            if enhance_color_boost:
                enabled.append("color")
            if enhance_ultra:
                enabled.append("ultra")
            if enhance_extreme:
                enabled.append("extreme")
            if enhance_face_restore:
                enabled.append("face_restore")
            if enhance_two_pass:
                enabled.append("two_pass")
            if enhance_temporal:
                enabled.append("temporal")
            if enhance_quality_gate:
                enabled.append("quality_gate")
            if enhance_deblock:
                enabled.append("deblock")
            if enhance_multicandidate:
                enabled.append("multicandidate")
            if enhance_10bit:
                enabled.append("10bit")
            if anti_flicker_effective:
                enabled.append("anti_flicker")
            if enhance_anti_flicker and not anti_flicker_effective:
                enabled.append("anti_flicker_guarded_off")
            if enhance_scene_cut:
                enabled.append("scene_cut_guard")
            suffix = f"{qg_note}{mc_note}{scene_note}"
            return f"[enhance: {','.join(enabled)}{suffix}]"
        except Exception as exc:
            return f"[enhance finalize failed: {exc}]"

    @staticmethod
    def _run_command(
        infer_command: str,
        timeout_sec: int,
        video_path: Path,
        audio_path: Path,
        output_path: Path,
        target_json_path: Path,
        timeline_json_path: Path,
        track_json_path: Path,
        runtime_env: dict,
    ):
        values = {
            "video": str(video_path.resolve()),
            "audio": str(audio_path.resolve()),
            "output": str(output_path.resolve()),
            "project": str(PROJECT_DIR.resolve()),
            "app": str(BASE_DIR.resolve()),
            "target_json": str(target_json_path.resolve()),
            "timeline_json": str(timeline_json_path.resolve()),
            "track_json": str(track_json_path.resolve()),
        }
        command = infer_command.format_map(_DefaultFormatMap(values))
        env = os.environ.copy()
        for k, v in (runtime_env or {}).items():
            if v is not None and str(v).strip() != "":
                env[str(k)] = str(v)
        try:
            completed = subprocess.run(
                command,
                cwd=str(PROJECT_DIR),
                shell=True,
                capture_output=True,
                text=True,
                timeout=max(10, int(timeout_sec)),
                env=env,
            )
        except subprocess.TimeoutExpired:
            return False, f"Command timeout after {timeout_sec} sec."
        except Exception as exc:
            return False, f"Command error: {exc}"

        stdout_tail = (completed.stdout or "").strip()[-700:]
        stderr_tail = (completed.stderr or "").strip()[-700:]
        if completed.returncode != 0:
            return False, f"Command failed (code {completed.returncode}). stderr: {stderr_tail or '-'}"
        if not output_path.exists():
            return False, f"Command finished but output file not found: {output_path.name}"
        return True, f"Inference completed. stdout: {stdout_tail or '-'}"


class _DefaultFormatMap(dict):
    def __missing__(self, key):
        return "{" + key + "}"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _is_allowed(ext: str, allowed: set) -> bool:
    return ext.lower() in allowed


def _prepare_dirs() -> None:
    for p in [VIDEOS_DIR, AUDIOS_DIR, OUTPUTS_DIR, JOBS_DIR, TEMP_DIR, DATA_DIR / "cef_cache", LOGS_DIR]:
        p.mkdir(parents=True, exist_ok=True)


def _clear_dir_contents(dir_path: Path) -> None:
    if not dir_path.exists():
        return
    for entry in dir_path.iterdir():
        try:
            if entry.is_dir():
                shutil.rmtree(entry, ignore_errors=True)
            else:
                entry.unlink()
        except Exception:
            pass


def _startup_cleanup_artifacts() -> None:
    _clear_dir_contents(VIDEOS_DIR)
    _clear_dir_contents(AUDIOS_DIR)
    _clear_dir_contents(OUTPUTS_DIR)
    _clear_dir_contents(TEMP_DIR)

    for json_file in [JOBS_FILE, VIDEO_INDEX_FILE, SELECTIONS_FILE, TIMELINES_FILE, TRACKS_FILE]:
        try:
            json_file.parent.mkdir(parents=True, exist_ok=True)
            json_file.write_text("{}", encoding="utf-8")
        except Exception:
            pass


def _make_video_id() -> str:
    return "v" + uuid.uuid4().hex[:12]


def _safe_upload_filename(raw_name: str, fallback_stem: str = "upload") -> str:
    # Keep unicode symbols (including Cyrillic), but sanitize invalid Windows filename chars.
    name = str(raw_name or "").replace("\\", "/").split("/")[-1]
    name = unicodedata.normalize("NFC", name).strip().strip(". ")
    name = re.sub(r'[\x00-\x1f<>:"/\\|?*]+', "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    if not name:
        return fallback_stem

    parsed = Path(name)
    stem = parsed.stem.strip().strip(". ")
    suffix = parsed.suffix.strip()
    suffix = re.sub(r'[\x00-\x1f<>:"/\\|?*]+', "", suffix)
    if not stem:
        stem = fallback_stem

    safe_name = f"{stem}{suffix}" if suffix else stem
    return safe_name[:180]


def _to_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return float(default)


def _bbox_center(b: dict):
    return (float(b["x"]) + float(b["w"]) * 0.5, float(b["y"]) + float(b["h"]) * 0.5)


def _center_distance(a, b):
    dx = float(a[0]) - float(b[0])
    dy = float(a[1]) - float(b[1])
    return (dx * dx + dy * dy) ** 0.5


def _bbox_iou(a: dict, b: dict):
    ax1, ay1 = float(a["x"]), float(a["y"])
    ax2, ay2 = ax1 + float(a["w"]), ay1 + float(a["h"])
    bx1, by1 = float(b["x"]), float(b["y"])
    bx2, by2 = bx1 + float(b["w"]), by1 + float(b["h"])
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0.0, ix2 - ix1), max(0.0, iy2 - iy1)
    inter = iw * ih
    union = (ax2 - ax1) * (ay2 - ay1) + (bx2 - bx1) * (by2 - by1) - inter
    if union <= 0:
        return 0.0
    return inter / union


def _read_video_meta(video_path: Path, cv2_mod=None):
    meta = {
        "fps": None,
        "frame_count": None,
        "duration_sec": None,
        "width": None,
        "height": None,
    }

    cv2 = cv2_mod
    if cv2 is None:
        try:
            import cv2  # type: ignore
        except Exception:
            return _read_video_meta_ffprobe(video_path, fallback=meta)

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return _read_video_meta_ffprobe(video_path, fallback=meta)
    try:
        fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
        if width <= 0 or height <= 0:
            ok, frame = cap.read()
            if ok and frame is not None:
                height, width = frame.shape[:2]
        duration_sec = float(frame_count / fps) if fps > 0.0 and frame_count > 0 else None

        meta["fps"] = fps if fps > 0 else None
        meta["frame_count"] = frame_count if frame_count > 0 else None
        meta["duration_sec"] = duration_sec
        meta["width"] = width if width > 0 else None
        meta["height"] = height if height > 0 else None
        if not (meta["width"] and meta["height"]):
            return _read_video_meta_ffprobe(video_path, fallback=meta)
        return meta
    finally:
        cap.release()


def _read_video_meta_ffprobe(video_path: Path, fallback: dict = None):
    meta = dict(fallback or {})
    cmd_probe = [
        _resolve_ffprobe_bin(),
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height,r_frame_rate,nb_frames:format=duration",
        "-of",
        "json",
        str(video_path),
    ]
    try:
        proc = subprocess.run(cmd_probe, capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            return meta
        payload = json.loads(proc.stdout or "{}")
        stream = (payload.get("streams") or [{}])[0]
        fmt = payload.get("format") or {}
        width = int(stream.get("width") or 0)
        height = int(stream.get("height") or 0)
        fps = _parse_ffprobe_fps(stream.get("r_frame_rate"))
        frame_count = int(stream.get("nb_frames") or 0)
        duration = _to_float(fmt.get("duration"), default=0.0)
        if duration <= 0 and fps > 0 and frame_count > 0:
            duration = float(frame_count / fps)
        meta["fps"] = fps if fps > 0 else meta.get("fps")
        meta["frame_count"] = frame_count if frame_count > 0 else meta.get("frame_count")
        meta["duration_sec"] = duration if duration > 0 else meta.get("duration_sec")
        meta["width"] = width if width > 0 else meta.get("width")
        meta["height"] = height if height > 0 else meta.get("height")
        return meta
    except Exception:
        return meta


def _parse_ffprobe_fps(raw):
    txt = str(raw or "").strip()
    if not txt:
        return 0.0
    if "/" in txt:
        try:
            a, b = txt.split("/", 1)
            num = float(a)
            den = float(b)
            if den == 0:
                return 0.0
            return float(num / den)
        except Exception:
            return 0.0
    return _to_float(txt, default=0.0)


def _meta_has_video_dimensions(meta: dict) -> bool:
    try:
        return int(meta.get("width") or 0) > 0 and int(meta.get("height") or 0) > 0
    except Exception:
        return False


def _normalize_video_for_opencv(input_path: Path):
    normalized_path = input_path.with_name(f"{input_path.stem}_normalized.mp4")
    cmd = [
        _resolve_ffmpeg_bin(),
        "-y",
        "-i",
        str(input_path),
        "-map",
        "0:v:0",
        "-map",
        "0:a?",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "veryfast",
        "-crf",
        "18",
        "-movflags",
        "+faststart",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(normalized_path),
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    except Exception as exc:
        return False, f"normalize error: {exc}", input_path
    if proc.returncode != 0 or not normalized_path.exists():
        err = (proc.stderr or "").strip()
        try:
            if normalized_path.exists():
                normalized_path.unlink()
        except Exception:
            pass
        return False, f"normalize ffmpeg failed: {err[-220:] if err else 'unknown'}", input_path
    return True, "", normalized_path


def _normalize_timeline_segments(segments, duration_sec=None):
    cleaned = []
    dropped_invalid = 0
    adjusted_overlap = 0
    merged_same_speaker = 0

    max_duration = None
    try:
        if duration_sec is not None:
            d = float(duration_sec)
            if d > 0:
                max_duration = d
    except Exception:
        max_duration = None

    for seg in segments:
        start = max(0.0, _to_float(seg.get("start_sec", 0.0), 0.0))
        end = max(0.0, _to_float(seg.get("end_sec", 0.0), 0.0))
        speaker_face_id = str(seg.get("speaker_face_id", "")).strip()
        if max_duration is not None:
            start = min(start, max_duration)
            end = min(end, max_duration)
        if end <= start:
            dropped_invalid += 1
            continue
        cleaned.append({"start_sec": start, "end_sec": end, "speaker_face_id": speaker_face_id})

    cleaned.sort(key=lambda s: (s["start_sec"], s["end_sec"]))
    normalized = []
    for seg in cleaned:
        if not normalized:
            normalized.append(seg)
            continue
        prev = normalized[-1]
        if seg["start_sec"] < prev["end_sec"]:
            if seg["speaker_face_id"] == prev["speaker_face_id"]:
                prev["end_sec"] = max(prev["end_sec"], seg["end_sec"])
                merged_same_speaker += 1
                continue
            seg = dict(seg)
            seg["start_sec"] = prev["end_sec"]
            adjusted_overlap += 1
            if seg["end_sec"] <= seg["start_sec"]:
                dropped_invalid += 1
                continue
        if seg["speaker_face_id"] == prev["speaker_face_id"] and seg["start_sec"] <= prev["end_sec"] + 1e-6:
            prev["end_sec"] = max(prev["end_sec"], seg["end_sec"])
            merged_same_speaker += 1
            continue
        normalized.append(seg)

    return {
        "segments": normalized,
        "stats": {
            "input_count": len(segments),
            "saved_count": len(normalized),
            "dropped_invalid": dropped_invalid,
            "adjusted_overlap": adjusted_overlap,
            "merged_same_speaker": merged_same_speaker,
            "duration_sec": max_duration,
        },
    }


def _choose_face_box(candidates, current_bbox, seed_center):
    if not candidates:
        return None
    if current_bbox is None:
        return min(candidates, key=lambda b: _center_distance(_bbox_center(b), seed_center))
    best = None
    best_score = -10**9
    curr_center = _bbox_center(current_bbox)
    curr_area = max(1.0, float(current_bbox["w"]) * float(current_bbox["h"]))
    for box in candidates:
        iou = _bbox_iou(current_bbox, box)
        cdist = _center_distance(_bbox_center(box), curr_center)
        area = max(1.0, float(box["w"]) * float(box["h"]))
        area_ratio = min(area, curr_area) / max(area, curr_area)
        score = (2.2 * iou) + (0.8 * area_ratio) - (0.0025 * cdist)
        if score > best_score:
            best = box
            best_score = score
    return best


def _normalize_exec_mode(mode: str) -> str:
    mode = str(mode or "").strip().lower()
    if mode in {"local", "manual"}:
        return mode
    return "local"


def _to_bool_flag(value, default=False) -> bool:
    if value is None:
        return bool(default)
    if isinstance(value, bool):
        return value
    txt = str(value).strip().lower()
    if txt in {"1", "true", "yes", "on"}:
        return True
    if txt in {"0", "false", "no", "off"}:
        return False
    return bool(default)


def _to_int_clamped(value, default: int, min_value: int, max_value: int) -> int:
    try:
        num = int(value)
    except Exception:
        num = int(default)
    return max(min_value, min(max_value, num))


def _normalize_pads(value, default: str = "0 10 0 0") -> str:
    raw = str(value or "").replace(",", " ").split()
    if len(raw) != 4:
        return default
    parsed = []
    for token in raw:
        try:
            parsed.append(str(int(token)))
        except Exception:
            return default
    return " ".join(parsed)


def _pick_next_queued_job(job_store: JsonKeyValueStore):
    jobs = sorted(job_store.list_all(), key=lambda x: x.get("created_at", ""))
    for job in jobs:
        if str(job.get("status", "")).lower() == "queued":
            return job
    return None


def _runtime_defaults():
    default_use_box = _to_bool_flag(W2L_USE_BOX, default=False)
    default_nosmooth = _to_bool_flag(W2L_NOSMOOTH, default=False)
    default_enhance_sharpen = _to_bool_flag(W2L_ENHANCE_SHARPEN, default=False)
    default_enhance_denoise = _to_bool_flag(W2L_ENHANCE_DENOISE, default=False)
    default_enhance_color_boost = _to_bool_flag(W2L_ENHANCE_COLOR_BOOST, default=False)
    default_enhance_ultra = _to_bool_flag(W2L_ENHANCE_ULTRA, default=False)
    default_enhance_extreme = _to_bool_flag(W2L_ENHANCE_EXTREME, default=False)
    default_enhance_face_restore = _to_bool_flag(W2L_ENHANCE_FACE_RESTORE, default=False)
    default_enhance_two_pass = _to_bool_flag(W2L_ENHANCE_TWO_PASS, default=False)
    default_enhance_quality_gate = _to_bool_flag(W2L_ENHANCE_QUALITY_GATE, default=False)
    default_enhance_temporal = _to_bool_flag(W2L_ENHANCE_TEMPORAL, default=False)
    default_enhance_deblock = _to_bool_flag(W2L_ENHANCE_DEBLOCK, default=False)
    default_enhance_multicandidate = _to_bool_flag(W2L_ENHANCE_MULTICANDIDATE, default=False)
    default_enhance_10bit = _to_bool_flag(W2L_ENHANCE_10BIT, default=False)
    default_enhance_anti_flicker = _to_bool_flag(W2L_ENHANCE_ANTI_FLICKER, default=False)
    default_enhance_scene_cut = _to_bool_flag(W2L_ENHANCE_SCENE_CUT, default=False)
    try:
        default_face_det_batch = max(1, int(W2L_FACE_DET_BATCH))
    except Exception:
        default_face_det_batch = 16
    try:
        default_wav2lip_batch = max(1, int(W2L_BATCH))
    except Exception:
        default_wav2lip_batch = 64
    try:
        default_resize_factor = max(1, int(W2L_RESIZE_FACTOR))
    except Exception:
        default_resize_factor = 1
    return {
        "exec_mode": _normalize_exec_mode(W2L_EXEC_MODE or "local"),
        "infer_command": W2L_INFER_CMD,
        "timeout_sec": max(10, int(W2L_CMD_TIMEOUT_SEC)),
        "checkpoint_path": W2L_CHECKPOINT_PATH,
        "use_box": default_use_box,
        "face_det_batch": default_face_det_batch,
        "wav2lip_batch": default_wav2lip_batch,
        "pads": W2L_PADS or "0 10 0 0",
        "resize_factor": default_resize_factor,
        "nosmooth": default_nosmooth,
        "enhance_sharpen": default_enhance_sharpen,
        "enhance_denoise": default_enhance_denoise,
        "enhance_color_boost": default_enhance_color_boost,
        "enhance_ultra": default_enhance_ultra,
        "enhance_extreme": default_enhance_extreme,
        "enhance_face_restore": default_enhance_face_restore,
        "enhance_two_pass": default_enhance_two_pass,
        "enhance_quality_gate": default_enhance_quality_gate,
        "enhance_temporal": default_enhance_temporal,
        "enhance_deblock": default_enhance_deblock,
        "enhance_multicandidate": default_enhance_multicandidate,
        "enhance_10bit": default_enhance_10bit,
        "enhance_anti_flicker": default_enhance_anti_flicker,
        "enhance_scene_cut": default_enhance_scene_cut,
    }


def _portable_checkpoint_candidates():
    repo_dir = PROJECT_DIR / "Wav2Lip"
    ckpt_dir = repo_dir / "checkpoints"
    return [
        ckpt_dir / "wav2lip_gan.pth",
        ckpt_dir / "wav2lip.pth",
    ]


def _normalize_checkpoint_path_for_portable(current_value: str, default_value: str) -> str:
    raw = str(current_value or "").strip()
    if raw:
        try:
            current_path = Path(raw)
            if current_path.exists():
                return raw
        except Exception:
            pass
    default_raw = str(default_value or "").strip()
    if default_raw:
        try:
            default_path = Path(default_raw)
            if default_path.exists():
                return default_raw
        except Exception:
            pass
    for candidate in _portable_checkpoint_candidates():
        try:
            if candidate.exists():
                return str(candidate)
        except Exception:
            pass
    return raw


def _resolve_ffmpeg_bin() -> str:
    if FFMPEG_EXE.exists():
        return str(FFMPEG_EXE)
    return "ffmpeg"


def _resolve_ffprobe_bin() -> str:
    if FFPROBE_EXE.exists():
        return str(FFPROBE_EXE)
    return "ffprobe"


def _ensure_runtime_settings(store: JsonKeyValueStore):
    rec = store.get("runtime")
    defaults = _runtime_defaults()
    if not rec:
        rec = {
            **defaults,
            "created_at": _utc_now(),
            "updated_at": _utc_now(),
        }
        store.set("runtime", rec)
        return rec
    changed = False
    for key, val in defaults.items():
        if key not in rec:
            rec[key] = val
            changed = True
    normalized_ckpt = _normalize_checkpoint_path_for_portable(
        str(rec.get("checkpoint_path", "") or ""),
        str(defaults.get("checkpoint_path", "") or ""),
    )
    if normalized_ckpt != str(rec.get("checkpoint_path", "") or ""):
        rec["checkpoint_path"] = normalized_ckpt
        changed = True
    if changed:
        rec["updated_at"] = _utc_now()
        store.set("runtime", rec)
    return rec


def create_app(window_action=None, window_rect=None, window_move=None):
    _prepare_dirs()
    _startup_cleanup_artifacts()
    job_store = JsonKeyValueStore(JOBS_FILE)
    settings_store = JsonKeyValueStore(SETTINGS_FILE)
    video_index = JsonKeyValueStore(VIDEO_INDEX_FILE)
    selections = JsonKeyValueStore(SELECTIONS_FILE)
    timelines = JsonKeyValueStore(TIMELINES_FILE)
    tracks = JsonKeyValueStore(TRACKS_FILE)
    probe_engine = FaceProbeEngine()
    tracker_engine = FaceTrackerEngine(probe_engine)
    _ensure_runtime_settings(settings_store)

    def _get_runtime_settings():
        return _ensure_runtime_settings(settings_store)

    runner = JobRunner(job_store, _get_runtime_settings)
    app = Flask(__name__, static_folder=str(WEB_DIR), static_url_path="")

    @app.get("/")
    def index_page():
        return send_from_directory(WEB_DIR, "index.html")

    @app.get("/api/health")
    def api_health():
        return jsonify({"ok": True, "service": "wav2lip-viewer"})

    @app.get("/api/config")
    def api_config():
        runtime = _get_runtime_settings()
        return jsonify(
            {
                "ok": True,
                "mode": "command" if runtime.get("infer_command") else "stub",
                "command_configured": bool(runtime.get("infer_command")),
                "exec_mode": runtime.get("exec_mode", "local"),
                "timeout_sec": int(runtime.get("timeout_sec", W2L_CMD_TIMEOUT_SEC)),
                "queue_size": runner.queue_size(),
                "probe_backend": probe_engine.mode,
                "track_backend": tracker_engine.mode,
            }
        )

    @app.get("/api/settings")
    def api_settings_get():
        return jsonify({"ok": True, "settings": _get_runtime_settings()})

    @app.post("/api/settings")
    def api_settings_set():
        payload = request.get_json(silent=True) or {}
        current = _get_runtime_settings()
        infer_command = str(payload.get("infer_command", current.get("infer_command", "")))
        exec_mode = _normalize_exec_mode(payload.get("exec_mode", current.get("exec_mode", "local")))
        timeout_sec = int(payload.get("timeout_sec", current.get("timeout_sec", W2L_CMD_TIMEOUT_SEC)) or W2L_CMD_TIMEOUT_SEC)
        timeout_sec = max(10, min(86400, timeout_sec))
        checkpoint_path = str(payload.get("checkpoint_path", current.get("checkpoint_path", "")) or "").strip()
        use_box = _to_bool_flag(payload.get("use_box", current.get("use_box", False)), default=False)
        face_det_batch = _to_int_clamped(payload.get("face_det_batch", current.get("face_det_batch", 16)), 16, 1, 512)
        wav2lip_batch = _to_int_clamped(payload.get("wav2lip_batch", current.get("wav2lip_batch", 64)), 64, 1, 512)
        pads_default = str(current.get("pads", "0 10 0 0") or "0 10 0 0")
        pads = _normalize_pads(payload.get("pads", pads_default), default=pads_default)
        resize_factor = _to_int_clamped(payload.get("resize_factor", current.get("resize_factor", 1)), 1, 1, 8)
        nosmooth = _to_bool_flag(payload.get("nosmooth", current.get("nosmooth", False)), default=False)
        enhance_sharpen = _to_bool_flag(payload.get("enhance_sharpen", current.get("enhance_sharpen", False)), default=False)
        enhance_denoise = _to_bool_flag(payload.get("enhance_denoise", current.get("enhance_denoise", False)), default=False)
        enhance_color_boost = _to_bool_flag(payload.get("enhance_color_boost", current.get("enhance_color_boost", False)), default=False)
        enhance_ultra = _to_bool_flag(payload.get("enhance_ultra", current.get("enhance_ultra", False)), default=False)
        enhance_extreme = _to_bool_flag(payload.get("enhance_extreme", current.get("enhance_extreme", False)), default=False)
        enhance_face_restore = _to_bool_flag(payload.get("enhance_face_restore", current.get("enhance_face_restore", False)), default=False)
        enhance_two_pass = _to_bool_flag(payload.get("enhance_two_pass", current.get("enhance_two_pass", False)), default=False)
        enhance_quality_gate = _to_bool_flag(payload.get("enhance_quality_gate", current.get("enhance_quality_gate", False)), default=False)
        enhance_temporal = _to_bool_flag(payload.get("enhance_temporal", current.get("enhance_temporal", False)), default=False)
        enhance_deblock = _to_bool_flag(payload.get("enhance_deblock", current.get("enhance_deblock", False)), default=False)
        enhance_multicandidate = _to_bool_flag(
            payload.get("enhance_multicandidate", current.get("enhance_multicandidate", False)), default=False
        )
        enhance_10bit = _to_bool_flag(payload.get("enhance_10bit", current.get("enhance_10bit", False)), default=False)
        enhance_anti_flicker = _to_bool_flag(
            payload.get("enhance_anti_flicker", current.get("enhance_anti_flicker", False)), default=False
        )
        enhance_scene_cut = _to_bool_flag(
            payload.get("enhance_scene_cut", current.get("enhance_scene_cut", False)), default=False
        )

        rec = {
            **current,
            "infer_command": infer_command.strip(),
            "exec_mode": exec_mode,
            "timeout_sec": timeout_sec,
            "checkpoint_path": checkpoint_path,
            "use_box": use_box,
            "face_det_batch": face_det_batch,
            "wav2lip_batch": wav2lip_batch,
            "pads": pads,
            "resize_factor": resize_factor,
            "nosmooth": nosmooth,
            "enhance_sharpen": enhance_sharpen,
            "enhance_denoise": enhance_denoise,
            "enhance_color_boost": enhance_color_boost,
            "enhance_ultra": enhance_ultra,
            "enhance_extreme": enhance_extreme,
            "enhance_face_restore": enhance_face_restore,
            "enhance_two_pass": enhance_two_pass,
            "enhance_quality_gate": enhance_quality_gate,
            "enhance_temporal": enhance_temporal,
            "enhance_deblock": enhance_deblock,
            "enhance_multicandidate": enhance_multicandidate,
            "enhance_10bit": enhance_10bit,
            "enhance_anti_flicker": enhance_anti_flicker,
            "enhance_scene_cut": enhance_scene_cut,
            "updated_at": _utc_now(),
        }
        if "created_at" not in rec:
            rec["created_at"] = _utc_now()
        settings_store.set("runtime", rec)
        return jsonify({"ok": True, "settings": rec})

    @app.post("/api/video/upload")
    def api_video_upload():
        video = request.files.get("video")
        if video is None:
            return jsonify({"ok": False, "error": "video file is required"}), 400

        video_name = _safe_upload_filename(video.filename or "", fallback_stem="video")
        if not video_name:
            return jsonify({"ok": False, "error": "Invalid video file name"}), 400
        video_ext = Path(video_name).suffix.lower()
        if not video_ext:
            return jsonify({"ok": False, "error": "Video file extension is required"}), 400
        if not _is_allowed(video_ext, ALLOWED_VIDEO_EXT):
            return jsonify({"ok": False, "error": f"Unsupported video format: {video_ext}"}), 400

        video_id = _make_video_id()
        saved_video_name = f"{video_id}_{video_name}"
        video_path = VIDEOS_DIR / saved_video_name
        video.save(str(video_path))
        meta = _read_video_meta(video_path, cv2_mod=probe_engine._cv2)
        if not _meta_has_video_dimensions(meta):
            ok_norm, norm_err, normalized_path = _normalize_video_for_opencv(video_path)
            if ok_norm:
                try:
                    video_path.unlink(missing_ok=True)
                except Exception:
                    pass
                video_path = normalized_path
                saved_video_name = normalized_path.name
                meta = _read_video_meta(video_path, cv2_mod=probe_engine._cv2)
            else:
                if not _meta_has_video_dimensions(meta):
                    return jsonify(
                        {
                            "ok": False,
                            "error": (
                                "Video container is accepted but decoding failed for this codec/profile. "
                                f"ffmpeg normalize fallback also failed: {norm_err}"
                            ),
                        }
                    ), 400

        rec = {
            "id": video_id,
            "video_file": saved_video_name,
            "meta": meta,
            "created_at": _utc_now(),
            "updated_at": _utc_now(),
        }
        video_index.set(video_id, rec)
        return jsonify({"ok": True, "video": rec})

    @app.get("/api/video/meta")
    def api_video_meta():
        video_id = str(request.args.get("video_id", "")).strip()
        if not video_id:
            return jsonify({"ok": False, "error": "video_id is required"}), 400
        video_rec = video_index.get(video_id)
        if not video_rec:
            return jsonify({"ok": False, "error": "video_id not found"}), 404

        video_path = VIDEOS_DIR / video_rec["video_file"]
        if not video_path.exists():
            return jsonify({"ok": False, "error": "video file is missing on disk"}), 404

        meta = video_rec.get("meta") or {}
        if not meta:
            meta = _read_video_meta(video_path, cv2_mod=probe_engine._cv2)
            patched = video_index.patch(video_id, meta=meta)
            if patched:
                video_rec = patched
        return jsonify({"ok": True, "video_id": video_id, "meta": meta})

    @app.post("/api/video/probe")
    def api_video_probe():
        payload = request.get_json(silent=True) or {}
        video_id = str(payload.get("video_id", "")).strip()
        frame_ratio = _to_float(payload.get("frame_ratio", 0.5), default=0.5)
        if not video_id:
            return jsonify({"ok": False, "error": "video_id is required"}), 400

        video_rec = video_index.get(video_id)
        if not video_rec:
            return jsonify({"ok": False, "error": "video_id not found"}), 404
        video_path = VIDEOS_DIR / video_rec["video_file"]
        if not video_path.exists():
            return jsonify({"ok": False, "error": "video file is missing on disk"}), 404

        ok, error, probed = probe_engine.probe(video_path, frame_ratio)
        if not ok:
            return jsonify({"ok": False, "error": error}), 500
        return jsonify({"ok": True, "probe": probed})

    @app.post("/api/face/select")
    def api_face_select():
        payload = request.get_json(silent=True) or {}
        video_id = str(payload.get("video_id", "")).strip()
        face_id = str(payload.get("face_id", "")).strip()
        bbox = payload.get("bbox") or {}
        frame_ratio = _to_float(payload.get("frame_ratio", 0.0), default=0.0)
        detector_mode = str(payload.get("detector_mode", "")).strip()

        if not video_id or not face_id:
            return jsonify({"ok": False, "error": "video_id and face_id are required"}), 400

        for key in ["x", "y", "w", "h"]:
            if key not in bbox:
                return jsonify({"ok": False, "error": "bbox must include x,y,w,h"}), 400

        rec = {
            "video_id": video_id,
            "face_id": face_id,
            "bbox": {
                "x": int(bbox["x"]),
                "y": int(bbox["y"]),
                "w": int(bbox["w"]),
                "h": int(bbox["h"]),
            },
            "frame_ratio": max(0.0, min(1.0, frame_ratio)),
            "detector_mode": detector_mode,
            "created_at": _utc_now(),
            "updated_at": _utc_now(),
        }
        selections.set(video_id, rec)
        tracks.set(video_id, {"video_id": video_id, "points": [], "created_at": _utc_now(), "updated_at": _utc_now()})
        return jsonify({"ok": True, "selection": rec})

    @app.get("/api/face/selection")
    def api_face_selection_get():
        video_id = str(request.args.get("video_id", "")).strip()
        if not video_id:
            return jsonify({"ok": False, "error": "video_id is required"}), 400
        rec = selections.get(video_id)
        if not rec:
            return jsonify({"ok": True, "selection": None})
        return jsonify({"ok": True, "selection": rec})

    @app.post("/api/tracking/build")
    def api_tracking_build():
        payload = request.get_json(silent=True) or {}
        video_id = str(payload.get("video_id", "")).strip()
        sample_step = int(payload.get("sample_step", 3) or 3)
        if not video_id:
            return jsonify({"ok": False, "error": "video_id is required"}), 400
        video_rec = video_index.get(video_id)
        if not video_rec:
            return jsonify({"ok": False, "error": "video_id not found"}), 404
        selection = selections.get(video_id)
        if not selection:
            return jsonify({"ok": False, "error": "Select target face before tracking"}), 400

        video_path = VIDEOS_DIR / video_rec["video_file"]
        if not video_path.exists():
            return jsonify({"ok": False, "error": "video file is missing on disk"}), 404
        ok, error, track_payload = tracker_engine.build_track(
            video_path=video_path,
            seed_bbox=selection["bbox"],
            seed_ratio=selection.get("frame_ratio", 0.0),
            sample_step=sample_step,
        )
        if not ok:
            return jsonify({"ok": False, "error": error}), 500

        rec = {
            "video_id": video_id,
            "target_face_id": selection["face_id"],
            "created_at": _utc_now(),
            "updated_at": _utc_now(),
            **track_payload,
        }
        tracks.set(video_id, rec)
        return jsonify({"ok": True, "track": rec})

    @app.get("/api/tracking")
    def api_tracking_get():
        video_id = str(request.args.get("video_id", "")).strip()
        if not video_id:
            return jsonify({"ok": False, "error": "video_id is required"}), 400
        rec = tracks.get(video_id)
        return jsonify({"ok": True, "track": rec})

    @app.post("/api/timeline/save")
    def api_timeline_save():
        payload = request.get_json(silent=True) or {}
        video_id = str(payload.get("video_id", "")).strip()
        segments = payload.get("segments") or []
        if not video_id:
            return jsonify({"ok": False, "error": "video_id is required"}), 400
        if not isinstance(segments, list):
            return jsonify({"ok": False, "error": "segments must be a list"}), 400
        video_rec = video_index.get(video_id)
        if not video_rec:
            return jsonify({"ok": False, "error": "video_id not found"}), 404
        selection = selections.get(video_id)
        allowed_speakers = {""}
        if selection and str(selection.get("face_id", "")).strip():
            allowed_speakers.add(str(selection.get("face_id", "")).strip())

        invalid_speakers = set()
        for idx, seg in enumerate(segments):
            if not isinstance(seg, dict):
                return jsonify({"ok": False, "error": f"segments[{idx}] must be an object"}), 400
            speaker = str(seg.get("speaker_face_id", "")).strip()
            if speaker and speaker not in allowed_speakers:
                invalid_speakers.add(speaker)
        if invalid_speakers:
            return (
                jsonify(
                    {
                        "ok": False,
                        "error": "Invalid speaker_face_id in timeline segments",
                        "invalid_speaker_face_ids": sorted(invalid_speakers),
                        "allowed_speaker_face_ids": sorted([s for s in allowed_speakers if s]),
                    }
                ),
                400,
            )

        duration_sec = ((video_rec.get("meta") or {}).get("duration_sec"))
        normalized = _normalize_timeline_segments(segments, duration_sec=duration_sec)

        rec = {
            "video_id": video_id,
            "segments": normalized["segments"],
            "stats": normalized["stats"],
            "created_at": _utc_now(),
            "updated_at": _utc_now(),
        }
        timelines.set(video_id, rec)
        return jsonify({"ok": True, "timeline": rec})

    @app.get("/api/timeline")
    def api_timeline_get():
        video_id = str(request.args.get("video_id", "")).strip()
        if not video_id:
            return jsonify({"ok": False, "error": "video_id is required"}), 400
        rec = timelines.get(video_id)
        if not rec:
            return jsonify({"ok": True, "timeline": {"video_id": video_id, "segments": []}})
        return jsonify({"ok": True, "timeline": rec})

    @app.post("/api/job/submit")
    def api_job_submit():
        video_id = str(request.form.get("video_id", "")).strip()
        audio = request.files.get("audio")
        if not video_id:
            return jsonify({"ok": False, "error": "video_id is required"}), 400
        if audio is None:
            return jsonify({"ok": False, "error": "audio file is required"}), 400

        video_rec = video_index.get(video_id)
        if not video_rec:
            return jsonify({"ok": False, "error": "video_id not found"}), 404
        selection = selections.get(video_id)
        if not selection:
            return jsonify({"ok": False, "error": "Select target face before creating job"}), 400
        tracking = tracks.get(video_id)
        if not tracking or not tracking.get("points"):
            return jsonify({"ok": False, "error": "Build target face tracking before creating job"}), 400

        timeline = timelines.get(video_id) or {"video_id": video_id, "segments": []}

        audio_name = _safe_upload_filename(audio.filename or "", fallback_stem="audio")
        if not audio_name:
            return jsonify({"ok": False, "error": "Invalid audio file name"}), 400
        audio_ext = Path(audio_name).suffix.lower()
        if not audio_ext:
            return jsonify({"ok": False, "error": "Audio file extension is required"}), 400
        if not _is_allowed(audio_ext, ALLOWED_AUDIO_EXT):
            return jsonify({"ok": False, "error": f"Unsupported audio format: {audio_ext}"}), 400

        job_id = uuid.uuid4().hex[:12]
        saved_audio_name = f"{job_id}_{audio_name}"
        video_file = video_rec["video_file"]
        video_ext = Path(video_file).suffix.lower() or ".mp4"
        output_name = f"{job_id}_result{video_ext}"

        audio_path = AUDIOS_DIR / saved_audio_name
        audio.save(str(audio_path))

        now = _utc_now()
        record = {
            "id": job_id,
            "status": "queued",
            "progress": 0,
            "created_at": now,
            "updated_at": now,
            "video_ref_id": video_id,
            "video_file": video_file,
            "audio_file": saved_audio_name,
            "output_file": output_name,
            "output_url": "",
            "target_face": selection,
            "timeline": timeline,
            "tracking": tracking,
            "message": "Queued",
        }
        job_store.set(job_id, record)
        runtime = _get_runtime_settings()
        if runtime.get("exec_mode", "local") == "local":
            runner.enqueue(job_id)
        return jsonify({"ok": True, "job": record})

    @app.post("/api/job/requeue")
    def api_job_requeue():
        payload = request.get_json(silent=True) or {}
        job_id = str(payload.get("job_id", "")).strip()
        if not job_id:
            return jsonify({"ok": False, "error": "job_id is required"}), 400
        rec = job_store.get(job_id)
        if not rec:
            return jsonify({"ok": False, "error": "Job not found"}), 404

        updated = job_store.patch(
            job_id,
            status="queued",
            started_at=None,
            finished_at=None,
            output_url="",
            worker_id="",
            leased_at=None,
            progress=0,
            message="Requeued",
        )
        runtime = _get_runtime_settings()
        if runtime.get("exec_mode", "local") == "local":
            runner.enqueue(job_id)
        return jsonify({"ok": True, "job": updated})

    @app.post("/api/job/cancel")
    def api_job_cancel():
        payload = request.get_json(silent=True) or {}
        job_id = str(payload.get("job_id", "")).strip()
        if not job_id:
            return jsonify({"ok": False, "error": "job_id is required"}), 400
        rec = job_store.get(job_id)
        if not rec:
            return jsonify({"ok": False, "error": "Job not found"}), 404
        status = str(rec.get("status", "")).lower()
        if status in {"done", "failed", "canceled"}:
            return jsonify({"ok": True, "job": rec})
        if status == "running":
            return jsonify({"ok": False, "error": "Running job cannot be canceled safely"}), 409

        updated = job_store.patch(
            job_id,
            status="canceled",
            finished_at=_utc_now(),
            progress=100,
            message="Canceled by user",
        )
        return jsonify({"ok": True, "job": updated})

    @app.post("/api/job/delete")
    def api_job_delete():
        payload = request.get_json(silent=True) or {}
        job_id = str(payload.get("job_id", "")).strip()
        if not job_id:
            return jsonify({"ok": False, "error": "job_id is required"}), 400
        rec = job_store.get(job_id)
        if not rec:
            return jsonify({"ok": False, "error": "Job not found"}), 404
        status = str(rec.get("status", "")).lower()
        if status in {"running", "leased"}:
            return jsonify({"ok": False, "error": f"Cannot delete job in status {status}"}), 409

        deleted = job_store.delete(job_id)
        if not deleted:
            return jsonify({"ok": False, "error": "Job not found"}), 404

        try:
            audio_file = str(deleted.get("audio_file", "")).strip()
            if audio_file:
                audio_path = AUDIOS_DIR / audio_file
                if audio_path.exists():
                    audio_path.unlink()
        except Exception:
            pass
        try:
            output_file = str(deleted.get("output_file", "")).strip()
            if output_file:
                output_path = OUTPUTS_DIR / output_file
                if output_path.exists():
                    output_path.unlink()
        except Exception:
            pass
        try:
            temp_dir = TEMP_DIR / f"job_{job_id}"
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass
        return jsonify({"ok": True, "deleted_job_id": job_id})

    @app.post("/api/worker/claim")
    def api_worker_claim():
        payload = request.get_json(silent=True) or {}
        worker_id = str(payload.get("worker_id", "")).strip()
        if not worker_id:
            return jsonify({"ok": False, "error": "worker_id is required"}), 400

        runtime = _get_runtime_settings()
        if runtime.get("exec_mode", "local") != "manual":
            return jsonify({"ok": False, "error": "worker claim is allowed only in manual exec_mode"}), 409

        job = _pick_next_queued_job(job_store)
        if not job:
            return jsonify({"ok": True, "job": None})

        leased = job_store.patch(
            job["id"],
            status="leased",
            worker_id=worker_id,
            leased_at=_utc_now(),
            progress=10,
            message=f"Leased by worker {worker_id}",
        )
        return jsonify({"ok": True, "job": leased})

    @app.post("/api/worker/complete")
    def api_worker_complete():
        job_id = str(request.form.get("job_id", "")).strip()
        worker_id = str(request.form.get("worker_id", "")).strip()
        output = request.files.get("output")
        if not job_id or not worker_id:
            return jsonify({"ok": False, "error": "job_id and worker_id are required"}), 400
        if output is None:
            return jsonify({"ok": False, "error": "output file is required"}), 400

        job = job_store.get(job_id)
        if not job:
            return jsonify({"ok": False, "error": "Job not found"}), 404
        if str(job.get("worker_id", "")).strip() != worker_id:
            return jsonify({"ok": False, "error": "worker_id does not match leased job"}), 409
        if str(job.get("status", "")).lower() not in {"leased", "running"}:
            return jsonify({"ok": False, "error": f"Job status is {job.get('status')}, cannot complete"}), 409

        output_path = OUTPUTS_DIR / job["output_file"]
        output.save(str(output_path))

        updated = job_store.patch(
            job_id,
            status="done",
            finished_at=_utc_now(),
            progress=100,
            output_url=f"/outputs/{job['output_file']}",
            message=f"Completed by worker {worker_id}",
        )
        return jsonify({"ok": True, "job": updated})

    @app.post("/api/worker/fail")
    def api_worker_fail():
        payload = request.get_json(silent=True) or {}
        job_id = str(payload.get("job_id", "")).strip()
        worker_id = str(payload.get("worker_id", "")).strip()
        error = str(payload.get("error", "")).strip() or "worker reported failure"
        if not job_id or not worker_id:
            return jsonify({"ok": False, "error": "job_id and worker_id are required"}), 400

        job = job_store.get(job_id)
        if not job:
            return jsonify({"ok": False, "error": "Job not found"}), 404
        if str(job.get("worker_id", "")).strip() != worker_id:
            return jsonify({"ok": False, "error": "worker_id does not match leased job"}), 409
        if str(job.get("status", "")).lower() not in {"leased", "running"}:
            return jsonify({"ok": False, "error": f"Job status is {job.get('status')}, cannot fail"}), 409

        updated = job_store.patch(
            job_id,
            status="failed",
            finished_at=_utc_now(),
            progress=100,
            message=f"Worker {worker_id} failed: {error}",
        )
        return jsonify({"ok": True, "job": updated})

    @app.get("/api/jobs")
    def api_jobs():
        jobs = sorted(job_store.list_all(), key=lambda x: x.get("created_at", ""), reverse=True)
        stats = {"queued": 0, "leased": 0, "running": 0, "done": 0, "failed": 0, "canceled": 0}
        for j in jobs:
            s = str(j.get("status", "")).lower()
            if s in stats:
                stats[s] += 1
        return jsonify({"ok": True, "jobs": jobs[:100], "queue_size": stats["queued"], "stats": stats})

    @app.get("/api/job/<job_id>")
    def api_job_get(job_id: str):
        rec = job_store.get(job_id)
        if rec is None:
            return jsonify({"ok": False, "error": "Job not found."}), 404
        return jsonify({"ok": True, "job": rec})

    @app.post("/api/output/open")
    def api_output_open():
        payload = request.get_json(silent=True) or {}
        job_id = str(payload.get("job_id", "")).strip()
        if not job_id:
            return jsonify({"ok": False, "error": "job_id is required"}), 400
        rec = job_store.get(job_id)
        if not rec:
            return jsonify({"ok": False, "error": "Job not found"}), 404
        output_file = str(rec.get("output_file", "")).strip()
        if not output_file:
            return jsonify({"ok": False, "error": "Job has no output file"}), 400
        output_path = OUTPUTS_DIR / output_file
        if not output_path.exists():
            return jsonify({"ok": False, "error": "Output file is missing on disk"}), 404
        try:
            os.startfile(str(output_path))  # type: ignore[attr-defined]
        except Exception as exc:
            return jsonify({"ok": False, "error": f"Cannot open output file: {exc}"}), 500
        return jsonify({"ok": True})

    @app.get("/outputs/<path:filename>")
    def outputs_file(filename: str):
        return send_from_directory(OUTPUTS_DIR, filename, as_attachment=False)

    @app.post("/api/window/action")
    def api_window_action():
        payload = request.get_json(silent=True) or {}
        action = str(payload.get("action", "")).strip().lower()
        scope = str(payload.get("scope", "main")).strip().lower()
        if action not in {"minimize", "maximize", "close", "drag"}:
            return jsonify({"ok": False, "error": "Invalid action."}), 400
        if not callable(window_action):
            return jsonify({"ok": False, "error": "Window API unavailable."}), 503
        ok = bool(window_action(action, scope))
        return jsonify({"ok": ok})

    @app.get("/api/window/rect")
    def api_window_rect():
        scope = str(request.args.get("scope", "main")).strip().lower()
        if not callable(window_rect):
            return jsonify({"ok": False, "error": "Window API unavailable."}), 503
        return jsonify(window_rect(scope))

    @app.post("/api/window/move")
    def api_window_move():
        payload = request.get_json(silent=True) or {}
        scope = str(payload.get("scope", "main")).strip().lower()
        left = payload.get("left")
        top = payload.get("top")
        if left is None or top is None:
            return jsonify({"ok": False, "error": "left and top are required."}), 400
        if not callable(window_move):
            return jsonify({"ok": False, "error": "Window API unavailable."}), 503
        ok = bool(window_move(int(left), int(top), scope))
        return jsonify({"ok": ok})

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=8090, debug=False, threaded=True)
