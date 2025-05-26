@echo off
echo 🏠 Apt-Hunter Web Interface Launcher
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo 💡 Please install Python 3.6+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python is installed
echo.

REM Run the launcher script
echo 🚀 Starting Apt-Hunter Web Interface...
python start_web_interface.py

pause 