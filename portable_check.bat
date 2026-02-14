@echo off
setlocal
cd /d %~dp0

set FAIL=0

echo [Portable Check] Wav2LipViewer
echo.

call :check_file "app\python\python.exe"
call :check_file "app\python\pythonw.exe"
call :check_file "app\launcher.py"
call :check_file "app\main.py"
call :check_file "app\web\index.html"
call :check_file "app\web\app.js"
call :check_file "app\bin\ffmpeg\ffmpeg.exe"
call :check_file "app\bin\ffmpeg\ffprobe.exe"

if exist "Wav2Lip\inference.py" (
  echo [OK]   Wav2Lip\inference.py
) else (
  echo [WARN] Wav2Lip\inference.py is missing (real inference mode unavailable, stub mode still works)
)

if exist "Wav2Lip\checkpoints\wav2lip_gan.pth" (
  echo [OK]   Wav2Lip\checkpoints\wav2lip_gan.pth
) else if exist "Wav2Lip\checkpoints\wav2lip.pth" (
  echo [OK]   Wav2Lip\checkpoints\wav2lip.pth
) else (
  echo [WARN] No checkpoint found in Wav2Lip\checkpoints\ (real inference mode unavailable)
)

echo.
if "%FAIL%"=="0" (
  echo Result: PASS ^(portable bundle files are present^)
  exit /b 0
) else (
  echo Result: FAIL ^(one or more required files are missing^)
  exit /b 1
)

:check_file
if exist "%~1" (
  echo [OK]   %~1
) else (
  echo [MISS] %~1
  set FAIL=1
)
exit /b 0
