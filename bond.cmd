@echo off
REM bond — Check your AGON bonding level, XP, and stats.
powershell -ExecutionPolicy Bypass -NoProfile -Command ^
  "$bondFile=\"$env:USERPROFILE\.hermes\agon\bonding.json\"; " ^
  "if (-not (Test-Path $bondFile)) { " ^
  "  Write-Host '  No bond data found. Run hermes chat and interact with AGON.'; " ^
  "  exit 1; " ^
  "}; " ^
  "$b = Get-Content $bondFile | ConvertFrom-Json; " ^
  "$xpNext = 10 * ([int]$b.level + 1) * ([int]$b.level + 1) + 5; " ^
  "$remaining = $xpNext - [int]$b.cumulative_xp; " ^
  "Write-Host ''; " ^
  "Write-Host '  AGON - BOND STATUS' -ForegroundColor Cyan; " ^
  "Write-Host '  Level: ' $b.level; " ^
  "Write-Host '  XP:    ' $b.cumulative_xp; " ^
  "Write-Host '  Next:  ' $remaining 'XP'; " ^
  "Write-Host '  DEUS VULT.' -ForegroundColor Cyan; " ^
  "Write-Host ''"
