@echo off
cd /d "%~dp0"
echo Starting OpenCLIP Photo Search...
python -m uvicorn web_app:app --host 127.0.0.1 --port 8000
pause
