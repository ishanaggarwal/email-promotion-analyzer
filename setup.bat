@echo off
REM Email Promotion Analyzer - Quick Setup Script for Windows
REM This script helps you set up the Email Promotion Analyzer quickly

echo ================================================
echo   Email Promotion Analyzer - Setup Script
echo ================================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [31mPython 3 is not installed. Please install Python 3.8 or higher.[0m
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [32mFound Python %PYTHON_VERSION%[0m

REM Check if we're in the right directory
if not exist "README.md" (
    echo [31mPlease run this script from the project root directory[0m
    exit /b 1
)

REM Create virtual environment
echo.
echo Setting up virtual environment...
if not exist "venv" (
    python -m venv venv
    echo [32mVirtual environment created[0m
) else (
    echo [33mVirtual environment already exists[0m
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
cd backend
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q
echo [32mDependencies installed[0m

REM Create .env file if it doesn't exist
echo.
cd ..
if not exist ".env" (
    copy .env.example .env
    echo [32mCreated .env file from template[0m
    echo [33mPlease edit .env and add your API keys[0m
) else (
    echo [33m.env file already exists[0m
)

REM Check for credentials.json
echo.
if not exist "backend\credentials.json" (
    echo [33mGmail credentials not found[0m
    echo    To enable Gmail integration:
    echo    1. Go to https://console.cloud.google.com/
    echo    2. Create OAuth credentials for Gmail API
    echo    3. Download credentials.json to backend\ directory
) else (
    echo [32mGmail credentials found[0m
)

REM Summary
echo.
echo ================================================
echo   Setup Complete! 🎉
echo ================================================
echo.
echo Next steps:
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate
echo.
echo   2. Edit .env file with your API keys
echo.
echo   3. Run the application:
echo      cd backend
echo      python app.py
echo.
echo   4. Access the API at http://localhost:5000
echo.
echo For more information, see README.md
echo.

pause
exit /b 0
