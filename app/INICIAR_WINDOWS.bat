@echo off
chcp 65001 >nul
cd /d "%~dp0"
py -3 --version >nul 2>&1
if errorlevel 1 (
 echo Instale Python 3 e marque Add Python to PATH
 pause
 exit /b 1
)
if not exist ".venv\Scripts\python.exe" py -3 -m venv .venv
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (pause & exit /b 1)
start "" "http://127.0.0.1:8765/controle"
".venv\Scripts\python.exe" servidor.py
pause
