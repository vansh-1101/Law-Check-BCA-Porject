@echo off
echo ========================================
echo Legal Consultation Platform - Setup
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate
echo ✓ Virtual environment activated
echo.

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip
echo ✓ Pip upgraded
echo.

echo Step 4: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo Step 5: Creating .env file...
if not exist .env (
    copy .env.example .env
    echo ✓ .env file created - Please edit it with your settings
) else (
    echo .env file already exists
)
echo.

echo Step 6: Creating instance directory...
if not exist instance mkdir instance
echo ✓ Instance directory created
echo.

echo Step 7: Creating uploads directory...
if not exist app\static\uploads mkdir app\static\uploads
echo ✓ Uploads directory created
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your configuration
echo 2. Run: python run.py
echo 3. Open browser: http://127.0.0.1:5000
echo.
echo To activate virtual environment later:
echo   venv\Scripts\activate
echo.
pause
