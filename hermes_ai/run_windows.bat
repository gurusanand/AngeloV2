@echo off
REM Hermes Config Generator - Windows Run Script

echo ========================================
echo Starting Hermes Config Generator
echo ========================================
echo.

REM Check if OpenAI API key is set
if "%OPENAI_API_KEY%"=="" (
    echo WARNING: OPENAI_API_KEY environment variable is not set
    echo.
    echo Please set your OpenAI API key:
    echo In PowerShell:
    echo    $env:OPENAI_API_KEY="your-api-key-here"
    echo.
    echo Or in Command Prompt:
    echo    set OPENAI_API_KEY=your-api-key-here
    echo.
    echo Press any key to continue anyway, or Ctrl+C to exit
    pause
)

REM Start Streamlit
echo Starting application...
echo.
echo The application will open in your default browser
echo If it doesn't open automatically, navigate to:
echo    http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

"..\.venv\Scripts\streamlit.exe" run app_v2.py --server.port 8501 --server.address localhost

pause
