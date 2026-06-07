<#
.SYNOPSIS
    AGON PowerShell init — dot-source this in your PowerShell profile.
.DESCRIPTION
    Add to profile: . C:\path\to\agon\init.ps1
    On every PowerShell start: checks Hermes, ensures AGON is default,
    shows the AGON banner once per session.
.NOTES
    Profile path: $PROFILE (typically ~\Documents\PowerShell\Microsoft.PowerShell_profile.ps1)
#>

$AGON_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check Hermes is installed
if (Get-Command "hermes" -ErrorAction SilentlyContinue) {
    # Ensure AGON is default personality
    & hermes config set agent.default_personality agon 2>$null | Out-Null

    # Show banner once per session
    if (-not $env:AGON_INIT_DONE) {
        Write-Host ""
        Write-Host "  ⚔ AGON - daimon of contest. 82 minds. One blade." -ForegroundColor Cyan
        Write-Host "  hermes chat  |  .\agon.cmd  |  .\chat.bat" -ForegroundColor Cyan
        Write-Host ""
        $env:AGON_INIT_DONE = "1"
    }
}
