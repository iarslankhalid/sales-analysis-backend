@echo off
SET PYTHON_EXE=python

:: Check if Python 3.9+ is installed
%PYTHON_EXE% --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in the PATH.
    echo Please install Python 3.9 or later.
    pause
    exit /b
)

:: Check the Python version
for /f "delims=" %%i in ('%PYTHON_EXE% --version 2^>nul') do set PYTHON_VERSION=%%i
echo Detected %PYTHON_VERSION%

:: Extract version number
for /f "tokens=2 delims= " %%a in ("%PYTHON_VERSION%") do set VERSION=%%a
for /f "tokens=1 delims=." %%a in ("%VERSION%") do set MAJOR=%%a
for /f "tokens=2 delims=." %%a in ("%VERSION%") do set MINOR=%%a

:: Check if version is >= 3.9
IF %MAJOR% LSS 3 (
    echo Python 3.9 or later is required. Your version is %VERSION%.
    pause
    exit /b
)
IF %MAJOR% == 3 IF %MINOR% LSS 9 (
    echo Python 3.9 or later is required. Your version is %VERSION%.
    pause
    exit /b
)

echo Python 3.9+ detected, proceeding with setup...

:: Check if .env file exists
IF NOT EXIST .env (
    echo .env file not found. Please create a .env file.
    pause
    exit /b
)

:: Check if .env contains necessary variables
findstr /i "XAI_API_KEY" .env >nul
IF %ERRORLEVEL% NEQ 0 (
    echo XAI_API_KEY not found in .env.
    pause
    exit /b
)

findstr /i "BASE_URL" .env >nul
IF %ERRORLEVEL% NEQ 0 (
    echo BASE_URL not found in .env.
    pause
    exit /b
)

findstr /i "FILE_PATH" .env >nul
IF %ERRORLEVEL% NEQ 0 (
    echo FILE_PATH not found in .env.
    pause
    exit /b
)

echo .env file is valid. Proceeding with virtual environment setup...

:: Create virtual environment
echo Creating virtual environment...
%PYTHON_EXE% -m venv venv

:: Activate virtual environment
call venv\Scripts\activate

echo Upgrading pip...
%PYTHON_EXE% -m pip install --upgrade pip

:: Install requirements
echo Installing required packages...
pip install -r requirements.txt


:: Run the Fastapi app with Uvicorn
echo Running Fastapi app with Uvicorn...
uvicorn app.main:app --reload

pause
