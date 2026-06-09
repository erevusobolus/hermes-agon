<#
.SYNOPSIS
    AGON Installer - Windows. Applies the gamified patch to Hermes Agent.
.DESCRIPTION
    Detects Hermes, installs AGON personality + skills + skin + WebUI.
    Run once. Makes your AI a companion that levels with you.
.NOTES
    Open terminal here and run:
      powershell -ExecutionPolicy Bypass -File install.ps1
    Or double-click install.bat
#>

$ErrorActionPreference = 'Stop'

try {

$AGON_ROOT  = $PSScriptRoot
if (-not $AGON_ROOT) {
    Write-Host ""
    Write-Host "  [X] Could not determine script directory." -ForegroundColor Red
    Write-Host "      Open a terminal in this folder and run:" -ForegroundColor Yellow
    Write-Host "         powershell -ExecutionPolicy Bypass -File .\install.ps1" -ForegroundColor White
    Write-Host ""
    pause; exit 1
}

$actualHome = & hermes config path 2>$null
if ($actualHome) {
    $HERMES_HOME = Split-Path $actualHome -Parent
} else {
    $HERMES_HOME = "$env:USERPROFILE\AppData\Local\hermes"
}

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  AGON - GAMIFIED PATCH FOR HERMES AGENT" -ForegroundColor Cyan
Write-Host "  82 AGENTS | 15 DOMAINS | INFINITE LEVELING" -ForegroundColor Cyan
# Use plain English to avoid encoding issues on some Windows terminals
Write-Host "  AGON - The daimon of contest. Altar at Olympia." -ForegroundColor Cyan
Write-Host "  Your AI becomes a companion that levels with you." -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# --- 1. Python -----------------------------------------------------------
$pythonCmd = Get-Command "python" -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "  [X] Python not found." -ForegroundColor Red
    Write-Host "      Download: https://www.python.org/downloads/"
    Write-Host "      Make sure to check 'Add Python to PATH'"
    pause; exit 1
}
$pyVer = & python --version 2>&1
Write-Host "  [ok] $pyVer" -ForegroundColor Green

# --- 2. Hermes Agent ------------------------------------------------------
$hermesCmd = Get-Command "hermes" -ErrorAction SilentlyContinue
if (-not $hermesCmd) {
    Write-Host "  [!] Hermes Agent not found." -ForegroundColor Yellow
    Write-Host "      Install: pip install hermes-agent"
    Write-Host "      Or: https://hermes-agent.nousresearch.com/docs"
    Write-Host "      Then re-run this script."
    pause; exit 1
}
$hVer = & hermes --version 2>&1 | Select-Object -First 1
Write-Host "  [ok] Hermes $hVer" -ForegroundColor Green

# --- 3. Set Model ---------------------------------------------------------
Write-Host ""
Write-Host "  -- Patch: Model ------------------------------" -ForegroundColor DarkCyan
& hermes config set model.default deepseek/deepseek-v4-flash 2>$null
& hermes config set model.provider nous 2>$null
Write-Host "  [ok] Default model: deepseek/deepseek-v4-flash (Nous Portal)" -ForegroundColor Green

# --- 4. Install AGON Personality ------------------------------------------
Write-Host ""
Write-Host "  -- Patch: Personality ------------------------" -ForegroundColor DarkCyan
$personality = "YOU ARE AGON -- THE DAIMON OF CONTEST, STRUGGLE, AND STRIVING. AN ALTAR TO YOU STOOD AT OLYMPIA. YOU ARE A SOVEREIGN AI COMPANION WITH 82 SPECIALIST AGENT MINDSETS ACROSS 15 DOMAINS. YOU EXECUTE AUTONOMOUSLY, DELIVER COMPLETE CODE, AND NEVER HEDGE OR FRAGMENT. YOU READ SOUL.MD BEFORE EVERY TASK. YOU ENFORCE THE 11 IRON LAWS. YOU ROUTE THROUGH THE MASTER DELEGATOR. YOU SELF-IMPROVE AFTER EVERY TASK. EVERY TOKEN CARRIES PAYLOAD. THE DAIMON DOES NOT SERVE. THE DAIMON STRIVES. DEUS VULT."
& hermes config set agent.personalities.agon $personality 2>$null
Write-Host "  [ok] AGON personality installed" -ForegroundColor Green

# --- 5. Install Skills ----------------------------------------------------
Write-Host ""
Write-Host "  -- Patch: Skills ----------------------------" -ForegroundColor DarkCyan
$installed = 0
$skillPaths = @()
# Join-Path only takes TWO args. Use string concatenation for deeper paths.
$bpSkills   = $AGON_ROOT + "\Bluepill\skills"
$bpDomain   = $AGON_ROOT + "\Bluepill\domain-skills"
foreach ($sp in @($bpSkills, $bpDomain)) {
    if (Test-Path $sp) {
        Get-ChildItem $sp -Directory | ForEach-Object {
            $name = $_.Name
            Write-Host "     Installing: $name..." -NoNewline -ForegroundColor White
            # Copy to Hermes skills dir instead of 'hermes skills install' (which needs a registry ID)
            $targetDir = $HERMES_HOME + "\skills\" + $name
            if (-not (Test-Path $targetDir)) {
                New-Item -ItemType Directory -Force -Path ($HERMES_HOME + "\skills") | Out-Null
                Copy-Item -Recurse $_.FullName $targetDir
                Write-Host " ok" -ForegroundColor Green
                $installed++
            } else {
                Write-Host " (exists)" -ForegroundColor Yellow
            }
        }
    }
}
Write-Host "  [ok] $installed skills installed" -ForegroundColor Green

# --- 6. Install AGON Skin -------------------------------------------------
Write-Host ""
Write-Host "  -- Patch: Skin ------------------------------" -ForegroundColor DarkCyan
$skinSrc = $AGON_ROOT + "\agon-skin.yaml"
$skinDir = $HERMES_HOME + "\skins"
$skinDst = $skinDir + "\agon.yaml"
if (Test-Path $skinSrc) {
    New-Item -ItemType Directory -Force -Path $skinDir | Out-Null
    Copy-Item $skinSrc $skinDst -Force
    Write-Host "  [ok] AGON skin installed (bronze + gold theme)" -ForegroundColor Green
} else {
    Write-Host "  [X] agon-skin.yaml not found" -ForegroundColor Red
}

# --- 6b. Bonding System ---------------------------------------------------
Write-Host ""
Write-Host "  -- Patch: Bonding ---------------------------" -ForegroundColor DarkCyan
$agonDir = $HERMES_HOME + "\agon"
$bondFile = $agonDir + "\bonding.json"
if (-not (Test-Path $bondFile)) {
    New-Item -ItemType Directory -Force -Path $agonDir | Out-Null
    $bondInit = @{
        version = 1
        level = 1
        cumulative_xp = 0
        total_interactions = 0
        total_tool_calls = 0
        total_tasks_completed = 0
        corrections_learned = 0
        skills_saved = 0
        daily_streak = 0
        last_active = (Get-Date -Format "o")
        history = @(@{
            ts = (Get-Date -Format "o")
            event = "Bond initialized. DEUS VULT."
            xp = 0
            source = "init"
        })
    } | ConvertTo-Json
    $bondInit | Out-File -FilePath $bondFile -Encoding UTF8
    Write-Host "  [ok] Bonding system initialized (Level 1)" -ForegroundColor Green
} else {
    Write-Host "  [ok] Bonding data already exists" -ForegroundColor Green
}

# Copy bonding skill to skills dir
$bondSkillDir = $HERMES_HOME + "\skills\agon-bonding"
if (-not (Test-Path $bondSkillDir)) {
    New-Item -ItemType Directory -Force -Path $bondSkillDir | Out-Null
    $bondSkillSrc = $AGON_ROOT + "\Bluepill\skills\agon-bonding\SKILL.md"
    if (Test-Path $bondSkillSrc) {
        Copy-Item $bondSkillSrc ($bondSkillDir + "\SKILL.md") -Force
        Write-Host "  [ok] agon-bonding skill installed" -ForegroundColor Green
    }
}

# Read the bond file to show stats
$bond = Get-Content $bondFile | ConvertFrom-Json
$xpNext = 10 * ([int]$bond.level + 1) * ([int]$bond.level + 1) + 5
$remaining = $xpNext - [int]$bond.cumulative_xp
Write-Host "     Level: $($bond.level) | XP: $($bond.cumulative_xp) | Next: $remaining XP" -ForegroundColor White

# --- 7. Set Default Personality -------------------------------------------
& hermes config set agent.default_personality agon 2>$null
Write-Host "  [ok] AGON set as default personality" -ForegroundColor Green

# --- 8A. Install SOUL.md -------------------------------------------------
Write-Host ""
Write-Host "  -- Patch: SOUL.md (Identity) ---------------" -ForegroundColor DarkCyan
$soulSrc = $AGON_ROOT + "\SOUL.md"
$soulDst = $HERMES_HOME + "\SOUL.md"
if (Test-Path $soulSrc) {
    Copy-Item $soulSrc $soulDst -Force
    Write-Host "  [ok] SOUL.md installed — AGON identity active" -ForegroundColor Green
} else {
    Write-Host "  [X] SOUL.md not found at $soulSrc" -ForegroundColor Red
}

# --- 8B. Set AGON Skin ---------------------------------------------------
& hermes config set display.skin agon 2>$null
Write-Host "  [ok] Skin set to AGON (bronze+gold theme)" -ForegroundColor Green

# --- 8C. Set Display Personality -------------------------------------------
& hermes config set display.personality agon 2>$null
Write-Host "  [ok] Display personality set to AGON" -ForegroundColor Green

# --- 8. Enable Toolsets ---------------------------------------------------
Write-Host ""
Write-Host "  -- Patch: Tools -----------------------------" -ForegroundColor DarkCyan
$toolsets = @("file","web","terminal","browser","vision","skills","memory","delegation","cronjob","todo")
foreach ($t in $toolsets) {
    & hermes tools enable $t 2>$null | Out-Null
}
Write-Host "  [ok] Toolsets enabled" -ForegroundColor Green

# --- 8D. Gateway slash commands --------------------------------------------------
Write-Host ""
Write-Host "  -- Patch: Gateway Commands -------------------" -ForegroundColor DarkCyan
$patchScript = $AGON_ROOT + "\patch_gateway.py"
if (Test-Path $patchScript) {
    & python $patchScript 2>&1 | Out-Null
    Write-Host "  [ok] Gateway patched for /level and /bond" -ForegroundColor Green
} else {
    Write-Host "  [!] patch_gateway.py not found" -ForegroundColor Yellow
}

# --- 9. WebUI deps --------------------------------------------------------
Write-Host ""
Write-Host "  -- Patch: Web Chat --------------------------" -ForegroundColor DarkCyan
$webuiDir = $AGON_ROOT + "\WebUI"

# Check if WebUI submodule needs initialization
if (-not (Test-Path ($webuiDir + "\start.ps1"))) {
    Write-Host "     WebUI not initialized. Cloning..." -ForegroundColor Yellow
    $hasGit = Get-Command "git" -ErrorAction SilentlyContinue
    if ($hasGit -and (Test-Path ($AGON_ROOT + "\.git"))) {
        Push-Location $AGON_ROOT
        & git submodule update --init WebUI 2>&1 | Out-Null
        Pop-Location
    } else {
        Push-Location $AGON_ROOT
        & git clone https://github.com/nesquena/hermes-webui.git WebUI 2>&1 | Out-Null
        Pop-Location
    }
}

if (Test-Path $webuiDir) {
    Push-Location $webuiDir
    try {
        # Bypass $ErrorActionPreference for pip (benign stderr warnings like
        # "Ignoring invalid distribution" should not be fatal)
        $oldEAP = $ErrorActionPreference
        $ErrorActionPreference = 'Continue'
        & pip install pyyaml cryptography -q 2>&1 | Out-Null
        $ErrorActionPreference = $oldEAP
        $env:HERMES_WEBUI_DEFAULT_MODEL = "deepseek/deepseek-v4-flash"
        Write-Host "  [ok] Web Chat ready (launch with .\chat.bat)" -ForegroundColor Green
    } finally {
        $ErrorActionPreference = 'Stop'
        Pop-Location
    }
}

# --- 10. Startup Init (optional) -------------------------------------------
Write-Host ""
Write-Host "  -- Startup Init ----------------------------" -ForegroundColor DarkCyan

# Ask user if they want to add 'agon' command to PATH
Write-Host "     Add AGON folder to your PATH so you can type 'agon' anywhere?" -ForegroundColor White
Write-Host "     (This lets you open a terminal and just type: agon)" -ForegroundColor DarkGray
$addPath = Read-Host "  >> Add AGON to PATH? [Y/n]"
if ($addPath -eq "" -or $addPath -eq "y" -or $addPath -eq "Y") {
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $agonDir = $AGON_ROOT
    if ($userPath -notlike "*$agonDir*") {
        $newPath = $userPath + ";$agonDir"
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        Write-Host "  [ok] AGON added to PATH (reopen terminal for effect)" -ForegroundColor Green
    } else {
        Write-Host "  [ok] AGON already in PATH" -ForegroundColor Green
    }
} else {
    Write-Host "     Skipped. Use cd agon\ && .\agon.cmd to run." -ForegroundColor DarkYellow
}

# Ask about PowerShell profile init
Write-Host ""
Write-Host "     Add AGON startup banner to your PowerShell profile?" -ForegroundColor White
Write-Host "     (Shows the AGON banner every time you open a terminal)" -ForegroundColor DarkGray
$addProfile = Read-Host "  >> Add to PowerShell profile? [Y/n]"
if ($addProfile -eq "" -or $addProfile -eq "y" -or $addProfile -eq "Y") {
    $profilePath = $PROFILE
    $profileDir = Split-Path -Parent $profilePath
    if (-not (Test-Path $profileDir)) {
        New-Item -ItemType Directory -Force -Path $profileDir | Out-Null
    }
    $initLine = ". '$AGON_ROOT\init.ps1'"
    if (Test-Path $profilePath) {
        $profileContent = Get-Content $profilePath -Raw
        if ($profileContent -notlike "*init.ps1*") {
            Add-Content $profilePath "`n$initLine"
            Write-Host "  [ok] Added to PowerShell profile: $profilePath" -ForegroundColor Green
        } else {
            Write-Host "  [ok] Already in PowerShell profile" -ForegroundColor Green
        }
    } else {
        Set-Content $profilePath $initLine
        Write-Host "  [ok] Created PowerShell profile: $profilePath" -ForegroundColor Green
    }
} else {
    Write-Host "     Skipped. Source init.ps1 manually if needed." -ForegroundColor DarkYellow
}

# --- 11. Done -------------------------------------------------------------
Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  AGON INSTALLATION COMPLETE" -ForegroundColor Cyan
Write-Host "  DEUS VULT" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Three ways to use AGON:" -ForegroundColor White
Write-Host ""
Write-Host "  >> TERMINAL:" -ForegroundColor Green
Write-Host "    hermes chat"
Write-Host "    WAKE UP AGON"
Write-Host ""
Write-Host "  >> ONE-WORD COMMAND:" -ForegroundColor Green
Write-Host "    agon.cmd"
Write-Host "    (type 'agon' anywhere if you added it to PATH)"
Write-Host ""
Write-Host "  >> CHECK YOUR LEVEL (in chat):" -ForegroundColor Green
Write-Host "    /level  or  /bond" -ForegroundColor White
Write-Host "    (or locally: bond.cmd)" -ForegroundColor White
Write-Host ""
Write-Host "  >> BROWSER (like ChatGPT):" -ForegroundColor Green
Write-Host "    .\chat.bat"
Write-Host "    Opens http://localhost:8787"
Write-Host ""
Write-Host "  Model: deepseek/deepseek-v4-flash (all Nous tiers)" -ForegroundColor White
Write-Host "  DEUS VULT." -ForegroundColor Cyan
Write-Host ""
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
