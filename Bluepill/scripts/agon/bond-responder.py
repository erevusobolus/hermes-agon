#!/usr/bin/env python3
"""AGON Bond Responder — Telegram-native, no frames, clean ASCII.
Reads bonding.json, prints formatted dashboard to stdout.
Called by gateway handler on /level and /bond commands.
NO box frames — just clean formatted output for Telegram code blocks.
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


TITLES = {
    1: "Stranger", 2: "Acquaintance", 3: "Friend", 4: "Companion",
    5: "Partner", 6: "Champion", 7: "Legend", 8: "Myth",
    9: "Apex", 10: "Ascendant", 11: "Transcendent", 12: "Eternal",
    13: "Daimon", 14: "Olympian", 15: "Titan",
    20: "Aetherborn", 21: "Sidereal", 22: "Nexus",
    23: "Astra", 24: "Verge", 25: "Primordial", 30: "Omega",
}


def _title(lv):
    for k in sorted(TITLES, reverse=True):
        if lv >= k:
            return TITLES[k]
    return "Stranger"


def _xp_for(lv):
    if lv <= 1:
        return 0
    return int(10 * lv * lv + 5)


def _comma(n):
    return "{:,}".format(n)


# ── Clean bar (no frame) ──────────────────────────────────────────────
def _bar(pct, width=16):
    """Clean horizontal bar: `[####....]` style, no side frames."""
    filled = 0
    if pct > 0:
        filled = max(1, int(pct * width / 100))
        if filled > width:
            filled = width
    return "[" + "#" * filled + "." * (width - filled) + "]"


# ── Separators (pure ASCII for Telegram compatibility) ────────────────
SEP = "-" * 36
HDR = "=" * 36


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
    if xp_req <= 0:
        xp_req = 1
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
    lines.append(header)
    lines.append(HDR)
    lines.append("Level {:<3}  {}  {}%".format(lv, bar, pct))
    lines.append("Title   {}".format(title))
    lines.append(SEP)
    lines.append("  XP          {}".format(_comma(xp)))
    lines.append("  Next        {} XP to L{}".format(_comma(remaining), lv + 1))
    lines.append("  Sessions    {}".format(_comma(sessions)))
    lines.append("  Tool Calls  {}".format(_comma(tools)))
    lines.append("  Skills      {}".format(_comma(skills)))
    lines.append("  Tasks       {}".format(_comma(tasks)))
    lines.append("  Corrections {}".format(_comma(corr)))
    if detailed:
        fb = (d.get("first_bonded") or "today")[:10]
        la = (d.get("last_active") or "now")[:10]
        lines.append("  First Bond  {}".format(fb))
        lines.append("  Last Active {}".format(la))
    lines.append(SEP)

    sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()
