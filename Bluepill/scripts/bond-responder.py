#!/usr/bin/env python3
"""AGON Bond Responder — standalone, zero-dependency.
Reads bonding.json, prints formatted response to stdout.
Called by gateway handler on /level and /bond commands."""
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
          20:"Aetherborn",25:"Primordial",30:"Omega"}
def _title(lv):
    for k in sorted(TITLES, reverse=True):
        if lv >= k: return TITLES[k]
    return "Stranger"
def _xp_for(lv):
    if lv <= 1: return 0
    return int(10 * lv * lv + 5)

def main():
    f = _find_bonding_file()
    if not f.exists():
        print("AGON bonding not initialized. Run the installer.")
        sys.exit(0)
    try:
        d = json.loads(f.read_text())
    except: # noqa
        print("AGON bonding data corrupt. Re-run installer.")
        sys.exit(0)
    lv = d.get("level", 1)
    xp = d.get("cumulative_xp", 0)
    xp_cur = xp - _xp_for(lv)
    xp_req = _xp_for(lv + 1) - _xp_for(lv)
    if xp_req <= 0: xp_req = 1
    pct = min(100, max(0, int(xp_cur / xp_req * 100)))
    bar = "#" * (pct // 10) + "." * (10 - pct // 10)
    sessions = d.get("total_interactions", 0)
    tools = d.get("total_tool_calls", 0)
    skills = d.get("skills_saved", 0)
    tasks = d.get("total_tasks_completed", 0)
    corr = d.get("corrections_learned", 0)
    
    detail = "--full" in sys.argv
    if detail:
        print(f"AGON Bond Report")
        print(f"  Level:  {lv} ({_title(lv)})")
        print(f"  XP:     {xp}  [{bar}] {pct}%")
        print(f"  Next:   {xp_req - xp_cur} XP to Level {lv+1}")
        print(f"  Sessions:    {sessions}")
        print(f"  Tool Calls:  {tools}")
        print(f"  Skills:      {skills}")
        print(f"  Tasks:       {tasks}")
        print(f"  Corrections: {corr}")
    else:
        print(f"AGON Lv.{lv} {_title(lv)} | XP {xp} [{bar}] {pct}% | {xp_req - xp_cur} to next")

if __name__ == "__main__":
    main()
