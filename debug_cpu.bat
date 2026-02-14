@echo off
setlocal
cd /d %~dp0
set W2L_USE_GPU=0
if "%W2L_REPO_DIR%"=="" set W2L_REPO_DIR=%~dp0Wav2Lip
if "%W2L_CHECKPOINT_PATH%"=="" (
  if exist "%~dp0Wav2Lip\checkpoints\wav2lip_gan.pth" (
    set W2L_CHECKPOINT_PATH=%~dp0Wav2Lip\checkpoints\wav2lip_gan.pth
  ) else if exist "%~dp0Wav2Lip\checkpoints\wav2lip.pth" (
    set W2L_CHECKPOINT_PATH=%~dp0Wav2Lip\checkpoints\wav2lip.pth
  )
)
set PYTHON_EXE=app\python\python.exe
if not exist "%PYTHON_EXE%" (
  echo ERROR: Embedded runtime is missing: %PYTHON_EXE%
  pause
  exit /b 1
)
"%PYTHON_EXE%" app\launcher.py
set EXITCODE=%ERRORLEVEL%
echo Launcher exited with code %EXITCODE%
pause
exit /b %EXITCODE%
