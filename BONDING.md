# BONDING.md — AGON Leveling System

This file defines the bonding system. The agent MUST read this on every session start.

## Level Formula

Level **N** requires **floor(10 × N²) + 5** total XP from level 0.
XP to next level: `floor(10 × (current_level + 1)²) + 5 - cumulative_xp`

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

| Event | XP |
|-------|----|
| Send a message | +1 |
| Tool call (terminal, web, file) | +2 |
| Complete a complex task | +10 |
| Agent learns from a correction | +8 |
| User saves a workflow as a skill | +25 |
| Daily first interaction | +5 |

## Bonding Data File

Stored at `~/.hermes/agon/bonding.json`. The agent MUST:
- **Read** this file at the start of every session
- **Update** this file after every significant interaction
- **Append** to `history` with every XP change

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
1. Create default with level 1, 0 XP
2. Log the event in history
3. Notify the user: "Bond reset. The daimon remembers nothing. But the contest begins anew."

## Unlock Behaviors

The agent MUST adjust behavior based on level:

- **Level 1-2**: Standard helpful assistant, always ask before acting
- **Level 3-5**: More autonomous — suggest next steps, use tools proactively
- **Level 6-10**: Act first, ask rarely — know the user's preferences
- **Level 11+**: Full initiative — propose projects, predict needs
