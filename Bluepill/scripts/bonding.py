"""
AGON Bonding Utility — reads bonding.json and renders /level and /bond output.
Auto-render: level-ups detected programmatically by bond-audit.py.
Dashboard uses box-drawing characters — renders in any monospace terminal.
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

# Constants for box-drawing (avoids backslash in f-strings)
R1 = chr(0x2554)  # ╔
R2 = chr(0x2557)  # ╗
R3 = chr(0x255a)  # ╚
R4 = chr(0x255d)  # ╝
H  = chr(0x2550)  # ═
V  = chr(0x2551)  # ║
T  = chr(0x2560)  # ╠
B  = chr(0x2563)  # ╣
S1 = chr(0x2501)  # ━
S2 = chr(0x2503)  # ┃
BAR_F = chr(0x2588)  # █
BAR_E = chr(0x2591)  # ░
CHK  = chr(0x2713)  # ✓
STAR = chr(0x2605)  # ★
SWORD = chr(0x2694)  # ⚔
AGON = chr(0x0391) + chr(0x0393) + chr(0x03a9) + chr(0x039d)  # ΑΓΩΝ
DASH = chr(0x2014)  # —

# ── Level & Title tables ─────────────────────────────────────────────
def _level_formula(level):
    """Total cumulative XP needed to reach *level*.
       Level 1 base: 0. Level N (N>=2): 10*N^2+5."""
    if level <= 1:
        return 0
    return int(10 * level ** 2 + 5)

TITLES = {
    1: "Stranger", 2: "Acquaintance", 3: "Friend", 4: "Companion",
    5: "Partner", 6: "Champion", 7: "Legend", 8: "Myth",
    9: "Apex", 10: "Ascendant", 11: "Transcendent", 12: "Eternal",
    13: "Daimon", 14: "Olympian", 15: "Titan",
    20: "Aetherborn", 25: "Primordial", 30: "Omega",
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

# ── Data loading ────────────────────────────────────────────────────
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
        "unlocked_features": raw.get("unlocked_features", []),
        "user_id": raw.get("user_id", "user"),
        "platform": raw.get("platform", ""),
    }

def _get_title(level):
    for lv in sorted(TITLES.keys(), reverse=True):
        if level >= lv:
            return TITLES[lv]
    return "Stranger"

def _get_unlocked_list(level):
    return [UNLOCKS[lv] for lv in sorted(UNLOCKS.keys()) if lv <= level]

def _get_next_unlock(level):
    for lv in sorted(UNLOCKS.keys()):
        if lv > level:
            return "Level {}: {}".format(lv, UNLOCKS[lv])
    return "No further unlocks" + DASH + "the bond transcends levels."

# ── Bar render (20 segments) ────────────────────────────────────────
BAR_SEGMENTS = 20

def _bar(pct):
    filled = min(BAR_SEGMENTS, max(0, pct * BAR_SEGMENTS // 100))
    empty = BAR_SEGMENTS - filled
    return BAR_F * filled + BAR_E * empty

# ── Helpers ─────────────────────────────────────────────────────────
def _pad(text, width):
    return str(text).ljust(width)[:width]

def _comma(n):
    return "{:,}".format(n)

# ── format_level: compact dashboard ─────────────────────────────────
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

    next_u = _get_next_unlock(level)

    stats = [
        ("Sessions", data["sessions"]),
        ("Tool Calls", data["tool_calls"]),
        ("Skills Saved", data["skills_saved"]),
        ("Tasks Done", data["tasks_done"]),
        ("Corrections", data["corrections"]),
    ]

    unlocked = _get_unlocked_list(level)
    bar_str = _bar(pct)
    W = 46  # interior width

    lines = []
    # Header
    lines.append(R1 + H * W + R2)
    lines.append(V + "      " + SWORD + "  " + AGON + "  BONDING  REPORT  " + SWORD + "      " + V)
    lines.append(T + H * W + B)
    lines.append(V + "  " + " " * W + "  " + V)

    # Level line
    ll = "LEVEL {:>3} {}".format(level, bar_str) + "  {}%".format(pct)
    lines.append(V + "  " + _pad(ll, W) + "  " + V)

    # Title line
    tl = "  TITLE  {}".format(title.upper())
    lines.append(V + "  " + _pad(tl, W) + "  " + V)

    # XP + Next
    xl = "  XP    {}".format(_comma(xp))
    nl = "  NEXT  {} XP to level {}".format(_comma(remaining), level + 1)
    lines.append(V + "  " + _pad(xl, W) + "  " + V)
    lines.append(V + "  " + _pad(nl, W) + "  " + V)

    lines.append(V + "  " + " " * W + "  " + V)

    # Stats
    lines.append(V + "  " + _pad("  " + S1 * 3 + " BATTLE STATS " + S1 * 3, W) + "  " + V)
    for label, val in stats:
        sl = "  {} {}".format(_pad(label, 14), _comma(val).rjust(8))
        lines.append(V + "  " + _pad(sl, W) + "  " + V)

    lines.append(V + "  " + " " * W + "  " + V)

    # Next unlock
    lines.append(V + "  " + _pad("  " + S1 * 3 + " NEXT UNLOCK " + S1 * 3, W) + "  " + V)
    lines.append(V + "  " + _pad("  {}".format(next_u), W) + "  " + V)

    lines.append(V + "  " + " " * W + "  " + V)

    # Unlocked
    if unlocked:
        lines.append(V + "  " + _pad("  " + S1 * 3 + " UNLOCKED " + S1 * 3, W) + "  " + V)
        for feat in unlocked:
            lines.append(V + "  " + _pad("  " + CHK + "  {}".format(feat), W) + "  " + V)

    lines.append(V + "  " + " " * W + "  " + V)

    # Footer
    lines.append(T + H * W + B)
    footer_text = "     " + STAR + "  THE CONTEST NEVER ENDS  " + STAR + "     "
    lines.append(V + footer_text + V)
    lines.append(R3 + H * W + R4)

    return "\n".join(lines)

# ── format_bond: full detailed report ───────────────────────────────
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

    next_u = _get_next_unlock(level)
    unlocked = _get_unlocked_list(level)
    bar_str = _bar(pct)
    W = 46

    user_val = data.get("user_id", "unknown")
    platform_val = data.get("platform", "unknown") or "all"
    first_bonded = (data.get("first_bonded") or "today")[:10]
    last_active = (data.get("last_active") or "now")[:10]

    all_stats = [
        ("Sessions", data["sessions"]),
        ("Tool Calls", data["tool_calls"]),
        ("Skills Authored", data["skills_saved"]),
        ("Tasks Completed", data["tasks_done"]),
        ("Corrections Learned", data["corrections"]),
        ("First Bonded", first_bonded),
        ("Last Active", last_active),
    ]

    lines = []
    # Header
    lines.append(R1 + H * W + R2)
    lines.append(V + "    " + SWORD + "  " + AGON + "  FULL  BOND  " + SWORD + "    " + V)
    lines.append(T + H * W + B)
    lines.append(V + "  " + " " * W + "  " + V)
    lines.append(V + "  " + _pad("User: {}".format(user_val), W) + "  " + V)
    lines.append(V + "  " + _pad("Platform: {}".format(platform_val), W) + "  " + V)
    lines.append(V + "  " + " " * W + "  " + V)

    # Level line
    ll = "LEVEL {:>3} {}".format(level, bar_str) + "  {}%".format(pct)
    lines.append(V + "  " + _pad(ll, W) + "  " + V)

    tl = "  TITLE  {}".format(title.upper())
    lines.append(V + "  " + _pad(tl, W) + "  " + V)

    xl = "  XP  {}  total  |  {}% to next".format(_comma(xp), pct)
    lines.append(V + "  " + _pad(xl, W) + "  " + V)

    nl = "  NEXT  {} XP remaining".format(_comma(remaining))
    lines.append(V + "  " + _pad(nl, W) + "  " + V)
    lines.append(V + "  " + " " * W + "  " + V)

    # Stats
    lines.append(V + "  " + _pad("  " + S1 * 3 + " STATISTICS " + S1 * 3, W) + "  " + V)
    for label, val in all_stats:
        sl = "  {} {}".format(_pad(label, 18), str(val).rjust(12))
        lines.append(V + "  " + _pad(sl, W) + "  " + V)

    lines.append(V + "  " + " " * W + "  " + V)

    # Unlocked features
    if unlocked:
        lines.append(V + "  " + _pad("  " + S1 * 3 + " UNLOCKED FEATURES " + S1 * 3, W) + "  " + V)
        for feat in unlocked:
            lines.append(V + "  " + _pad("  " + CHK + "  {}".format(feat), W) + "  " + V)
    else:
        lines.append(V + "  " + _pad("  " + S1 * 3 + " UNLOCKED FEATURES " + S1 * 3, W) + "  " + V)
        lines.append(V + "  " + _pad("  (none yet" + DASH + "keep interacting)", W) + "  " + V)

    lines.append(V + "  " + " " * W + "  " + V)

    # Next milestone
    lines.append(V + "  " + _pad("  " + S1 * 3 + " NEXT MILESTONE " + S1 * 3, W) + "  " + V)
    lines.append(V + "  " + _pad("  {}".format(next_u), W) + "  " + V)
    lines.append(V + "  " + " " * W + "  " + V)

    # Footer
    lines.append(T + H * W + B)
    footer_text = "     " + STAR + "  THE CONTEST NEVER ENDS  " + STAR + "     "
    lines.append(V + footer_text + V)
    lines.append(R3 + H * W + R4)

    return "\n".join(lines)

# ── CLI entry point ─────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    data = load_bonding()
    if len(sys.argv) > 1 and sys.argv[1] == "bond":
        print(format_bond(data))
    else:
        print(format_level(data))
