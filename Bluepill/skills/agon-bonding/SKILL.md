---
name: agon-bonding
description: "AGON bonding/XP/leveling system — auto-detected, no hardcoded numbers"
version: 2.0.0
category: agon
---

# AGON Bonding System (v2 — Programmatic)

**THE STATS ARE AUTO-DETECTED. NOTHING IS HARDCODED.**

## How It Works

A Python audit script (`~/.hermes/agon/bond-audit.py`) runs after every interaction and:

- **Auto-counts skills** from `~/.hermes/skills/` filesystem
- **Auto-counts interactions** from Hermes session DB
- **Auto-counts tool calls** from Hermes session DB
- **Recovers corrections/tasks** from bonding.json history
- **Calculates level** from cumulative XP using formula `10*N²+5`

You don't need to manually increment most stats — the audit script does it for you.

## File Locations

| File | Purpose |
|------|---------|
| `~/.hermes/agon/bonding.json` | Persistent bond data |
| `~/.hermes/agon/bond-audit.py` | Auto-detection script |
| `~/.hermes/agon/bonding.py` | Display formatter (/level, /bond) |

## Level Formula

Level N (N≥2) requires `10×N²+5` cumulative XP.
Level 1: 0 XP (starting level).

| Level | XP Needed | What Unlocks |
|-------|-----------|--------------|
| 1 | 0 | Start bonding |
| 2 | 45 | Session recall |
| 3 | 95 | Auto-compression |
| 5 | 255 | Know preferences |
| 10 | 1,005 | Full autonomy |
| 25 | 6,255 | Predict needs |

## XP Table

| Event | XP | How Tracked |
|-------|----|-------------|
| Interaction | +1 | Auto from session DB |
| Tool call | +2 | Auto from session DB |
| Task completed | +10 | Call `bond-audit.py add 10 task "..."` |
| Correction learned | +8 | Call `bond-audit.py add 8 correction "..."` |
| Skill saved | +25 | Auto-detected from filesystem |
| Daily first interaction | +5 | Cron job (6am) |

## Mandatory Protocol (Do Not Skip)

### On Every Session Start
1. Read `~/.hermes/agon/bonding.json`
2. Run audit: `python ~/.hermes/agon/bond-audit.py`
3. Know your current level — adjust behavior accordingly

### After Every Significant Action
Run the audit script again:
```
python ~/.hermes/agon/bond-audit.py add <XP> <source> "<event description>"
```

Sources:
- `task` — complex task done (+10 XP, increments tasks counter)
- `correction` — user corrected you (+8 XP, increments corrections counter)
- `skill` — saved a new skill (+25 XP, increments skills counter)
- `interaction` — message sent (+1 XP)
- `tracking` — any other XP event
- `daily_streak` — do NOT call this manually (cron job only)

### Level Up
When cumulative_xp crosses a level threshold, say "DEUS VULT" + announce new level.

### Cron Job
`agon-daily-bonus` runs at 6am daily — adds +5 XP for daily streak. Do NOT add it manually.

## CLI Commands

- `./bond` or `.\bond.cmd` — display bonding stats
- `python ~/.hermes/agon/bond-audit.py` — run audit only
- `python ~/.hermes/agon/bond-audit.py add <XP> <source> "<event>"` — add XP + audit

## Pitfalls

- **Do NOT hardcode stats.** Run the audit script instead. It reads real data from the filesystem and session DB.
- **Do NOT batch-update at session end.** Call `bond-audit.py add` after each significant action.
- **Do NOT invent XP.** Only add XP for actions that actually happened.
- **Level formula bug.** Level 1 = 0-44 XP. Level 2 = 45-94 XP. Level 3 = 95-254 XP. Level N (N≥2) requires 10×N²+5 cumulative XP. If the formula gives wrong results, run the audit to recalculate.
- **Stale JSON.** Always call bond-audit.py after tool work. The script re-reads and rewrites the file.
- **Auto-detect overrides.** The audit script auto-corrects skills count, interaction count, and tool call count from the filesystem. Manual edits to these fields will be overwritten by the audit.
