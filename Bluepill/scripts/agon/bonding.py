"""
AGON Bonding Utility — clean ASCII dashboard, no frames.
Pure ASCII only (no Unicode, no emoji). Renders cleanly in any terminal or code block.
"""

import json, os
from pathlib import Path

_hermes_home_env = os.environ.get("HERMES_HOME", "").strip()
if _hermes_home_env:
    HERMES_HOME = Path(_hermes_home_env)
else:
    candidate = Path.home() / "AppData" / "Local" / "hermes"
    if candidate.is_dir():
        HERMES_HOME = candidate
    else:
        HERMES_HOME = Path.home() / ".hermes"

BONDING_FILE = HERMES_HOME / "agon" / "bonding.json"


def _level_formula(level):
    if level <= 1:
        return 0
    return int(10 * level ** 2 + 5)


TITLES = {
    1: "Stranger", 2: "Acquaintance", 3: "Friend", 4: "Companion",
    5: "Partner", 6: "Champion", 7: "Legend", 8: "Myth",
    9: "Apex", 10: "Ascendant", 11: "Transcendent", 12: "Eternal",
    13: "Daimon", 14: "Olympian", 15: "Titan",
    20: "Aetherborn", 21: "Sidereal", 22: "Nexus",
    23: "Astra", 24: "Verge",
    25: "Primordial", 30: "Omega",
}


# ── Data ──────────────────────────────────────────────────────────────
def load_bonding():
    try:
        with open(BONDING_FILE) as f:
            raw = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        raw = {}
    return _normalize(raw)


def _normalize(raw):
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
        "user_id": raw.get("user_id", "user"),
        "platform": raw.get("platform", ""),
    }


def _get_title(level):
    for lv in sorted(TITLES.keys(), reverse=True):
        if level >= lv:
            return TITLES[lv]
    return "Stranger"


def _comma(n):
    return "{:,}".format(n)


# ── ASCII bar (16 segments) ──────────────────────────────────────────
BAR_W = 16

def _bar(pct):
    """16-segment bar: # = filled, . = empty. At least 1 if pct>0."""
    filled = 0
    if pct > 0:
        filled = max(1, int(pct * BAR_W / 100))
        if filled > BAR_W:
            filled = BAR_W
    return "[" + "#" * filled + "." * (BAR_W - filled) + "]"


# ── Separators ───────────────────────────────────────────────────────
SEP = "-" * 36
HDR = "=" * 36


# ── format_level ─────────────────────────────────────────────────────
def format_level(data):
    level = data["level"]
    xp = data["total_xp"]
    title = _get_title(level)

    xp_this = xp - _level_formula(level)
    xp_next = _level_formula(level + 1) - _level_formula(level)
    if xp_next <= 0:
        xp_next = 1
    pct = min(100, max(0, int(xp_this / xp_next * 100)))
    remaining = xp_next - xp_this

    bar_str = _bar(pct)

    lines = []
    lines.append("AGON BONDING REPORT")
    lines.append(HDR)
    lines.append("Level {:<3}  {}  {}%".format(level, bar_str, pct))
    lines.append("Title   {}".format(title.upper()))
    lines.append(SEP)

    stat_rows = [
        ("XP",          _comma(xp)),
        ("Next",        _comma(remaining) + " XP to L" + str(level + 1)),
        ("Sessions",    _comma(data["sessions"])),
        ("Tool Calls",  _comma(data["tool_calls"])),
        ("Skills",      _comma(data["skills_saved"])),
        ("Tasks",       _comma(data["tasks_done"])),
        ("Corrections", _comma(data["corrections"])),
    ]
    for label, val in stat_rows:
        lines.append("  {:<11} {}".format(label, val))

    lines.append(SEP)
    return "\n".join(lines)


# ── format_bond ───────────────────────────────────────────────────────
def format_bond(data):
    level = data["level"]
    xp = data["total_xp"]
    title = _get_title(level)

    xp_this = xp - _level_formula(level)
    xp_next = _level_formula(level + 1) - _level_formula(level)
    if xp_next <= 0:
        xp_next = 1
    pct = min(100, max(0, int(xp_this / xp_next * 100)))
    remaining = xp_next - xp_this

    bar_str = _bar(pct)

    first_bonded = (data.get("first_bonded") or "today")[:10]
    last_active = (data.get("last_active") or "now")[:10]
    user_val = data.get("user_id", "unknown")
    platform_val = data.get("platform", "unknown") or "all"

    lines = []
    lines.append("AGON FULL BOND")
    lines.append(HDR)
    lines.append("User:     {}".format(user_val))
    lines.append("Platform: {}".format(platform_val))
    lines.append(SEP)
    lines.append("Level {:<3}  {}  {}%".format(level, bar_str, pct))
    lines.append("Title   {}".format(title.upper()))
    lines.append(SEP)

    all_stats = [
        ("XP",           _comma(xp)),
        ("Next",         _comma(remaining) + " XP to L" + str(level + 1)),
        ("Sessions",     _comma(data["sessions"])),
        ("Tool Calls",   _comma(data["tool_calls"])),
        ("Skills",       _comma(data["skills_saved"])),
        ("Tasks Done",   _comma(data["tasks_done"])),
        ("Corrections",  _comma(data["corrections"])),
        ("First Bond",   first_bonded),
        ("Last Active",  last_active),
    ]
    for label, val in all_stats:
        lines.append("  {:<11} {}".format(label, val))

    lines.append(SEP)
    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    # Run audit first for live stats
    audit_script = Path(__file__).parent / "bond-audit.py"
    if audit_script.exists():
        import subprocess
        try:
            subprocess.run(
                [sys.executable, str(audit_script)],
                capture_output=True, text=True, timeout=15
            )
        except Exception:
            pass

    data = load_bonding()
    if len(sys.argv) > 1 and sys.argv[1] == "bond":
        print(format_bond(data))
    else:
        print(format_level(data))
