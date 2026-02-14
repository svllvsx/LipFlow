@echo off
setlocal
cd /d %~dp0
set W2L_USE_GPU=1
if "%W2L_REPO_DIR%"=="" set W2L_REPO_DIR=%~dp0Wav2Lip
if "%W2L_CHECKPOINT_PATH%"=="" (
  if exist "%~dp0Wav2Lip\checkpoints\wav2lip.pth" (
    set W2L_CHECKPOINT_PATH=%~dp0Wav2Lip\checkpoints\wav2lip.pth
  ) else if exist "%~dp0Wav2Lip\checkpoints\wav2lip_gan.pth" (
    set W2L_CHECKPOINT_PATH=%~dp0Wav2Lip\checkpoints\wav2lip_gan.pth
  )
)
if "%W2L_USE_BOX%"=="" set W2L_USE_BOX=0
set PYTHON_EXE=app\python\pythonw.exe
if not exist "%PYTHON_EXE%" (
  echo ERROR: Embedded runtime is missing: %PYTHON_EXE%
  echo This portable build is incomplete.
  exit /b 1
)
start "" "%PYTHON_EXE%" app\launcher.py
exit /b 0
