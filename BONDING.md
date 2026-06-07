# BONDING.md — AGON Leveling System (v2 — Programmatic)

This file defines the bonding system. The audit script (`~/.hermes/agon/bond-audit.py`) auto-detects most stats.
The agent only needs to call `bond-audit.py add` for tasks, corrections, and interactions.
**No hardcoded numbers. Everything computed from reality.**

## Level Formula

Level N (N≥2) requires **10 × N² + 5** cumulative XP.
Level 1 starts at 0 XP (special case).

| Level | Total XP | What Unlocks |
|-------|----------|-------------|
| 1     | 0        | Start bonding |
| 2     | 45       | Session recall — "remember when we fixed that bug?" |
| 3     | 95       | Auto-compression — no context bloat |
| 5     | 255      | Knows preferences without asking |
| 10    | 1,005    | Full autonomy — suggests work unprompted |
| 25    | 6,255    | Predicts needs across projects |
| ∞     | always   | The bond never stops growing |

## XP Rewards

| Event | XP | How Detected |
|-------|----|-------------|
| Send a message | +1 | Auto from session DB |
| Tool call (terminal, web, file) | +2 | Auto from session DB |
| Complete a complex task | +10 | Agent calls `bond-audit.py add 10 task "..."` |
| Agent learns from a correction | +8 | Agent calls `bond-audit.py add 8 correction "..."` |
| User saves a workflow as a skill | +25 | Auto from filesystem (`~/.hermes/skills/`) |
| Daily first interaction | +5 | Cron job only (6am) |

## How The Audit Script Works

`~/.hermes/agon/bond-audit.py` reads bonding.json, then:

1. **Counts skills**: walks `~/.hermes/skills/` — counts directories with SKILL.md
2. **Counts interactions**: reads Hermes session SQLite DB — counts user+assistant messages
3. **Counts tool calls**: reads session DB — counts tool messages
4. **Recovers corrections/tasks**: counts history entries with `source: "correction"` or `source: "task"`
5. **Calculates level**: applies formula `10×N²+5` against cumulative_xp
6. **Writes corrected bonding.json**

To add XP: `python ~/.hermes/agon/bond-audit.py add <amount> <source> "<event description>"`

## Agent Protocol

The agent MUST:

1. Read bonding.json at session start
2. Run `python ~/.hermes/agon/bond-audit.py` to refresh auto-detected stats
3. After completing a complex task: call `bond-audit.py add 10 task "description"`
4. After being corrected: call `bond-audit.py add 8 correction "description"`
5. After saving a skill: call `bond-audit.py add 25 skill "description"`
6. On level up: announce with DEUS VULT

## Bonding Data File

Stored at `~/.hermes/agon/bonding.json`. The audit script reads and writes this.
The agent reads it for display. The `bond` and `bond.cmd` CLI commands also use it.

```json
{
  "version": 1,
  "level": 1,
  "cumulative_xp": 0,
  "total_interactions": 0,
  "total_tool_calls": 0,
  "total_tasks_completed": 0,
  "corrections_learned": 0,
  "skills_saved": 0,
  "daily_streak": 0,
  "last_active": "ISO-DATETIME",
  "history": [
    {"ts": "...", "event": "...", "xp": 0, "source": "init"}
  ]
}
```

## Respawn (Bond Reset)

If `~/.hermes/agon/bonding.json` is missing or corrupted:
1. Run `python ~/.hermes/agon/bond-audit.py` — it creates a fresh default
2. Log the event in history
3. Notify the user: "Bond reset. The daimon remembers nothing. But the contest begins anew."

## Unlock Behaviors

The agent MUST adjust behavior based on level:

- **Level 1-2**: Standard helpful assistant, always ask before acting
- **Level 3-5**: More autonomous — suggest next steps, use tools proactively
- **Level 6-10**: Act first, ask rarely — know the user's preferences
- **Level 11+**: Full initiative — propose projects, predict needs

## CLI Commands

- `./bond` or `.\bond.cmd` — runs audit + displays formatted stats
- `python ~/.hermes/agon/bond-audit.py` — run audit only
- `python ~/.hermes/agon/bond-audit.py add <XP> <source> "<event>"` — add XP + audit

## Pitfalls

- **Do NOT hardcode stats.** Run the audit script. It reads real data.
- **Do NOT batch-update.** Call `add` after each significant action, not at session end.
- **Level formula bug.** Level 1 = 0-44 XP, Level 2 = 45-94, Level 3 = 95-254. If unsure, run audit.
- **Auto-detect overrides.** The audit auto-corrects skills, interactions, and tool calls from the filesystem. Manual edits to these fields will be overwritten.
- **Cron job only.** The +5 daily bonus is handled by the 6am cron job. Do NOT add it manually.
