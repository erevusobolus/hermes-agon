<#
.SYNOPSIS
    AGON Web Chat - one-click launcher for Windows.
.DESCRIPTION
    Checks Python + Hermes + deps, installs what's missing, sets AGON config,
    then launches the WebUI via the WebUI's native start.ps1.
    Double-click chat.bat instead of this file directly.
.NOTES
    Uses the WebUI's start.ps1 to launch server.py (bootstrap.py refuses
    to run on Windows: it checks platform.system() == 'Windows' and bails).
#>

# --- Force strict mode ----------------------------------------------------
$ErrorActionPreference = 'Stop'

# --- Wrap everything so errors always pause -----------------------------
try {

$AGON_ROOT = $PSScriptRoot
if (-not $AGON_ROOT) {
    Write-Host ""
    Write-Host "  [X] Could not determine script directory." -ForegroundColor Red
    Write-Host "      Instead, open a terminal here and run:" -ForegroundColor Yellow
    Write-Host "         powershell -ExecutionPolicy Bypass -File .\chat.ps1" -ForegroundColor White
    Write-Host "      Or double-click chat.bat" -ForegroundColor White
    Write-Host ""
    pause; exit 1
}

$WEBUI_DIR   = $AGON_ROOT + "\WebUI"
$HERMES_HOME = $env:USERPROFILE + "\.hermes"

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  AGON - WEB CHAT" -ForegroundColor Cyan
Write-Host "  Opens in your browser. Like ChatGPT." -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# --- 1. Validate paths --------------------------------------------------
if (-not (Test-Path $WEBUI_DIR -PathType Container)) {
    Write-Host "  [X] WebUI directory not found at:" -ForegroundColor Red
    Write-Host "      $WEBUI_DIR" -ForegroundColor White
    Write-Host "      Make sure the 'WebUI' folder is present next to this script." -ForegroundColor Yellow
    pause; exit 1
}
$startPs1 = $WEBUI_DIR + "\start.ps1"
if (-not (Test-Path $startPs1)) {
    Write-Host "  [X] start.ps1 not found in WebUI directory." -ForegroundColor Red
    Write-Host "      The WebUI folder may be incomplete." -ForegroundColor Yellow
    pause; exit 1
}

$ok = 0

# --- 2. Python -----------------------------------------------------------
$pythonCmd = Get-Command "python" -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "  [X] Python not found" -ForegroundColor Red
    Write-Host "      1. Download from: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "      2. Check 'Add Python to PATH' during install" -ForegroundColor White
    Write-Host "      3. Restart terminal, then run this again" -ForegroundColor White
    pause; exit 1
}
$pyVer = & python --version 2>&1
Write-Host "  [ok] $pyVer" -ForegroundColor Green; $ok++

# --- 3. Hermes Agent -----------------------------------------------------
$hermesCmd = Get-Command "hermes" -ErrorAction SilentlyContinue
if (-not $hermesCmd) {
    Write-Host "  [~] Hermes Agent not found - installing..." -ForegroundColor Yellow
    $installOk = $false

    # Try pip
    $pipResult = & pip install hermes-agent 2>&1
    $hermesCmd = Get-Command "hermes" -ErrorAction SilentlyContinue
    if ($hermesCmd) { $installOk = $true }

    # Try winget fallback
    if (-not $installOk) {
        Write-Host "      pip install failed - trying winget..." -ForegroundColor Yellow
        $wgResult = & winget install hermes-agent 2>&1
        Start-Sleep -Seconds 2
        $hermesCmd = Get-Command "hermes" -ErrorAction SilentlyContinue
        if ($hermesCmd) { $installOk = $true }
    }

    if ($installOk) {
        Write-Host "  [ok] Hermes Agent installed" -ForegroundColor Green; $ok++
    } else {
        Write-Host "  [X] Could not install Hermes automatically" -ForegroundColor Red
        Write-Host "      Try manually:" -ForegroundColor White
        Write-Host "        pip install hermes-agent" -ForegroundColor White
        pause; exit 1
    }
} else {
    $hVer = & hermes --version 2>&1 | Select-Object -First 1
    Write-Host "  [ok] Hermes $hVer" -ForegroundColor Green; $ok++
}

# --- 4. AGON Config ------------------------------------------------------
Write-Host ""
Write-Host "  -- AGON Configuration ---------------------" -ForegroundColor DarkCyan
& hermes config set model.default "deepseek/deepseek-v4-flash" 2>$null
& hermes config set model.provider "nous" 2>$null
Write-Host "     Model: deepseek/deepseek-v4-flash (Nous Portal)" -ForegroundColor White

$skinDir = $HERMES_HOME + "\skins"
$skinDst = $skinDir + "\agon.yaml"
$skinSrc = $AGON_ROOT + "\agon-skin.yaml"
if (Test-Path $skinSrc) {
    New-Item -ItemType Directory -Force -Path $skinDir | Out-Null
    Copy-Item $skinSrc $skinDst -Force
    Write-Host "     Skin:  AGON bronze+gold" -ForegroundColor White
} else {
    Write-Host "     Skin:  agon-skin.yaml not found (optional)" -ForegroundColor DarkYellow
}

# --- 5. WebUI Python deps -----------------------------------------------
Write-Host ""
Write-Host "  -- WebUI Dependencies ---------------------" -ForegroundColor DarkCyan
Push-Location $WEBUI_DIR
try {
    # Bypass $ErrorActionPreference for pip (benign stderr warnings like
    # "Ignoring invalid distribution" should not be fatal)
    $oldEAP = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    & pip install pyyaml cryptography -q 2>&1 | Out-Null
    $ErrorActionPreference = $oldEAP
    Write-Host "     Python packages ready" -ForegroundColor White
} finally {
    $ErrorActionPreference = 'Stop'
    Pop-Location
}

# --- 6. Set env vars -----------------------------------------------------
$env:HERMES_WEBUI_DEFAULT_MODEL = "deepseek/deepseek-v4-flash"
$env:HERMES_WEBUI_HOST          = "127.0.0.1"
$env:HERMES_WEBUI_PORT          = "8787"

# --- 7. Summary ----------------------------------------------------------
Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  All checks passed! Launching WebUI..." -ForegroundColor Cyan
Write-Host "  Opening http://localhost:8787 in your browser." -ForegroundColor Cyan
Write-Host "  Close this window to stop the server." -ForegroundColor Cyan
Write-Host ""
Write-Host "  DEUS VULT." -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# --- 8. Launch browser + server -----------------------------------------
Start-Process "http://localhost:8787"

# Launch via the WebUI's native start.ps1.
# Use Invoke-Expression inside a separate PowerShell process so start.ps1's
# internal 'exit' calls don't kill this script.
$startCmd = "-ExecutionPolicy Bypass -File `"$startPs1`""
Start-Process -Wait -NoNewWindow powershell -ArgumentList $startCmd

# --- 9. Done -------------------------------------------------------------
Write-Host ""
Write-Host "  Server stopped. Press any key to close..." -ForegroundColor Cyan
pause
exit 0

} catch {
    Write-Host ""
    Write-Host "  [X] UNEXPECTED ERROR" -ForegroundColor Red
    Write-Host "      $($_.Exception.Message)" -ForegroundColor White
    Write-Host "      At line $($_.InvocationInfo.ScriptLineNumber)" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  Press any key to close..." -ForegroundColor Cyan
    pause
    exit 1
}
