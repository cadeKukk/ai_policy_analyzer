@echo off
REM Startup script for AI Policy Analyzer on Windows

echo === AI Policy Analyzer Startup ===

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH. Please install Python 3 to run this application.
    pause
    exit /b 1
)

REM Check if virtual environment exists, if not create it
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo Error: Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to activate virtual environment.
    pause
    exit /b 1
)

REM Install requirements if needed
echo Installing dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install dependencies.
    pause
    exit /b 1
)

REM Run the demo
echo Starting AI Policy Analyzer...
echo Once the server starts, open your web browser and go to: http://localhost:5000
python run_demo.py

REM Deactivate virtual environment on exit
call deactivate

pause 