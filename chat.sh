#!/usr/bin/env bash
# AGON Web Chat — one-click launcher for Linux/Mac.
# Checks Python + Hermes + deps, installs what's missing, sets AGON config,
# then launches the WebUI via the WebUI's native start.sh.
set -euo pipefail

AGON_ROOT="$(cd "$(dirname "$0")" && pwd)"
WEBUI_DIR="$AGON_ROOT/WebUI"
HERMES_HOME="${HOME}/.hermes"

# ─── Color helpers ──────────────────────────────────────────────────────
bold='\033[1m'; cyan='\033[0;36m'; green='\033[0;32m'
yellow='\033[0;33m'; red='\033[0;31m'; dark='\033[2m'; reset='\033[0m'

info()  { echo -e "${cyan}$1${reset}"; }
ok()    { echo -e "${green}  [✓] $1${reset}"; }
warn()  { echo -e "${yellow}  [!] $1${reset}"; }
fail()  { echo -e "${red}  [✗] $1${reset}"; }

# ─── Header ─────────────────────────────────────────────────────────────
echo ""
echo -e "${cyan}╔═══════════════════════════════════════════════════════════════════════╗${reset}"
echo -e "${cyan}║  ΑΓΩΝ — DAIMON OF CONTEST. ALTAR AT OLYMPIA.                           ║${reset}"
echo -e "${cyan}║                Opens in your browser. Like ChatGPT.                   ║${reset}"
echo -e "${cyan}╚═══════════════════════════════════════════════════════════════════════╝${reset}"
echo ""

# ─── 1. Validate paths ─────────────────────────────────────────────────
if [ ! -d "$WEBUI_DIR" ]; then
    fail "WebUI directory not found at:"
    echo "      $WEBUI_DIR"
    echo "      Run install.sh first, or:"
    echo "        git submodule update --init WebUI"
    exit 1
fi
if [ ! -f "$WEBUI_DIR/start.sh" ]; then
    fail "start.sh not found in WebUI directory."
    echo "      Run install.sh first, or:"
    echo "        git submodule update --init WebUI"
    exit 1
fi

ok_count=0

# ─── 2. Python ──────────────────────────────────────────────────────────
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        PYTHON="$cmd"
        break
    fi
done
if [ -z "$PYTHON" ]; then
    fail "Python not found"
    echo "      Install Python 3.12+ from https://www.python.org/downloads/"
    echo "      Then run this script again."
    exit 1
fi
pyver=$("$PYTHON" --version 2>&1)
ok "$pyver"; ((ok_count++))

# ─── 3. Hermes Agent ────────────────────────────────────────────────────
if ! command -v hermes &>/dev/null; then
    warn "Hermes Agent not found — installing..."
    # Try pip first
    if command -v pip &>/dev/null; then
        pip install hermes-agent 2>/dev/null || true
    fi
    if command -v pip3 &>/dev/null; then
        pip3 install hermes-agent 2>/dev/null || true
    fi
    if command -v hermes &>/dev/null; then
        ok "Hermes Agent installed via pip"
    else
        warn "pip install failed — trying curl installer..."
        curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash 2>/dev/null || true
        # shellcheck disable=SC1091
        [ -f "$HOME/.hermes/env" ] && source "$HOME/.hermes/env"
    fi
    if command -v hermes &>/dev/null; then
        ok "Hermes Agent installed"; ((ok_count++))
    else
        fail "Could not install Hermes automatically."
        echo "      Try: pip install hermes-agent"
        echo "      Or:  https://hermes-agent.nousresearch.com/docs"
        exit 1
    fi
else
    hver=$(hermes --version 2>&1 | head -1)
    ok "Hermes $hver"; ((ok_count++))
fi

# ─── 4. AGON Config ─────────────────────────────────────────────────────
echo ""
echo -e "${cyan}  ── AGON Configuration ───────────────────────${reset}"
hermes config set model.default "deepseek/deepseek-v4-flash" 2>/dev/null || true
hermes config set model.provider "nous" 2>/dev/null || true
echo "     Model: deepseek/deepseek-v4-flash (Nous Portal)"

SKIN_DIR="$HERMES_HOME/skins"
SKIN_DST="$SKIN_DIR/agon.yaml"
SKIN_SRC="$AGON_ROOT/agon-skin.yaml"
if [ -f "$SKIN_SRC" ]; then
    mkdir -p "$SKIN_DIR"
    cp "$SKIN_SRC" "$SKIN_DST"
    echo "     Skin:  AGON bronze+gold"
else
    echo -e "${yellow}     Skin:  agon-skin.yaml not found (optional)${reset}"
fi

# ─── 5. WebUI Python deps ──────────────────────────────────────────────
echo ""
echo -e "${cyan}  ── WebUI Dependencies ───────────────────────${reset}"
(cd "$WEBUI_DIR" && pip install pyyaml cryptography -q 2>/dev/null || true)
echo "     Python packages ready"

# ─── 6. Set env vars ────────────────────────────────────────────────────
export HERMES_WEBUI_DEFAULT_MODEL="deepseek/deepseek-v4-flash"
export HERMES_WEBUI_HOST="127.0.0.1"
export HERMES_WEBUI_PORT="8787"

# ─── 7. Summary ─────────────────────────────────────────────────────────
echo ""
echo -e "${cyan}╔═══════════════════════════════════════════════════════════════════════╗${reset}"
echo -e "${cyan}║           All checks passed! Launching WebUI...                        ║${reset}"
echo -e "${cyan}║           Opening http://localhost:8787 in your browser.                ║${reset}"
echo -e "${cyan}║           Close this window to stop the server.                         ║${reset}"
echo -e "${cyan}║                                                                       ║${reset}"
echo -e "${cyan}║                           DEUS VULT.                                    ║${reset}"
echo -e "${cyan}╚═══════════════════════════════════════════════════════════════════════╝${reset}"
echo ""

# ─── 8. Launch browser + server ─────────────────────────────────────────
# Open browser (cross-platform)
case "$(uname -s)" in
    Darwin) open "http://localhost:8787" ;;
    Linux)  xdg-open "http://localhost:8787" 2>/dev/null || true ;;
esac

# Launch via the WebUI's native start.sh (runs server.py directly)
cd "$WEBUI_DIR" && exec bash start.sh
