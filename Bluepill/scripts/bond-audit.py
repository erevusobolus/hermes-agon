#!/usr/bin/env python3
"""
AGON Bond Audit — auto-detects real stats from the environment.
Run after every interaction to keep bonding.json honest.
No hardcoded numbers. Everything computed from reality.

Auto-detects level-ups and logs them programmatically.
"""
import json
import os
import sqlite3
from datetime import datetime, date
from pathlib import Path

# === Paths ===
_hermes_home_env = os.environ.get("HERMES_HOME", "").strip()
if _hermes_home_env:
    HERMES_HOME = Path(_hermes_home_env)
else:
    candidate = Path.home() / "AppData" / "Local" / "hermes"
    if candidate.is_dir():
        HERMES_HOME = candidate
    else:
        HERMES_HOME = Path.home() / ".hermes"

BOND_FILE = HERMES_HOME / "agon" / "bonding.json"
SKILLS_DIR = HERMES_HOME / "skills"
SESSION_DB = HERMES_HOME / "state.db"
LEGACY_BOND = Path.home() / ".hermes" / "agon" / "bonding.json"

# === Titles & Unlocks ===
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

# === Level Formula ===
def calc_level(cumulative_xp: int) -> int:
    """Level N requires 10*N^2+5 cumulative XP.
    Level 1: 0-44 XP, Level 2: 45-94, Level 3: 95-254, etc."""
    if cumulative_xp < 45:
        return 1
    level = 2
    while True:
        needed = 10 * (level + 1) * (level + 1) + 5
        if cumulative_xp < needed:
            return level
        level += 1

def xp_for_level(level: int) -> int:
    if level <= 1:
        return 0
    return 10 * level * level + 5

def next_level_xp_total(cumulative_xp: int) -> int:
    return xp_for_level(calc_level(cumulative_xp) + 1)

def get_title(level: int) -> str:
    for lv in sorted(TITLES.keys(), reverse=True):
        if level >= lv:
            return TITLES[lv]
    return "Stranger"

def get_next_unlock(level: int) -> str:
    for lv in sorted(UNLOCKS.keys()):
        if lv > level:
            return f"Level {lv}: {UNLOCKS[lv]}"
    return "No further unlocks — the bond transcends levels."

def get_unlocked_upto(level: int) -> list[dict]:
    """Return all unlocks earned up to this level."""
    result = []
    for lv in sorted(UNLOCKS.keys()):
        if lv <= level:
            result.append({"level": lv, "feature": UNLOCKS[lv]})
    return result

# === Auto-Detect Functions ===
def count_skills() -> int:
    if not SKILLS_DIR.exists():
        return 0
    count = 0
    for root, dirs, files in os.walk(SKILLS_DIR):
        if "SKILL.md" in files:
            count += 1
    return count

def count_interactions_and_tool_calls(db_path: Path) -> dict:
    result = {"interactions": 0, "tool_calls": 0}
    if not db_path.exists():
        return result
    try:
        conn = sqlite3.connect(str(db_path))
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM messages WHERE role IN ('user', 'assistant')")
        result["interactions"] = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM messages WHERE role = 'tool'")
        result["tool_calls"] = c.fetchone()[0]
        conn.close()
    except Exception:
        pass
    return result

def _merge_legacy_data(bond: dict, legacy: dict) -> dict:
    merged = dict(bond)
    old_xp = legacy.get("total_xp", 0) or legacy.get("cumulative_xp", 0)
    if old_xp > merged.get("cumulative_xp", 0):
        merged["cumulative_xp"] = old_xp
    for legacy_key, new_key in [
        ("total_tasks_completed", "total_tasks_completed"),
        ("total_corrections", "corrections_learned"),
        ("total_skills_created", "skills_saved"),
        ("total_sessions", "total_interactions"),
    ]:
        old_val = legacy.get(legacy_key, 0)
        if old_val > merged.get(new_key, 0):
            merged[new_key] = old_val
    old_features = legacy.get("unlocked_features", [])
    if old_features:
        merged["unlocked_features"] = old_features
    for key in ["user_id", "platform", "first_bonded"]:
        val = legacy.get(key)
        if val and not merged.get(key):
            merged[key] = val
    return merged

# === Audit ===
def audit():
    """Read bonding.json, audit stats, write corrected version.
    Returns summary dict with 'leveled_up' flag if level changed."""
    bond = {"version": 1}

    if BOND_FILE.exists():
        try:
            bond = json.loads(BOND_FILE.read_text(encoding="utf-8"))
        except Exception:
            bond = {"version": 1}

    if LEGACY_BOND.exists():
        try:
            legacy = json.loads(LEGACY_BOND.read_text(encoding="utf-8"))
            bond = _merge_legacy_data(bond, legacy)
        except Exception:
            pass

    defaults = {
        "version": 1, "level": 1, "cumulative_xp": 0,
        "total_interactions": 0, "total_tool_calls": 0,
        "total_tasks_completed": 0, "corrections_learned": 0,
        "skills_saved": 0, "daily_streak": 0,
        "last_active": datetime.now().isoformat(), "history": [],
        "unlocked_features": [],
    }
    for k, v in defaults.items():
        bond.setdefault(k, v)

    old_level = bond.get("level", 1)

    installed_skills = count_skills()
    bond["skills_saved"] = max(bond.get("skills_saved", 0), installed_skills)

    db_stats = count_interactions_and_tool_calls(SESSION_DB)
    bond["total_interactions"] = max(bond.get("total_interactions", 0), db_stats["interactions"])
    bond["total_tool_calls"] = max(bond.get("total_tool_calls", 0), db_stats["tool_calls"])

    # Compute XP from DB stats
    db_base_xp = bond["total_interactions"] * 1 + bond["total_tool_calls"] * 2
    history_xp = sum(h.get("xp", 0) for h in bond.get("history", []))
    bond["cumulative_xp"] = max(db_base_xp, history_xp)

    # Recover corrections/tasks from history
    bond["corrections_learned"] = max(bond.get("corrections_learned", 0),
                                       sum(1 for h in bond.get("history", []) if h.get("source") == "correction"))
    bond["total_tasks_completed"] = max(bond.get("total_tasks_completed", 0),
                                         sum(1 for h in bond.get("history", []) if h.get("source") == "task"))

    # Recalculate level
    new_level = calc_level(bond["cumulative_xp"])
    bond["level"] = new_level
    bond["last_active"] = datetime.now().isoformat()

    # Programmatic level-up detection
    leveled_up = new_level > old_level
    if leveled_up and old_level > 0:
        new_title = get_title(new_level)
        unlocks = get_unlocked_upto(new_level)
        # Only log unlocks that haven't been logged yet
        already_unlocked = set(bond.get("unlocked_features", []))
        new_unlocks = [u["feature"] for u in unlocks if u["feature"] not in already_unlocked]

        unlock_str = ""
        if new_unlocks:
            unlock_str = " Unlocked: " + ", ".join(new_unlocks)

        bond["history"].append({
            "ts": datetime.now().isoformat(),
            "event": f"LEVEL UP! Level {new_level} — {new_title}.{unlock_str}",
            "xp": bond["cumulative_xp"],
            "source": "level_up",
        })

        # Track unlocked features
        all_unlocked = set(u["feature"] for u in unlocks)
        bond["unlocked_features"] = list(all_unlocked)

    BOND_FILE.parent.mkdir(parents=True, exist_ok=True)
    BOND_FILE.write_text(json.dumps(bond, indent=2, ensure_ascii=False), encoding="utf-8")

    summary = _summary(bond)
    summary["leveled_up"] = leveled_up
    return summary

def add_xp(xp_amount: int, source: str, event: str) -> dict:
    """Add XP and re-audit. Detects level-ups programmatically."""
    bond = {"version": 1}
    if BOND_FILE.exists():
        try:
            bond = json.loads(BOND_FILE.read_text(encoding="utf-8"))
        except Exception:
            bond = {"version": 1}

    for k, v in {
        "version": 1, "level": 1, "cumulative_xp": 0,
        "total_interactions": 0, "total_tool_calls": 0,
        "total_tasks_completed": 0, "corrections_learned": 0,
        "skills_saved": 0, "daily_streak": 0,
        "last_active": datetime.now().isoformat(), "history": [],
        "unlocked_features": [],
    }.items():
        bond.setdefault(k, v)

    old_level = bond.get("level", 1)
    bond["cumulative_xp"] += xp_amount

    if source == "task":
        bond["total_tasks_completed"] = bond.get("total_tasks_completed", 0) + 1
    elif source == "correction":
        bond["corrections_learned"] = bond.get("corrections_learned", 0) + 1
    elif source == "skill":
        bond["skills_saved"] = bond.get("skills_saved", 0) + 1
    elif source == "interaction":
        bond["total_interactions"] = bond.get("total_interactions", 0) + 1

    bond["history"].append({
        "ts": datetime.now().isoformat(),
        "event": event,
        "xp": xp_amount,
        "source": source,
    })

    new_level = calc_level(bond["cumulative_xp"])
    bond["level"] = new_level
    bond["last_active"] = datetime.now().isoformat()

    # Programmatic level-up detection
    if new_level > old_level:
        new_title = get_title(new_level)
        unlocks = get_unlocked_upto(new_level)
        already_unlocked = set(bond.get("unlocked_features", []))
        new_unlocks = [u["feature"] for u in unlocks if u["feature"] not in already_unlocked]
        unlock_str = ""
        if new_unlocks:
            unlock_str = " Unlocked: " + ", ".join(new_unlocks)
        bond["history"].append({
            "ts": datetime.now().isoformat(),
            "event": f"LEVEL UP! Level {new_level} — {new_title}.{unlock_str}",
            "xp": bond["cumulative_xp"],
            "source": "level_up",
        })
        all_unlocked = set(u["feature"] for u in unlocks)
        bond["unlocked_features"] = list(all_unlocked)

    BOND_FILE.parent.mkdir(parents=True, exist_ok=True)
    BOND_FILE.write_text(json.dumps(bond, indent=2, ensure_ascii=False), encoding="utf-8")

    summary = _summary(bond)
    summary["leveled_up"] = new_level > old_level
    return summary

def _summary(bond: dict) -> dict:
    xp = bond.get("cumulative_xp", 0)
    level = bond.get("level", 1)
    next_xp = next_level_xp_total(xp)
    remaining = next_xp - xp
    pct = round((xp / next_xp) * 100, 1) if next_xp > 0 else 0
    return {
        "level": level,
        "title": get_title(level),
        "xp": xp,
        "xp_to_next": remaining,
        "next_level_xp_total": next_xp,
        "progress_pct": pct,
        "interactions": bond.get("total_interactions", 0),
        "tool_calls": bond.get("total_tool_calls", 0),
        "tasks": bond.get("total_tasks_completed", 0),
        "corrections": bond.get("corrections_learned", 0),
        "skills": bond.get("skills_saved", 0),
        "daily_streak": bond.get("daily_streak", 0),
        "next_unlock": get_next_unlock(level),
        "unlocked_features": bond.get("unlocked_features", []),
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "add":
        xp = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        source = sys.argv[3] if len(sys.argv) > 3 else "tracking"
        event = sys.argv[4] if len(sys.argv) > 4 else "Manual XP add"
        print(json.dumps(add_xp(xp, source, event), indent=2))
    else:
        print(json.dumps(audit(), indent=2))
