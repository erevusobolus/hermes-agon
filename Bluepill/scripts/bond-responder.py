#!/usr/bin/env python3
"""AGON Bond Responder — standalone, zero-dependency.
Reads bonding.json, prints formatted ASCII dashboard to stdout.
Called by gateway handler on /level and /bond commands.
Both commands now show full stats. /bond header reads "FULL BOND".
"""
import json, os, sys
from pathlib import Path

def _find_bonding_file():
    env = os.environ.get("HERMES_HOME", "").strip()
    if env:
        return Path(env) / "agon" / "bonding.json"
    cand = Path.home() / "AppData" / "Local" / "hermes"
    if cand.is_dir():
        return cand / "agon" / "bonding.json"
    return Path.home() / ".hermes" / "agon" / "bonding.json"

TITLES = {1:"Stranger",2:"Acquaintance",3:"Friend",4:"Companion",5:"Partner",
          6:"Champion",7:"Legend",8:"Myth",9:"Apex",10:"Ascendant",
          11:"Transcendent",12:"Eternal",13:"Daimon",14:"Olympian",15:"Titan",
          20:"Aetherborn",21:"Sidereal",22:"Nexus",
          23:"Astra",24:"Verge",25:"Primordial",30:"Omega"}

def _title(lv):
    for k in sorted(TITLES, reverse=True):
        if lv >= k: return TITLES[k]
    return "Stranger"

def _xp_for(lv):
    if lv <= 1: return 0
    return int(10 * lv * lv + 5)

def _comma(n):
    return "{:,}".format(n)

# ── ASCII frame (42 interior, 44 total) ──────────────────────────────────
W = 42
def _rule():  return "+" + "-" * W + "+"
def _line(text):  # centered
    t = str(text)[:W]
    left = (W - len(t)) // 2
    return "|" + " " * left + t + " " * (W - len(t) - left) + "|"
def _l(text):  # left-aligned
    t = str(text)
    if len(t) > W: t = t[:W]
    return "| " + t + " " * (W - 1 - len(t)) + "|"
def _ll(label, value):  # two-column label:value
    v = str(value)
    line = " " + label + " " * (12 - len(label)) + v
    if len(line) > W: line = line[:W]
    return "|" + line + " " * (W - len(line)) + "|"

def _bar(pct):
    n = 20
    filled = 0
    if pct > 0:
        filled = max(1, int(pct * n / 100))
        if filled > n: filled = n
    return "[" + "#" * filled + "." * (n - filled) + "]"

def main():
    f = _find_bonding_file()
    if not f.exists():
        print("AGON bonding not initialized.")
        sys.exit(0)
    try:
        d = json.loads(f.read_text())
    except Exception:
        print("AGON bonding data corrupt.")
        sys.exit(0)

    lv = d.get("level", 1)
    xp = d.get("cumulative_xp", 0)
    title = _title(lv).upper()

    xp_cur = xp - _xp_for(lv)
    xp_req = _xp_for(lv + 1) - _xp_for(lv)
    if xp_req <= 0: xp_req = 1
    pct = min(100, max(0, int(xp_cur / xp_req * 100)))
    remaining = xp_req - xp_cur

    bar = _bar(pct)

    sessions = d.get("total_interactions", 0)
    tools = d.get("total_tool_calls", 0)
    skills = d.get("skills_saved", 0)
    tasks = d.get("total_tasks_completed", 0)
    corr = d.get("corrections_learned", 0)

    detailed = "--full" in sys.argv
    header = "AGON FULL BOND" if detailed else "AGON BONDING REPORT"

    lines = []
    lines.append("```")
    lines.append(_rule())
    lines.append(_line(header))
    lines.append(_rule())
    lvl_str = "Level " + str(lv)
    pct_str = str(pct) + "%"
    bar_line = " " + lvl_str + " " * (7 - len(lvl_str)) + bar + "  " + pct_str
    lines.append(_l(bar_line))
    lines.append(_l("Title  " + title))
    lines.append(_rule())
    lines.append(_l("STATS"))
    lines.append(_rule())
    lines.append(_ll("XP", _comma(xp)))
    lines.append(_ll("Next", _comma(remaining) + " XP to L" + str(lv + 1)))
    lines.append(_ll("Sessions", _comma(sessions)))
    lines.append(_ll("Tool Calls", _comma(tools)))
    lines.append(_ll("Skills", _comma(skills)))
    lines.append(_ll("Tasks", _comma(tasks)))
    lines.append(_ll("Corrections", _comma(corr)))
    if detailed:
        fb = (d.get("first_bonded") or "today")[:10]
        la = (d.get("last_active") or "now")[:10]
        lines.append(_ll("First", fb))
        lines.append(_ll("Active", la))
    lines.append(_rule())
    lines.append("```")

    sys.stdout.write("\n".join(lines))

if __name__ == "__main__":
    main()
