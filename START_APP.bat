@echo off
echo ============================================
echo FoodMind AI - Starting Application
echo ============================================
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from https://python.org
    pause
    exit /b 1
)
echo.

echo Checking required packages...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo WARNING: Streamlit not installed!
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install packages
        pause
        exit /b 1
    )
)
echo.

echo ============================================
echo Starting FoodMind AI...
echo ============================================
echo.
echo The app will open in your browser automatically.
echo If not, open: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server.
echo ============================================
echo.

python -m streamlit run app.py

pause
