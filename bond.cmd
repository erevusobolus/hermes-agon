@echo off
REM bond — Check your AGON bonding level, XP, and stats (via programmable audit)
powershell -ExecutionPolicy Bypass -NoProfile -Command ^
  "$audit=\"$env:USERPROFILE\\.hermes\\agon\\bond-audit.py\"; " ^
  "$bonding=\"$env:USERPROFILE\\.hermes\\agon\\bonding.py\"; " ^
  "if (-not (Test-Path $audit)) { " ^
  "  Write-Host '  AGON audit script not found. Run install.ps1 first.'; " ^
  "  exit 1; " ^
  "}; " ^
  "python $audit > $null 2>&1; " ^
  "if (Test-Path $bonding) { " ^
  "  Set-Location \"$env:USERPROFILE\\.hermes\\agon\"; " ^
  "  python -c \"from bonding import format_level, load_bonding; print(format_level(load_bonding()))\"; " ^
  "} else { " ^
  "  $b = Get-Content \"$env:USERPROFILE\\.hermes\\agon\\bonding.json\" | ConvertFrom-Json; " ^
  "  $xpNext = 10 * ([int]$b.level + 1) * ([int]$b.level + 1) + 5; " ^
  "  $remaining = $xpNext - [int]$b.cumulative_xp; " ^
  "  Write-Host ''; " ^
  "  Write-Host '  AGON - BOND STATUS' -ForegroundColor Cyan; " ^
  "  Write-Host '  Level: ' $b.level; " ^
  "  Write-Host '  XP:    ' $b.cumulative_xp; " ^
  "  Write-Host '  Next:  ' $remaining 'XP'; " ^
  "  Write-Host '  DEUS VULT.' -ForegroundColor Cyan; " ^
  "  Write-Host ''; " ^
  "}"
