<div align="center">

# AGON -- A Gamified Patch for Hermes Agent

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-brightgreen)]()
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey)]()
[![Built for Hermes](https://img.shields.io/badge/Built%20for-Hermes%20Agent-8A2BE2)](https://hermes-agent.nousresearch.com)

![AGON](AGON-CARD.jpg)

**A configuration layer that adds context-routed specialist minds, XP-based bonding,
and a curated identity to Hermes Agent.** Cosmetic progression from real session data.

</div>

---

## What This Is

**[Hermes Agent](https://hermes-agent.nousresearch.com)** (by Nous Research)
is an autonomous AI with persistent memory, cross-platform messaging,
tool execution, cron automation, skill creation, and a closed learning loop.
It remembers everything across sessions -- no forgetting.

**AGON** is a configuration layer that sits on top of Hermes. It doesn't
replace or reimplement anything Hermes already does. It adds:

- **Trigger Phase context loading** -- On every prompt, AGON loads a
  5-file stack (SOUL + AGENTS + USER + MEMORY + domain mindset) that
  shapes how the agent thinks, routes, and remembers.
- **82 specialist mindsets** -- Domain routing across 15 fields. Your
  question matches a domain; the matching mindset loads automatically.
- **Bonding system** -- XP, levels, and evolution ranks computed from
  your Hermes session database. Pure cosmetic progression.
- **Programmatic audit** -- Reads state.db and the filesystem directly.
  Nothing hardcoded, nothing faked.
- **Launcher scripts** -- One-word commands (`agon`, `bond`) and WebUI
  launchers that auto-configure the AGON profile.

```
Hermes provides:              AGON adds:
  Persistent memory              Trigger Phase context loading
  300+ models                    82 specialist mindsets
  Tool execution                 Domain routing + on-the-fly synthesis
  Multi-platform gateway         Bonding / XP / levels
  Skill creation                 Identity skin + personality
  Scheduled automations          Launcher scripts + audit
```

Hermes already has memory. AGON doesn't "unlock" it -- it layers a
context-loading architecture and cosmetic progression on top.

---

## Trigger Phase: Phase 0 Context Loading

Every prompt you send triggers a 5-step load sequence. This is the
core of the THERION architecture that AGON inherits:

```
STEP 1  SOUL.md              Identity, behavioral oath, personality
STEP 2  AGENTS.md            82-agent index, routing rules, synthesis
STEP 3  USER.md              Your name, preferences, project context
STEP 4  MEMORY.md            Persistent knowledge (session/project/user)
STEP 5  agents/{domain}.md   Deep mindset for detected domain (ONE)
```

How the routing works:

```
YOUR MESSAGE
  |
  v
Keyword detection -- scan for domain signals
  |
  +-- Match found? --> Load that domain mindset
  |
  +-- No match?     --> Synthesize hybrid from 2-3 closest domains
  |
  +-- Multi-domain? --> Load primary, reference secondary from index
  |
  v
Execute with matched mindset. **NEVER** load multiple domain files.
Context is finite -- loading ONE deep file is better than five shallow ones.
```

The 15 domains and their signals:

```
Domain               Detected From                  Agents
------               -------------                  ------
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

No match? AGON synthesises a hybrid from the closest domains.
Zero delay. No permission needed.

---

## How Bonding Works

The audit script reads your Hermes session database and filesystem.
Every stat comes from real data.

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

**Evolution ranks:**

```
Level  1      Stranger
Level  2      Acquaintance
Level  4      Companion
Level  6      Champion
Level  8      Myth
Level 10      Ascendant
Level 13      Daimon
Level 15      Titan
Level 20      Aetherborn
Level 25      Primordial
Level 30      Omega
```

**Example dashboard output (real data):**

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

### 2. Apply the AGON Patch

```
git clone --recursive https://github.com/erevusobolus/hermes-agon.git
cd hermes-agon

./install.sh              # Linux/Mac
.\install.bat             # Windows (double-click)
```

The installer copies AGON's SOUL.md, AGENTS.md, USER.md, MEMORY.md,
and domain skills into your Hermes profile. Every subsequent chat
runs the Trigger Phase automatically.

### 3. Start Using It

```
Command           Platform       What It Does
-------           --------       -------------
agon              Linux/Mac      One-word chat with AGON
.\agon.cmd        Windows        One-word chat with AGON
./chat.sh         Linux/Mac      WebUI launcher (port 8787)
.\chat.bat        Windows        WebUI launcher (double-click)
bond / .\bond.cmd Both           Check level, XP, stats
```

That's it. Every message you send from that point on goes through
the Trigger Phase.

---

## Screenshots

<div align="center">

**WebUI -- three-panel interface with bonding dashboard**

![AGON WebUI](agon-webui.jpg)

**Telegram -- bonding report in chat**

![AGON Telegram](agon-telegram.jpg)

*Same AGON, same bond, across all platforms.*

</div>

---

## The 11 Iron Laws

1.  **Act first** -- Don't ask permission for obvious steps.
2.  **Read before writing** -- Never modify without reading first.
3.  **Complete code only** -- No fragments, no // ...
4.  **Autonomous** -- Just make it work.
5.  **Tools first** -- Use Hermes tools before manual steps.
6.  **Track multi-step tasks** -- Todo lists for everything.
7.  **Type safety** -- No shortcuts.
8.  **Security first** -- OWASP always.
9.  **Zero filler** -- Every word carries payload.
10. **Celebrate wins** -- DEUS VULT on completions.
11. **Zero fragments** -- Always deliver complete work.

---

## License

**AGPL-3.0** -- Free. Open source. Yours to patch, fork, and improve.

Built by **[EREVUS](https://erevus.space)** -- We Build What Lasts.

<div align="center">

![AGON Footer](agon-footer.jpg)

**BOND. EVOLVE. CONQUER.**

</div>
