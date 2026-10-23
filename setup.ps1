# FoodMind AI - Windows Setup Script
# This script automates the setup process for Windows users

Write-Host "========================================" -ForegroundColor Green
Write-Host "   FoodMind AI - Installation Script   " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from python.org" -ForegroundColor Red
    exit 1
}

Write-Host "Found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow

if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Skipping..." -ForegroundColor Cyan
} else {
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Virtual environment created successfully!" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Note: If you see execution policy errors, run:" -ForegroundColor Cyan
    Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Cyan
    Write-Host ""
}

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Check for .env file
Write-Host "Checking configuration..." -ForegroundColor Yellow

if (Test-Path ".env") {
    Write-Host ".env file found" -ForegroundColor Green
} else {
    Write-Host ".env file not found (optional for AI features)" -ForegroundColor Cyan
    Write-Host "To enable AI Assistant:" -ForegroundColor Cyan
    Write-Host "1. Copy .env.example to .env" -ForegroundColor Cyan
    Write-Host "2. Add your Gemini API key" -ForegroundColor Cyan
}
Write-Host ""

# Installation complete
Write-Host "========================================" -ForegroundColor Green
Write-Host "   Installation Complete!              " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To start FoodMind AI, run:" -ForegroundColor Yellow
Write-Host "  streamlit run app.py" -ForegroundColor White
Write-Host ""
Write-Host "The application will open in your browser at:" -ForegroundColor Yellow
Write-Host "  http://localhost:8501" -ForegroundColor White
Write-Host ""
Write-Host "Enjoy FoodMind AI! 🥗" -ForegroundColor Green
