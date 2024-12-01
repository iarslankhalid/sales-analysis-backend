#!/bin/bash

# Check if Python 3.9+ is installed
PYTHON_VERSION=$(python3 --version 2>&1)

if [[ $? -ne 0 ]]; then
    echo "Python is not installed or not in the PATH."
    echo "Please install Python 3.9 or later."
    exit 1
fi

echo "Detected Python version: $PYTHON_VERSION"

# Extract version number
VERSION=$(echo $PYTHON_VERSION | awk '{print $2}')
MAJOR=$(echo $VERSION | cut -d. -f1)
MINOR=$(echo $VERSION | cut -d. -f2)

# Check if version is >= 3.9
if [[ $MAJOR -lt 3 || ( $MAJOR -eq 3 && $MINOR -lt 9 ) ]]; then
    echo "Python 3.9 or later is required. Your version is $VERSION."
    exit 1
fi

echo "Python 3.9+ detected, proceeding with setup..."

# Check if .env file exists
if [[ ! -f .env ]]; then
    echo ".env file not found. Please create a .env file."
    exit 1
fi

# Check if .env contains necessary variables
if ! grep -iq "XAI_API_KEY" .env; then
    echo "XAI_API_KEY not found in .env."
    exit 1
fi

if ! grep -iq "BASE_URL" .env; then
    echo "BASE_URL not found in .env."
    exit 1
fi

if ! grep -iq "FILE_PATH" .env; then
    echo "FILE_PATH not found in .env."
    exit 1
fi

echo ".env file is valid. Proceeding with virtual environment setup..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing required packages..."
pip install -r requirements.txt

# Install necessary dependencies for Uvicorn and Flask-ASGI
echo "Installing Uvicorn and Flask-ASGI..."
pip install uvicorn flask-asgi

# Run the Flask app with Uvicorn
echo "Running Flask app with Uvicorn..."
uvicorn app.main:app --reload
