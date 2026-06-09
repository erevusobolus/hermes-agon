#!/usr/bin/env python3
"""
AGON Gateway Patch — registers /level and /bond as gateway slash commands.

Idempotent: safe to run multiple times. Detects already-patched state
and skips. Patches Hermes source files and creates ~/.hermes/agon/bonding.py.

Run after installing/updating Hermes Agent. Called automatically by
install.sh / install.ps1.
"""
import json, os, re, shutil, sys
from pathlib import Path

HERMES_SRC = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")) / "hermes-agent"
AGON_DIR = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")) / "agon"


# ─── helpers ────────────────────────────────────────────────────────────────

def _splice_before_text(path: Path, marker: str, new_block: str, check: str = "") -> bool:
    """Insert *new_block* before the first line containing *marker*.
    If *check* is provided and found in the file, skip (already patched).
    """
    content = path.read_text(encoding="utf-8")
    if check and check in content:
        return False  # already present
    idx = content.find(marker)
    if idx == -1:
        print(f"  [!] Could not find marker '{marker}' in {path}")
        return False
    insert_at = content.index("\n", idx) + 1
    new_content = content[:insert_at] + new_block + "\n" + content[insert_at:]
    path.write_text(new_content, encoding="utf-8")
    return True


# ─── step 1: patch commands.py ─────────────────────────────────────────────

COMMANDS_CHECK = 'CommandDef("level", "Show AGON bonding level'
COMMANDS_MARKER = 'CommandDef("quit", "Exit the CLI (use --delete'
COMMANDS_BLOCK = """\
    CommandDef("debug", "Upload debug report (system info + logs) and get shareable links", "Info"),

    # AGON Bonding
    CommandDef("level", "Show AGON bonding level, XP bar, stats, and next unlock", "Info",
               aliases=("bond", "xp", "bonding"), gateway_only=True),
    CommandDef("bond", "Show full AGON bonding report with all details", "Info",
               gateway_only=True),

    # Exit
    CommandDef("quit", "Exit the CLI (use --delete to also remove session history)", "Exit",
"""


def patch_commands():
    path = HERMES_SRC / "hermes_cli" / "commands.py"
    if not path.exists():
        print(f"  [X] commands.py not found at {path}")
        return False
    if _splice_before_text(path, COMMANDS_MARKER, COMMANDS_BLOCK, check=COMMANDS_CHECK):
        print("  [\u2713] /level and /bond added to COMMAND_REGISTRY")
    else:
        print("  [\u2713] /level and /bond already registered (skipped)")
    return True


# ─── step 2: patch gateway dispatch in run.py ──────────────────────────────

DISPATCH_CHECK = 'canonical in ("level", "bond")'
DISPATCH_MARKER = 'if canonical == "restart"'
DISPATCH_BLOCK = """\
        if canonical in ("level", "bond"):
            return await self._handle_agon_bond_command(event, detail=canonical == "bond")
"""


def patch_dispatch():
    path = HERMES_SRC / "gateway" / "run.py"
    if not path.exists():
        print(f"  [X] run.py not found at {path}")
        return False
    if _splice_before_text(path, DISPATCH_MARKER, DISPATCH_BLOCK, check=DISPATCH_CHECK):
        print("  [\u2713] /level and /bond dispatch added to gateway")
    else:
        print("  [\u2713] /level and /bond dispatch already present (skipped)")
    return True


# ─── step 3: patch handler method in run.py ────────────────────────────────

HANDLER_CHECK = "_handle_agon_bond_command"
HANDLER_MARKER = 'async def _handle_platform_command'
HANDLER_BLOCK = """\
    async def _handle_agon_bond_command(self, event: MessageEvent, detail: bool = False) -> str:
        \"\"\"Handle ``/level`` and ``/bond`` — show AGON bonding report.\"\"\"
        try:
            import sys
            sys.path.insert(0, os.path.expanduser("~/.hermes/agon"))
            from bonding import format_level, format_bond, load_bonding
            data = load_bonding()
            if detail:
                return format_bond(data)
            return format_level(data)
        except Exception as exc:
            logger.warning("AGON bond command failed: %s", exc)
            return (
                "AGON bonding system is not initialized. "
                "Run the AGON installer from your hermes-agon project:\\n"
                "  cd ~/Documents/hermes-agon && ./install.sh"
            )
"""


def patch_handler():
    path = HERMES_SRC / "gateway" / "run.py"
    if not path.exists():
        return False
    if _splice_before_text(path, HANDLER_MARKER, HANDLER_BLOCK, check=HANDLER_CHECK):
        print("  [\u2713] AGON bond handler method added to gateway")
    else:
        print("  [\u2713] AGON bond handler already present (skipped)")
    return True


# ─── step 4: create bonding.py utility ────────────────────────────────────

BONDING_PY = '''"""
AGON Bonding Utility — reads bonding.json and renders /level and /bond output.

Used by gateway/run.py handlers for the /level and /bond slash commands.
Supports the AGON bonding schema (version, level, cumulative_xp, ...).
"""
import json
from pathlib import Path

HERMES_HOME = Path(__file__).resolve().parent
BONDING_FILE = HERMES_HOME / "bonding.json"

TITLES = {
    1: "Stranger", 2: "Acquaintance", 3: "Friend", 4: "Companion",
    5: "Partner", 6: "Champion", 7: "Legend", 8: "Myth",
    9: "Apex", 10: "Ascendant", 11: "Transcendent", 12: "Eternal",
    13: "Daimon", 14: "Olympian", 15: "Titan",
}

UNLOCKS = {
    2: "Session memory recall",
    3: "Auto-compression on session end",
    4: "Skill suggestions on complex tasks",
    5: "Preference detection without asking",
    6: "Proactive task suggestions",
    7: "Auto-creates skills from repeated patterns",
    8: "Predictive domain routing",
    9: "Full autonomous maintenance",
    10: "Suggests work unprompted",
    15: "Cross-project context awareness",
    20: "Predicts next task from history",
    25: "Multi-session strategy awareness",
    30: "Autonomous skill optimization",
}


def _level_formula(level: int) -> int:
    """Total XP needed to reach *level* (inclusive)."""
    return int(10 * level ** 2 + 5)


def load_bonding() -> dict:
    """Load bonding.json and return normalized data."""
    try:
        with open(BONDING_FILE) as f:
            raw = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        raw = {}
    return _normalize(raw)


def _normalize(raw: dict) -> dict:
    """Normalize AGON bonding JSON to internal schema."""
    return {
        "level": raw.get("level") or raw.get("bonding_level", 1),
        "total_xp": raw.get("cumulative_xp") or raw.get("total_xp", 0),
        "sessions": raw.get("total_interactions") or raw.get("total_sessions", 0),
        "tool_calls": raw.get("total_tool_calls", 0),
        "skills_saved": raw.get("skills_saved") or raw.get("total_skills_created", 0),
        "tasks_done": raw.get("total_tasks_completed", 0),
        "corrections": raw.get("corrections_learned") or raw.get("total_corrections", 0),
        "first_bonded": raw.get("first_bonded", ""),
        "last_active": raw.get("last_active", ""),
        "unlocked_features": raw.get("unlocked_features", []),
        "user_id": raw.get("user_id", "user"),
        "platform": raw.get("platform", ""),
    }


def _get_title(level: int) -> str:
    for lv in sorted(TITLES.keys(), reverse=True):
        if level >= lv:
            return TITLES[lv]
    return "Stranger"


def _get_next_unlock(level: int) -> str:
    for lv in sorted(UNLOCKS.keys()):
        if lv > level:
            return f"Level {lv}: {UNLOCKS[lv]}"
    return "No further unlocks \\u2014 the bond transcends levels."


def _bar(pct: int) -> str:
    filled = min(10, max(0, pct // 10))
    empty = 10 - filled
    return chr(0x2588) * filled + chr(0x2592) * empty


def format_level(data: dict) -> str:
    """Compact /level response."""
    level = data["level"]
    xp = data["total_xp"]
    xp_this = xp - _level_formula(level)
    xp_next = _level_formula(level + 1) - _level_formula(level)
    if xp_next <= 0:
        xp_next = 1
    pct = min(100, max(0, int(xp_this / xp_next * 100)))
    lines = [
        "\\u2550" * 40,
        "         AGON BONDING REPORT",
        "\\u2550" * 40,
        "",
        f"  Level:    {level}  {_bar(pct)}  {pct}%",
        f"  Title:    {_get_title(level)}",
        f"  XP:       {xp} total",
        f"  To Next:  {xp_next - xp_this} XP",
        "",
        "  Stats:",
        f"    Sessions:       {data['sessions']}",
        f"    Tool Calls:     {data['tool_calls']}",
        f"    Skills Saved:   {data['skills_saved']}",
        f"    Tasks Done:     {data['tasks_done']}",
        f"    Corrections:    {data['corrections']}",
        f"    Bonded Since:   {(data['first_bonded'] or 'today')[:10]}",
        "",
        f"  Next:   {_get_next_unlock(level)}",
        "",
        "  DEUS VULT.",
        "",
    ]
    return "\\n".join(lines)


def format_bond(data: dict) -> str:
    """Full /bond report."""
    level = data["level"]
    xp = data["total_xp"]
    xp_this = xp - _level_formula(level)
    xp_next = _level_formula(level + 1) - _level_formula(level)
    if xp_next <= 0:
        xp_next = 1
    pct = min(100, max(0, int(xp_this / xp_next * 100)))
    title = _get_title(level)
    next_unlock = _get_next_unlock(level)
    features = data.get("unlocked_features", []) or []

    lines = [
        "\\u2550" * 40,
        "       AGON \\u2014 FULL BOND REPORT",
        "\\u2550" * 40,
        "",
        f"  User:     {data.get('user_id', 'unknown')}",
        f"  Platform: {data.get('platform', 'unknown') or 'all'}",
        f"  Level:    {level} ({title})",
        f"  XP:       {xp} total  |  {pct}% to next level",
        f"  Next Lv:  {xp_next - xp_this} XP remaining",
        "",
        "  \\u2500\\u2500 Statistics \\u2500\\u2500",
        f"    Sessions Used:        {data['sessions']}",
        f"    Tool Calls Executed:  {data['tool_calls']}",
        f"    Skills Authored:      {data['skills_saved']}",
        f"    Tasks Completed:      {data['tasks_done']}",
        f"    Corrections Learned:  {data['corrections']}",
        f"    First Bonded:         {(data['first_bonded'] or 'today')[:10]}",
        f"    Last Active:          {(data['last_active'] or 'now')[:10]}",
        "",
        "  \\u2500\\u2500 Unlocked Features \\u2500\\u2500",
    ]
    if features:
        for feat in features:
            lines.append(f"    \\u2713 {feat}")
    else:
        lines.append("    (none yet \\u2014 keep interacting)")
    lines += [
        "",
        "  \\u2500\\u2500 Next Milestone \\u2500\\u2500",
        f"    {next_unlock}",
        "",
        "  DEUS VULT.",
        "",
    ]
    return "\\n".join(lines)
'''


def create_bonding_py():
    AGON_DIR.mkdir(parents=True, exist_ok=True)
    dest = AGON_DIR / "bonding.py"
    if dest.exists() and "format_level" in dest.read_text(encoding="utf-8"):
        print("  [\u2713] bonding.py already up to date (skipped)")
        return True
    dest.write_text(BONDING_PY, encoding="utf-8")
    print("  [\u2713] ~/.hermes/agon/bonding.py created")
    return True


# ─── step 5: ensure bonding.json exists ────────────────────────────────────

def ensure_bonding_json():
    AGON_DIR.mkdir(parents=True, exist_ok=True)
    dest = AGON_DIR / "bonding.json"
    if dest.exists():
        print("  [\u2713] bonding.json already exists (keeping your stats)")
        return True
    default = {
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
        ],
    }
    dest.write_text(json.dumps(default, indent=2), encoding="utf-8")
    print("  [\u2713] bonding.json initialized (Level 1)")
    return True


# ─── main ──────────────────────────────────────────────────────────────────

# ─── step 6: install skill to Hermes skills dir ──────────────────────────

SKILL_NAME = "agon-gateway-bonding"


def install_skill():
    """Copy the skill SKILL.md from the repo to ~/.hermes/skills/."""
    repo_skill = Path(__file__).resolve().parent / "Bluepill" / "skills" / SKILL_NAME / "SKILL.md"
    dest_dir = Path.home() / ".hermes" / "skills" / SKILL_NAME
    dest = dest_dir / "SKILL.md"
    if dest.exists():
        print(f"  [\u2713] skill '{SKILL_NAME}' already installed (skipped)")
        return True
    if not repo_skill.exists():
        print(f"  [!] skill source not found at {repo_skill}")
        return True  # non-fatal
    dest_dir.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(str(repo_skill), str(dest))
    print(f"  [\u2713] skill '{SKILL_NAME}' installed")
    return True


def _install_bond_responder():
    """Copy bond-responder.py from Bluepill/scripts/ to ~/.hermes/agon/."""
    repo_script = Path(__file__).resolve().parent / "Bluepill" / "scripts" / "bond-responder.py"
    dest = AGON_DIR / "bond-responder.py"
    if not repo_script.exists():
        print("  [!] bond-responder.py not found in repo (non-fatal)")
        return True
    if dest.exists() and "AGON Bond Responder" in dest.read_text(encoding="utf-8"):
        print("  [ok] bond-responder.py already up to date (skipped)")
        return True
    import shutil
    shutil.copy2(str(repo_script), str(dest))
    print("  [ok] bond-responder.py installed — programmatic /level and /bond")
    return True


def main():
    print("")
    print("  -- Patch: AGON Gateway Commands --------------------")

    if not HERMES_SRC.exists():
        print(f"  [X] Hermes source not found at {HERMES_SRC}")
        print("      Make sure Hermes Agent is installed.")
        return False

    ok = True
    ok &= patch_commands()
    ok &= patch_dispatch()
    ok &= patch_handler()
    ok &= create_bonding_py()
    ok &= ensure_bonding_json()
    ok &= install_skill()
    ok &= _install_bond_responder()

    if ok:
        print("")
        print("  [\u2713] AGON Gateway patched successfully!")
        print("      /level and /bond now work across all platforms")
        print("      (Telegram, Discord, CLI, WebUI)")
        print("      Restart the gateway: hermes gateway restart")
        print("")


if __name__ == "__main__":
    main()
