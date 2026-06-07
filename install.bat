@echo off
title AGON — Patch Installer
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0install.ps1"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Script exited with code %ERRORLEVEL%. Press any key to close...
    pause > nul
)
