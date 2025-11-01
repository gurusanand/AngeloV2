@echo off
REM Hermes Config Generator - Windows Installation Script
REM This script installs all dependencies and sets up the application

echo ========================================
echo Hermes Config Generator Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/5] Python found
python --version
echo.

REM Check if pip is available
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo [2/5] pip found
echo.

REM Upgrade pip
echo [3/5] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo pip upgraded successfully
echo.

REM Install required packages
echo [4/5] Installing required packages...
echo This may take a few minutes...
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install required packages
    pause
    exit /b 1
)
echo All packages installed successfully
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Git is not installed
    echo Git integration features will not work
    echo You can install Git from https://git-scm.com/download/win
    echo.
) else (
    echo [5/5] Git found
    git --version
    echo.
)

REM Create config directory
if not exist "config_repo" mkdir config_repo
echo Configuration repository directory created
echo.

REM Check for OpenAI API key
if "%OPENAI_API_KEY%"=="" (
    echo ========================================
    echo IMPORTANT: OpenAI API Key Required
    echo ========================================
    echo.
    echo The application requires an OpenAI API key to function.
    echo.
    echo To set your API key:
    echo 1. Get your API key from https://platform.openai.com/api-keys
    echo 2. Run this command in PowerShell:
    echo    $env:OPENAI_API_KEY="your-api-key-here"
    echo.
    echo Or in Command Prompt:
    echo    set OPENAI_API_KEY=your-api-key-here
    echo.
    echo For permanent setup, add it to Windows Environment Variables
    echo.
) else (
    echo OpenAI API key detected
    echo.
)

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To start the application, run:
echo    run_windows.bat
echo.
echo Or manually:
echo    streamlit run app.py
echo.
pause
