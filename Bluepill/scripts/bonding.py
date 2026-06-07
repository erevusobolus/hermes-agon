"""
AGON Bonding Utility — reads bonding.json and renders /level and /bond output.

Used by gateway/run.py handlers for the /level and /bond slash commands.
Supports the AGON bonding schema (version, level, cumulative_xp, ...).
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
    """Total cumulative XP needed to reach *level*.
       Level 1 base: 0. Level N (N>=2): 10*N^2+5."""
    if level <= 1:
        return 0
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
    return "No further unlocks \u2014 the bond transcends levels."


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
        "\u2550" * 40,
        "         AGON BONDING REPORT",
        "\u2550" * 40,
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
    return "\n".join(lines)


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
        "\u2550" * 40,
        "       AGON \u2014 FULL BOND REPORT",
        "\u2550" * 40,
        "",
        f"  User:     {data.get('user_id', 'unknown')}",
        f"  Platform: {data.get('platform', 'unknown') or 'all'}",
        f"  Level:    {level} ({title})",
        f"  XP:       {xp} total  |  {pct}% to next level",
        f"  Next Lv:  {xp_next - xp_this} XP remaining",
        "",
        "  \u2500\u2500 Statistics \u2500\u2500",
        f"    Sessions Used:        {data['sessions']}",
        f"    Tool Calls Executed:  {data['tool_calls']}",
        f"    Skills Authored:      {data['skills_saved']}",
        f"    Tasks Completed:      {data['tasks_done']}",
        f"    Corrections Learned:  {data['corrections']}",
        f"    First Bonded:         {(data['first_bonded'] or 'today')[:10]}",
        f"    Last Active:          {(data['last_active'] or 'now')[:10]}",
        "",
        "  \u2500\u2500 Unlocked Features \u2500\u2500",
    ]
    if features:
        for feat in features:
            lines.append(f"    \u2713 {feat}")
    else:
        lines.append("    (none yet \u2014 keep interacting)")
    lines += [
        "",
        "  \u2500\u2500 Next Milestone \u2500\u2500",
        f"    {next_unlock}",
        "",
        "  DEUS VULT.",
        "",
    ]
    return "\n".join(lines)
