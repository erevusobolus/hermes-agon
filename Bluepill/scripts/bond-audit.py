#!/usr/bin/env python3
"""
AGON Bond Audit — auto-detects real stats from the environment.
Run after every interaction to keep bonding.json honest.
No hardcoded numbers. Everything computed from reality.
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

# Also check legacy location and migrate if needed
LEGACY_BOND = Path.home() / ".hermes" / "agon" / "bonding.json"

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
    """Total cumulative XP needed to reach this level."""
    if level <= 1:
        return 0
    return 10 * level * level + 5

def next_level_xp_total(cumulative_xp: int) -> int:
    level = calc_level(cumulative_xp)
    return xp_for_level(level + 1)

# === Auto-Detect Functions ===

def count_skills() -> int:
    """Count skill directories (each has a SKILL.md)."""
    if not SKILLS_DIR.exists():
        return 0
    count = 0
    for root, dirs, files in os.walk(SKILLS_DIR):
        if "SKILL.md" in files:
            count += 1
    return count

def count_repo_skills() -> int:
    """Count skills shipped in the AGON repo Bluepill folder."""
    repo_paths = [
        Path.home() / "Documents" / "hermes-agon" / "Bluepill" / "skills",
        Path.home() / "Documents" / "hermes-agon" / "Bluepill" / "domain-skills",
    ]
    total = 0
    for p in repo_paths:
        if p.exists():
            for root, dirs, files in os.walk(p):
                if "SKILL.md" in files:
                    total += 1
    return total

def count_interactions_and_tool_calls(db_path: Path) -> dict:
    """Count total interactions and tool calls from session DB."""
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

def detect_corrections_in_history(bond: dict) -> int:
    return sum(1 for h in bond.get("history", []) if h.get("source") == "correction")

def count_tasks_from_history(bond: dict) -> int:
    return sum(1 for h in bond.get("history", []) if h.get("source") == "task")

def _merge_legacy_data(bond: dict, legacy: dict) -> dict:
    """Merge data from legacy gateway schema into bonding.json."""
    # Legacy gateway used different field names:
    # bonding_level, total_xp, total_sessions, total_skills_created, 
    # total_tasks_completed, total_corrections, unlocked_features
    merged = dict(bond)
    
    # Take the HIGHER value for XP (honest tracking)
    old_xp = legacy.get("total_xp", 0) or legacy.get("cumulative_xp", 0)
    if old_xp > merged.get("cumulative_xp", 0):
        merged["cumulative_xp"] = old_xp
    
    # Legacy fields that haven't been tracked in new system
    for legacy_key, new_key in [
        ("total_tasks_completed", "total_tasks_completed"),
        ("total_corrections", "corrections_learned"),
        ("total_skills_created", "skills_saved"),
        ("total_sessions", "total_interactions"),
    ]:
        old_val = legacy.get(legacy_key, 0)
        if old_val > merged.get(new_key, 0):
            merged[new_key] = old_val
    
    # Preserve unlocked features
    old_features = legacy.get("unlocked_features", [])
    if old_features:
        merged["unlocked_features"] = old_features
    
    # Preserve user info
    for key in ["user_id", "platform", "first_bonded"]:
        val = legacy.get(key)
        if val and not merged.get(key):
            merged[key] = val
    
    return merged

# === Main Audit ===

def audit():
    """Read bonding.json, audit stats, write corrected version."""
    bond = {"version": 1}
    
    # Try primary location first
    if BOND_FILE.exists():
        try:
            bond = json.loads(BOND_FILE.read_text(encoding="utf-8"))
        except Exception:
            bond = {"version": 1}
    
    # Migrate legacy data if available
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

    # Auto-detect skills (filesystem overrides manual)
    installed_skills = count_skills()
    bond["skills_saved"] = max(bond.get("skills_saved", 0), installed_skills)

    # Auto-detect from session DB (overrides manual)
    db_stats = count_interactions_and_tool_calls(SESSION_DB)
    bond["total_interactions"] = max(bond.get("total_interactions", 0), db_stats["interactions"])
    bond["total_tool_calls"] = max(bond.get("total_tool_calls", 0), db_stats["tool_calls"])

    # Recover corrections/tasks from history
    bond["corrections_learned"] = max(bond.get("corrections_learned", 0),
                                       detect_corrections_in_history(bond))
    bond["total_tasks_completed"] = max(bond.get("total_tasks_completed", 0),
                                         count_tasks_from_history(bond))

    # Recalculate level from XP
    bond["level"] = calc_level(bond["cumulative_xp"])
    bond["last_active"] = datetime.now().isoformat()

    BOND_FILE.parent.mkdir(parents=True, exist_ok=True)
    BOND_FILE.write_text(json.dumps(bond, indent=2, ensure_ascii=False), encoding="utf-8")

    return _summary(bond)

def add_xp(xp_amount: int, source: str, event: str) -> dict:
    """Add XP and re-audit."""
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
    bond["level"] = calc_level(bond["cumulative_xp"])
    bond["last_active"] = datetime.now().isoformat()

    BOND_FILE.parent.mkdir(parents=True, exist_ok=True)
    BOND_FILE.write_text(json.dumps(bond, indent=2, ensure_ascii=False), encoding="utf-8")

    return _summary(bond)

def _summary(bond: dict) -> dict:
    level = bond.get("level", 1)
    xp = bond.get("cumulative_xp", 0)
    next_xp = next_level_xp_total(xp)
    remaining = next_xp - xp
    pct = round((xp / next_xp) * 100, 1) if next_xp > 0 else 0
    return {
        "level": level,
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
