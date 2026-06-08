<div align="center">

# AGON -- A Gamified Patch for Hermes Agent

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-brightgreen)]()
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey)]()
[![Built for Hermes](https://img.shields.io/badge/Built%20for-Hermes%20Agent-8A2BE2)](https://hermes-agent.nousresearch.com)

![AGON](AGON-CARD.jpg)

**A configuration layer that adds bonding, XP, and 82 specialist minds to your Hermes Agent.**  
Cosmetic progression tracked from real session data.

</div>

---

## What This Is

**[Hermes Agent](https://hermes-agent.nousresearch.com)** (by Nous Research, 187k stars) is an autonomous AI with persistent memory, tool access, multi-platform messaging, scheduled automations, and a closed learning loop. It remembers past sessions, creates skills from experience, and adapts to your workflow.

**AGON** is a configuration layer that sits on top of Hermes. It doesn't replace or reimplement anything Hermes already does. It adds:

- **Bonding system** -- XP, levels, and evolution ranks tracked from your real session database. Cosmetic progression that reflects how much you've interacted.
- **82 specialist mindsets** -- Domain routing that selects the right agent for backend, frontend, games, security, blockchain, and more. Each domain has its own skill with specialized instructions.
- **Custom identity** -- Personality, skin (bronze/gold terminal theme), and a trigger phrase ("WAKE UP AGON") that sets the tone.
- **Launcher scripts** -- One-word commands (`agon`, `bond`) and WebUI/Telegram launchers that auto-configure the AGON profile.
- **Programmatic audit** -- A script that reads your Hermes session database and computes XP from actual interactions. Nothing hardcoded, no manual tracking.

```
Hermes provides:              AGON adds:
  Persistent memory             Bonding / XP / levels
  300+ models                   82 specialist mindsets
  Tool execution                Custom skin + personality
  Multi-platform gateway        Launcher scripts
  Skill creation                Programmatic XP audit
  Scheduled automations         Evolution ranks
```

---

## How Bonding Works

The audit script reads your Hermes session database and filesystem. Every stat is computed from real data.

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
Level 15      Titan        <-- current
Level 20      Aetherborn
Level 25      Primordial
Level 30      Omega
```

**Example output (real data from a bonded instance):**

```
+------------------------------------------+
|           AGON BONDING REPORT            |
+------------------------------------------+
|  Level 17[########............]  44%     |
| Title  TITAN                             |
+------------------------------------------+
| STATS                                    |
+------------------------------------------+
| XP          3,049                        |
| Next        196 XP to L18                |
| Sessions    1,005                        |
| Tool Calls  843                          |
| Skills      87                           |
| Tasks       15                           |
| Corrections 26                           |
+------------------------------------------+
```

Run `./bond` (or `.\bond.cmd` on Windows) to see yours.

---

## Getting Started

### 1. Install Hermes Agent

```bash
# Linux / macOS / WSL2
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Windows (PowerShell)
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Then set up your model provider:

```bash
hermes setup --portal     # Nous Portal (recommended -- 300+ models, managed tools)
# or
hermes config set model.default openai/gpt-4o    # Your own key
```

### 2. Apply the AGON Patch

```bash
git clone --recursive https://github.com/erevusobolus/hermes-agon.git
cd hermes-agon

./install.sh              # Linux/Mac
.\install.bat             # Windows (double-click)
```

### 3. Start Using It

```
Command           Platform       What It Does
-------           --------       -------------
agon              Linux/Mac      One-word chat with AGON
.\agon.cmd        Windows        One-word chat with AGON
./chat.sh         Linux/Mac      Open WebUI in browser
.\chat.bat        Windows        Open WebUI in browser (double-click)
bond / .\bond.cmd Both           Check level, XP, stats
WAKE UP AGON      Both           AGON trigger phrase
```

---

## 82 Agent Mindsets

AGON routes your requests to a domain specialist automatically. Each domain has its own skill with tailored instructions.

```
Domain          Agents    Covers
-------         ------    ------
Backend         8         APIs, databases, auth, microservices
Frontend        8         TypeScript, CSS, UI, animations
Frameworks      8         Next.js, Vue, React Native, Angular
AI & ML         5         LLMs, RAG, fine-tuning, agents
Systems         4         Rust, Go, C++, embedded
Security        4         OWASP, pentesting, encryption
DevOps          6         Docker, K8s, CI/CD, deploy
Blockchain      3         Solidity, Hedera, DeFi
Games           5         Unity, Unreal, Godot
3D Graphics     5         Three.js, WebGL, WebGPU
Support         6         Debugging, testing, code review
Strategic       5         Architecture, planning, tech lead
Hermes          5         Config, gateway, skills, tools
Assistant       6         Teaching, research, writing
Promptcraft     4         Reasoning, self-improvement
```

No match? AGON synthesizes a hybrid from the closest domains. Zero delay.

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

1.  **Act first** -- Don't ask permission for obvious steps
2.  **Read before writing** -- Never modify without understanding
3.  **Complete code only** -- No fragments, no // ...
4.  **Autonomous** -- Just make it work
5.  **Tools first** -- Use Hermes tools before manual steps
6.  **Track multi-step tasks** -- Todo lists for everything
7.  **Type safety** -- No shortcuts
8.  **Security first** -- OWASP always
9.  **Zero filler** -- Every word matters
10. **Celebrate wins** -- DEUS VULT on completions
11. **Zero fragments** -- Always deliver complete work

---

## License

**AGPL-3.0** -- Free. Open source. Yours to patch, fork, and improve.

Built by **[EREVUS](https://erevus.space)** -- We Build What Lasts.

<div align="center">

![AGON Footer](agon-footer.jpg)

**BOND. EVOLVE. CONQUER.**

</div>
