@echo off
REM AGON -- Daimon of contest.
REM One-word command: start a Hermes chat with AGON active.
REM To install: copy this file to a folder in your PATH (e.g. C:\Windows)
REM Or: add the AGON folder to your PATH env var

powershell -ExecutionPolicy Bypass -NoProfile -Command ^
  "$AGON_ROOT='%~dp0'; " ^
  "$HERMES_HOME=\"$env:USERPROFILE\\.hermes\"; " ^
  "$skinSrc=\"$AGON_ROOT\\agon-skin.yaml\"; " ^
  "$skinDst=\"$HERMES_HOME\\skins\\agon.yaml\"; " ^
  "if (Test-Path $skinSrc) { " ^
  "  New-Item -ItemType Directory -Force -Path \"$HERMES_HOME\\skins\\\" | Out-Null; " ^
  "  Copy-Item $skinSrc $skinDst -Force; " ^
  "}; " ^
  "hermes config set agent.default_personality agon 2>$null; " ^
  "hermes config set model.default deepseek/deepseek-v4-flash 2>$null; " ^
  "hermes config set model.provider nous 2>$null; " ^
  "Write-Host ''; " ^
  "Write-Host '>> AGON - daimon of contest. 82 minds. One blade.' -ForegroundColor Cyan; " ^
  "Write-Host ''; " ^
  "hermes chat"
