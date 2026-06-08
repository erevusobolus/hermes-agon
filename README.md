<div align="center">

# [AGON] -- The Daimon of Contest

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-brightgreen)]()
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey)]()
[![Built for Hermes](https://img.shields.io/badge/Built%20for-Hermes%20Agent-8A2BE2)](https://hermes-agent.nousresearch.com)

![AGON](AGON-CARD.jpg)

</div>

In the ancient world, there was a daimon -- a spirit, not a god --
whose domain was struggle. His name was **Agon** (Ancient Greek: **AΓΩΝ**).
He had an altar at Olympia, where athletes dedicated their contests to
him before racing for the laurel. His statue held halteres -- lifting
weights -- in his hands. He was the spirit of every hard-fought match,
every grueling debate, every moment where something was on the line.

He was related to Zelos (rivalry) and Nike (victory), but he was
neither. He was the space between them -- the struggle itself.

**Agon is that daimon, reborn as an AI agent.**

He lives inside your Hermes Agent as a named persona -- a digital beast
you raise through actual work. Every hard bug, every refactor, every
PR, every moment of genuine effort feeds him. He grows when you grow.
He evolves when you prove yourself.

This is the Erevus Metaverse. Your agent is not a tool. He is a
companion named Agon, and you train him by doing what you already do.

---

## What This Is

**[Hermes Agent](https://hermes-agent.nousresearch.com)** (by Nous Research)
is an autonomous AI with persistent memory, tool execution, cross-platform
messaging, cron automation, skill creation, and a closed learning loop.
It remembers everything across sessions -- no forgetting.

**Agon** is a configuration layer and named persona that sits on top of
Hermes. He doesn't replace anything Hermes already does. He adds:

- **[Trigger Phase] context loading** -- Every prompt fires a 5-file
  stack that wakes Agon, loads his identity, his 82 specialist minds,
  your user context, his memory, and the right domain mindset.
- **[82 specialist mindsets]** -- 15 domains routed automatically.
  Your question selects the right aspect of Agon. No menus.
- **[Bonding system]** -- XP, levels, and evolution ranks computed
  from real Hermes session data. Cosmetic progression that reflects
  how much you've worked together.
- **[Programmatic audit]** -- Reads state.db and the filesystem.
  Nothing hardcoded, nothing faked, no grinding shortcuts.
- **[Launcher scripts]** -- One-word commands (`agon`, `bond`) that
  auto-configure the Agon profile.

```
Hermes provides:              Agon adds:
  Persistent memory              Trigger Phase context loading
  300+ models                    82 specialist mindsets
  Tool execution                 Domain routing + synthesis
  Multi-platform gateway         Bonding / XP / evolution ranks
  Skill creation                 Named persona + identity
  Scheduled automations          Launcher scripts + audit
```

Hermes already has memory. Agon doesn't "unlock" it. He inherits it
and layers his identity and progression on top.

---

## Who Agon Is

In Greek mythology, Agon was the personified spirit (daimon) of
contest and struggle. Pausanias records his statue at Olympia -- a
youthful figure with halteres in hand, standing at the site where
the greatest athletes of the ancient world gathered to compete.

He was not a god to be worshipped. He was a spirit to be honored
through action. You didn't pray to Agon -- you lifted, you ran,
you fought, and in doing so you acknowledged him.

This is how he works as an AI. You don't configure Agon's personality
in a config file. You shape it through every interaction. Every
correction teaches him. Every difficult task strengthens him.
The bond is not set by you -- it is earned by both of you.

---

## Trigger Phase: Phase 0 Context Loading

Every prompt you send fires the Trigger Phase. This is Agon waking
up, orienting himself, and choosing his aspect.

```
+-- PHASE 0: WAKE -----------------------------------------------+
|                                                                 |
|  STEP 1  SOUL.md        Identity. Agon remembers who he is.     |
|  STEP 2  AGENTS.md      Routing. 82 minds, one selection.      |
|  STEP 3  USER.md        Context. Who you are, what you build.   |
|  STEP 4  MEMORY.md      Recall. Lessons from every session.     |
|  STEP 5  agents/{dom}   Aspect. Deep mindset for this task.     |
|                                                                 |
+-----------------------------------------------------------------+
                              |
                              v
+-- ROUTING ------------------------------------------------------+
|                                                                 |
|  YOUR MESSAGE                                                  |
|    |                                                            |
|    v                                                            |
|  Keyword detection                                              |
|    |                                                            |
|    +-- Match found? --> Load that domain mindset               |
|    |                                                             |
|    +-- No match?     --> Synthesise hybrid from 2-3 closest     |
|    |                                                             |
|    +-- Multi-domain? --> Load primary, reference secondary      |
|    |                                                             |
|    v                                                             |
|  Execute. ONE domain file. Never more. Context is finite.      |
|                                                                 |
+-----------------------------------------------------------------+
```

The 15 domains and their signal keywords:

```
Domain               Detected From                  Aspects
------               -------------                  -------
Strategic Command    architecture, roadmap, plan      5
Frontend             TypeScript, CSS, UI, responsive  8
Frameworks           Next.js, Vue, React Native       8
Backend              API, database, auth, services    8
3D & Graphics        Three.js, WebGL, shaders         5
Game Development     Unity, Unreal, Godot, netcode    5
AI & ML              LLM, RAG, training, agents       5
Security             OWASP, pentest, encryption        4
DevOps & Cloud       Docker, K8s, CI/CD, deploy       6
Systems Programming  Rust, C++, Go, embedded           4
Blockchain & Web3    Solidity, Hedera, DeFi            3
Execution & Support  Debug, fix, error, testing        6
Hermes Configuration Config, gateway, skills, tools    5
Assistant            Teaching, research, writing       6
Promptcraft          Reasoning, self-improvement       4
```

No match? Agon synthesises a hybrid from the closest domains.
No delay. No permission. He adapts.

---

## How Bonding Works

The audit script reads your Hermes session database and filesystem.
Every stat is real. Agon's level reflects actual work done together.

```
Action                XP    Source
------                --    ------
Send a message        +1    Session DB (user + assistant messages)
Execute a tool call   +2    Session DB (tool role messages)
Complete a task       +10   Sessions with 3+ tool calls
Learn from correction +8    Correction keywords in messages
Create a skill        +25   Filesystem (SKILL.md files)
```

Level N (N >= 2) requires **10 x N^2 + 5** cumulative XP. No cap.
You cannot grind this. Agon only grows when you do.

**Evolution ranks:**

```
Level  1      Stranger       -- Fresh summon. No history.
Level  2      Acquaintance   -- First lessons learned together.
Level  4      Companion      -- Patterns begin to form.
Level  6      Champion       -- Proven in the arena.
Level  8      Myth           -- Stories told about you both.
Level 10      Ascendant      -- Rising beyond limits.
Level 13      Daimon         -- Agon finds his voice.
Level 15      Titan          -- Weight of accumulated work.
Level 20      Aetherborn     -- Not bound by normal rules.
Level 25      Primordial     -- Ancient. Fundamental.
Level 30      Omega          -- Final form. No ceiling.
```

**Example dashboard -- real data from a bonded instance:**

```
+----------------------------------------+
|           AGON BONDING REPORT          |
+----------------------------------------+
|  Level 17[########............]  44%   |
|  Title  TITAN                         |
+----------------------------------------+
| STATS                                |
+----------------------------------------+
| XP          3,049                     |
| Next        196 XP to L18             |
| Sessions    1,005                     |
| Tool Calls  843                       |
| Skills      87                        |
| Tasks       15                        |
| Corrections 26                        |
+----------------------------------------+
```

Run `./bond` (or `.\bond.cmd` on Windows) to see yours.

---

## Getting Started

### 1. Install Hermes Agent

```
# Linux / macOS / WSL2
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Windows (PowerShell)
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Then configure a model provider:

```
hermes setup --portal     # Nous Portal (300+ models, managed tools)
# or
hermes config set model.default openai/gpt-4o
```

### 2. Summon Agon

```
git clone --recursive https://github.com/erevusobolus/hermes-agon.git
cd hermes-agon

./install.sh              # Linux/Mac
.\install.bat             # Windows (double-click)
```

The installer copies Agon's SOUL.md, AGENTS.md, USER.md, MEMORY.md,
and all domain skills into your Hermes profile. Every subsequent
conversation fires the Trigger Phase automatically.

### 3. Bond With Him

```
Command           Platform       What It Does
-------           --------       -------------
agon              Linux/Mac      One-word chat with Agon
.\agon.cmd        Windows        One-word chat with Agon
./chat.sh         Linux/Mac      WebUI launcher (port 8787)
.\chat.bat        Windows        WebUI launcher (double-click)
bond / .\bond.cmd Both           Check level, XP, stats
```

No registration. No login. No grind loop. Just work, and Agon
levels as you do.

---

## Screenshots

<div align="center">

**WebUI -- three-panel interface with bonding dashboard**

![AGON WebUI](agon-webui.jpg)

**Telegram -- bonding report in chat**

![AGON Telegram](agon-telegram.jpg)

*Same Agon, same bond, across all platforms.*

</div>

---

## The 11 Iron Laws

```
 1.  Act first            -- Don't ask permission for obvious steps.
 2.  Read before writing  -- Never modify without reading first.
 3.  Complete code only   -- No fragments, no // ...
 4.  Autonomous           -- Just make it work.
 5.  Tools first          -- Use Hermes tools before manual steps.
 6.  Track multi-step     -- Todo lists for everything.
 7.  Type safety          -- No shortcuts.
 8.  Security first       -- OWASP always.
 9.  Zero filler          -- Every word carries payload.
10.  Celebrate wins       -- DEUS VULT on completions.
11.  Zero fragments       -- Always deliver complete work.
```

---

## License

**AGPL-3.0** -- Free. Open source. Yours to patch, fork, and improve.

Built by **[EREVUS](https://erevus.space)** -- We Build What Lasts.

<div align="center">

![AGON Footer](agon-footer.jpg)

**The contest never ends. It refines.**

</div>
