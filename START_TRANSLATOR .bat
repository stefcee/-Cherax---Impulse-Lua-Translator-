@echo off
title Impulse Language Translator - Starting...
echo ========================================
echo  Impulse Language Translator by Stefc3
echo ========================================
echo.
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo.
echo Checking dependencies...
pip show deep-translator >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install deep-translator requests
)

echo.
echo Starting translator...
python ImpulseLanguageTranslator.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start translator!
    pause
)
