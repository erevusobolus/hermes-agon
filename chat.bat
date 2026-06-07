@echo off
title AGON — Web Chat
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0chat.ps1"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Script exited with code %ERRORLEVEL%. Press any key to close...
    pause > nul
)
