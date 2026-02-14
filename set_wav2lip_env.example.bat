@echo off
setlocal
cd /d %~dp0

rem Configure these two paths before running:
set W2L_REPO_DIR=%~dp0Wav2Lip
set W2L_CHECKPOINT_PATH=%~dp0Wav2Lip\checkpoints\wav2lip.pth

rem Optional tuning:
set W2L_FACE_DET_BATCH=16
set W2L_BATCH=64
set W2L_PADS=0 10 0 0
set W2L_RESIZE_FACTOR=1
set W2L_NOSMOOTH=0
set W2L_USE_BOX=0

call only_gpu.bat
