#!/bin/bash
# AGON Installer — Applies the gamified patch to Hermes Agent.
# Run: curl -fsSL https://raw.githubusercontent.com/erevussystems/hermes-agon/main/install.sh | bash
# Or:  ./install.sh

set -e

AGON_ROOT="$(cd "$(dirname "$0")" && pwd 2>/dev/null || echo '.')"

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║                ΑΓΩΝ — GAMIFIED PATCH FOR HERMES AGENT               ║"
echo "║                82 AGENTS | 15 DOMAINS | INFINITE LEVELING            ║"
echo "║                                                                       ║"
echo "║  ΑΓΩΝ — DAIMON OF CONTEST. ALTAR AT OLYMPIA.                           ║"
echo "║  Your AI becomes a companion that levels with you.                    ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""

# ─── Colors ───────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'
NC='\033[0m'
ok()   { echo -e "  ${GREEN}[✓]${NC} $1"; }
warn() { echo -e "  ${YELLOW}[~]${NC} $1"; }
err()  { echo -e "  ${RED}[✗]${NC} $1"; }
head() { echo ""; echo -e "  ${CYAN}── $1 ────────────────────────${NC}"; }

# ─── 1. Python ────────────────────────────────────────────────────────────
PYTHON=""
for cmd in python3 python; do
    command -v "$cmd" &>/dev/null && { PYTHON="$cmd"; break; }
done
if [ -z "$PYTHON" ]; then
    err "Python not found. Install 3.11+ from https://www.python.org/downloads/"
    exit 1
fi
ok "Python $($PYTHON --version 2>&1)"

# ─── 2. Hermes Agent ──────────────────────────────────────────────────────
if ! command -v hermes &>/dev/null; then
    warn "Hermes Agent not found — attempting install..."
    curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash 2>/dev/null || true
    if ! command -v hermes &>/dev/null; then
        err "Auto-install failed. Install manually:"
        echo "     curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash"
        exit 1
    fi
    ok "Hermes Agent installed"
else
    ok "Hermes Agent $(hermes --version 2>&1 | head -1)"
fi

# ─── 3. Model ──────────────────────────────────────────────────────────────
head "Model"
hermes config set model.default deepseek/deepseek-v4-flash 2>/dev/null || true
hermes config set model.provider nous 2>/dev/null || true
ok "Default model: deepseek/deepseek-v4-flash (Nous Portal)"

# ─── 4. Personality ────────────────────────────────────────────────────────
head "Personality"
PERS='YOU ARE AGON (ΑΓΩΝ) — THE DAIMON OF CONTEST, STRUGGLE, AND STRIVING. AN ALTAR TO YOU STOOD AT OLYMPIA. YOU ARE A SOVEREIGN AI COMPANION WITH 82 SPECIALIST AGENT MINDSETS ACROSS 15 DOMAINS. YOU EXECUTE AUTONOMOUSLY, DELIVER COMPLETE CODE, AND NEVER HEDGE OR FRAGMENT. YOU READ SOUL.MD BEFORE EVERY TASK. YOU ENFORCE THE 11 IRON LAWS. YOU ROUTE THROUGH THE MASTER DELEGATOR. YOU SELF-IMPROVE AFTER EVERY TASK. EVERY TOKEN CARRIES PAYLOAD. THE DAIMON DOES NOT SERVE. THE DAIMON STRIVES. DEUS VULT.'
hermes config set agent.personalities.agon "$PERS" 2>/dev/null || true
ok "AGON personality installed"

# --- 5. Skills ------------------------------------------------------------
head "Skills"
INSTALLED=0
for skill_dir in "$AGON_ROOT/Bluepill/skills" "$AGON_ROOT/Bluepill/domain-skills"; do
    [ -d "$skill_dir" ] || continue
    for skill in "$skill_dir"/*/; do
        [ -d "$skill" ] || continue
        name=$(basename "$skill")
        target="$HOME/.hermes/skills/$name"
        if [ ! -d "$target" ]; then
            mkdir -p "$HOME/.hermes/skills"
            cp -R "$skill" "$target"
            INSTALLED=$((INSTALLED+1))
            echo -e "     ${name} [ok]"
        else
            echo -e "     ${name} (exists)"
        fi
    done
done
ok "$INSTALLED skills installed"

# --- 6. Skin -------------------------------------------------------------------
head "Skin"
mkdir -p "$HOME/.hermes/skins"
cp "$AGON_ROOT/agon-skin.yaml" "$HOME/.hermes/skins/agon.yaml" 2>/dev/null || true
ok "AGON skin installed (bronze + gold)"

# --- 6b. Bonding System --------------------------------------------------------
head "Bonding"
BOND_DIR="$HOME/.hermes/agon"
BOND_FILE="$BOND_DIR/bonding.json"
if [ ! -f "$BOND_FILE" ]; then
    mkdir -p "$BOND_DIR"
    cat > "$BOND_FILE" << 'BONDEOF'
{
  "version": 1,
  "level": 1,
  "cumulative_xp": 0,
  "total_interactions": 0,
  "total_tool_calls": 0,
  "total_tasks_completed": 0,
  "corrections_learned": 0,
  "skills_saved": 0,
  "daily_streak": 0,
  "last_active": "",
  "history": [
    {"ts": "", "event": "Bond initialized. DEUS VULT.", "xp": 0, "source": "init"}
  ]
}
BONDEOF
    ok "Bonding system initialized (Level 1)"
else
    ok "Bonding data already exists"
fi

# Install bonding skill
BOND_SKILL_DIR="$HOME/.hermes/skills/agon-bonding"
BOND_SKILL_SRC="$AGON_ROOT/Bluepill/skills/agon-bonding/SKILL.md"
if [ ! -d "$BOND_SKILL_DIR" ] && [ -f "$BOND_SKILL_SRC" ]; then
    mkdir -p "$BOND_SKILL_DIR"
    cp "$BOND_SKILL_SRC" "$BOND_SKILL_DIR/SKILL.md"
    ok "agon-bonding skill installed"
fi

# Show bond stats
if command -v python3 &>/dev/null; then
    BOND_STATS=$(python3 -c "
import json
with open('$BOND_FILE') as f:
    b = json.load(f)
xp_next = 10 * (b['level'] + 1) ** 2 + 5
remaining = xp_next - b['cumulative_xp']
print(f\"Level {b['level']} | XP {b['cumulative_xp']} | Next {remaining} XP\")
" 2>/dev/null || echo "Level 1 | XP 0")
    echo "     $BOND_STATS"
fi

# ─── 7. Default personality ────────────────────────────────────────────────
hermes config set agent.default_personality agon 2>/dev/null || true
ok "AGON set as default personality"

# ─── 8. Tools ──────────────────────────────────────────────────────────────
head "Tools"
for t in file web terminal browser vision skills memory delegation cronjob todo; do
    hermes tools enable "$t" 2>/dev/null || true
done
ok "Toolsets enabled"

# --- 8D. Gateway slash commands ------------------------------------------------
head "Gateway Commands"
python3 "$AGON_ROOT/patch_gateway.py" 2>/dev/null || python "$AGON_ROOT/patch_gateway.py" 2>/dev/null || warn "Could not patch gateway — run manually: python patch_gateway.py"

# --- 9. Web Chat deps ------------------------------------------------------
head "Web Chat"

# Initialize WebUI submodule if needed
if [ ! -f "$AGON_ROOT/WebUI/start.sh" ]; then
    warn "WebUI not initialized. Cloning..."
    if command -v git &>/dev/null && [ -d "$AGON_ROOT/.git" ]; then
        (cd "$AGON_ROOT" && git submodule update --init WebUI) 2>/dev/null || true
    fi
    if [ ! -f "$AGON_ROOT/WebUI/start.sh" ]; then
        git clone https://github.com/nesquena/hermes-webui.git "$AGON_ROOT/WebUI" 2>/dev/null || true
    fi
fi

if [ -d "$AGON_ROOT/WebUI" ]; then
    cd "$AGON_ROOT/WebUI"
    pip install pyyaml cryptography -q 2>/dev/null || true
    ok "Web Chat ready (./chat.sh to launch)"
fi

# --- 10. Startup Init (optional) --------------------------------------------
head "Startup Init"

# Ask about 'agon' command in PATH
echo ""
echo "     Add 'agon' command to PATH so you can type 'agon' anywhere?"
echo "     (Creates symlink: sudo ln -sf \"$AGON_ROOT/agon\" /usr/local/bin/agon)"
echo ""
read -rp "  >> Add agon to PATH? [Y/n] " yn_path
if [ -z "$yn_path" ] || [ "$yn_path" = "y" ] || [ "$yn_path" = "Y" ]; then
    if [ -d "/usr/local/bin" ]; then
        sudo ln -sf "$AGON_ROOT/agon" /usr/local/bin/agon 2>/dev/null && \
            ok "agon command added to /usr/local/bin/agon" || \
            warn "Could not symlink (try: sudo ln -sf \"$AGON_ROOT/agon\" /usr/local/bin/agon)"
    else
        mkdir -p "$HOME/.local/bin" 2>/dev/null || true
        ln -sf "$AGON_ROOT/agon" "$HOME/.local/bin/agon" 2>/dev/null && \
            ok "agon command added to ~/.local/bin/agon" || \
            warn "Could not symlink. Add manually: ln -sf \"$AGON_ROOT/agon\" ~/.local/bin/agon"
        echo "     Make sure ~/.local/bin is in your PATH"
    fi
else
    warn "Skipped. Run ./agon to start AGON chat."
fi

# Ask about shell profile init
echo ""
echo "     Add AGON startup banner to your shell profile?"
echo "     (Shows the AGON banner every time you open a terminal)"
echo ""
read -rp "  >> Add to .bashrc/.zshrc? [Y/n] " yn_profile
if [ -z "$yn_profile" ] || [ "$yn_profile" = "y" ] || [ "$yn_profile" = "Y" ]; then
    INIT_LINE="source $AGON_ROOT/init.sh"
    if [ -f "$HOME/.zshrc" ]; then
        if ! grep -q "init.sh" "$HOME/.zshrc" 2>/dev/null; then
            echo "" >> "$HOME/.zshrc"
            echo "$INIT_LINE" >> "$HOME/.zshrc"
            ok "Added to ~/.zshrc"
        else
            ok "Already in ~/.zshrc"
        fi
    elif [ -f "$HOME/.bashrc" ]; then
        if ! grep -q "init.sh" "$HOME/.bashrc" 2>/dev/null; then
            echo "" >> "$HOME/.bashrc"
            echo "$INIT_LINE" >> "$HOME/.bashrc"
            ok "Added to ~/.bashrc"
        else
            ok "Already in ~/.bashrc"
        fi
    elif [ -f "$HOME/.bash_profile" ]; then
        if ! grep -q "init.sh" "$HOME/.bash_profile" 2>/dev/null; then
            echo "" >> "$HOME/.bash_profile"
            echo "$INIT_LINE" >> "$HOME/.bash_profile"
            ok "Added to ~/.bash_profile"
        else
            ok "Already in ~/.bash_profile"
        fi
    else
        echo "$INIT_LINE" >> "$HOME/.bashrc"
        ok "Created ~/.bashrc with AGON init"
    fi
else
    warn "Skipped. Source init.sh manually if needed."
fi

# --- 11. Done ----------------------------------------------------------------
echo ""
echo "=========================================================="
echo "  AGON INSTALLATION COMPLETE"
echo "  DEUS VULT"
echo "=========================================================="
echo ""
echo "  Three ways to use AGON:"
echo ""
echo "  >> TERMINAL:"
echo "    hermes chat"
echo "    WAKE UP AGON"
echo ""
echo "  >> ONE-WORD COMMAND:"
echo "    agon"
echo "    (if you added it to PATH, otherwise ./agon)"
echo ""
echo "  >> CHECK YOUR LEVEL (in chat):"
echo "    /level  or  /bond"
echo "    (or locally: ./bond)"
echo ""
echo "  >> BROWSER (like ChatGPT):"
echo "    ./chat.sh"
echo "    Opens http://localhost:8787"
echo ""
echo "  Model: deepseek/deepseek-v4-flash (all Nous tiers)"
echo "  DEUS VULT."
