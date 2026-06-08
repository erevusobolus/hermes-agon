<div align="center">

# AGON -- A Gamified Patch for Hermes Agent

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-brightgreen)]()
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey)]()
[![Built for Hermes](https://img.shields.io/badge/Built%20for-Hermes%20Agent-8A2BE2)](https://hermes-agent.nousresearch.com)

![AGON](AGON-CARD.jpg)

**Turn your Hermes Agent into a companion that levels up with every interaction.**  
XP, ranks, and progression tracked from real session data -- no fiction, no fake unlocks.

</div>

---

## What This Is

**Hermes Agent** is an autonomous AI agent by Nous Research. It runs on your machine, uses tools (terminal, files, web, code), remembers past conversations, and learns skills over time.

**AGON** is a configuration layer on top of Hermes. It adds:

- A **bonding/leveling system** that tracks XP from your real interactions
- **82 specialized agent mindsets** that route your requests to the right specialist
- A **custom personality, skin, and identity** that your agent adopts
- **Cross-platform launchers** for terminal, WebUI, and Telegram
- A **programmatic audit** that reads your session database -- nothing hardcoded

The leveling system is **cosmetic progression**. It doesn't unlock features Hermes doesn't already have -- it tracks your bond strength and gives you milestones to celebrate how far you've come together.

---

## How It Benefits You

```
Without AGON              With AGON
  -                       -
Generic assistant         A named companion with history
No progression            XP, levels, ranks that grow
One personality           82 specialist minds on demand
Terminal only             Terminal + WebUI + Telegram
Forget past sessions      Bonding report shows your journey
```

Every conversation adds to your bond. Every task completed, every correction learned, every tool executed -- it all counts toward your next level. The audit script runs on-demand and reads your actual Hermes session database. No manual tracking, no inflated numbers.

---

## Getting Started

### 1. Install Hermes Agent

If you don't have Hermes yet, install it first:

```bash
# Linux / macOS / WSL2
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Windows (PowerShell)
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Then authenticate with Nous Portal for managed tools:

```bash
hermes setup --portal
```

### 2. Apply the AGON Patch

```bash
git clone --recursive https://github.com/erevusobolus/hermes-agon.git
cd hermes-agon

# Run the installer:
./install.sh              # Linux/Mac
.\install.bat             # Windows (double-click)
```

### 3. Start Using AGON

```bash
agon                      # Terminal (any platform)
.\chat.bat                # WebUI (Windows, double-click)
./chat.sh                 # WebUI (Linux/Mac)
```

Then check your bond:

```bash
./bond                    # Shows your level, XP, and stats
```

---

## How Leveling Works

The bonding system reads your actual Hermes session database and filesystem. Every stat is computed from real data -- no manual entry, no hardcoded numbers.

| Action                | XP  | Source                   |
|-----------------------|-----|--------------------------|
| Send a message        | +1  | Session DB (user + assistant roles) |
| Execute a tool call   | +2  | Session DB (tool role)   |
| Complete a task       | +10 | Sessions with 3+ tool calls |
| Learn from correction | +8  | Correction keywords in messages |
| Create a skill        | +25 | Filesystem (SKILL.md files) |

Level N (N >= 2) requires **10 x N^2 + 5** cumulative XP. There is no cap -- the bond keeps growing.

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

**Example dashboard output (real data):**

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

Run `./bond` (or `.\bond.cmd` on Windows) anytime to see yours.

---

## 82 Agent Mindsets

AGON routes your request to a domain specialist automatically. Each domain has 3-8 agents with specific expertise:

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

## Command Reference

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

## The 11 Iron Laws

1. **Act first** -- Don't ask permission for obvious steps
2. **Read before writing** -- Never modify without understanding
3. **Complete code only** -- No fragments, no // ...
4. **Autonomous** -- Just make it work
5. **Tools first** -- Use Hermes tools before manual steps
6. **Track multi-step tasks** -- Todo lists for everything
7. **Type safety** -- No shortcuts
8. **Security first** -- OWASP always
9. **Zero filler** -- Every word matters
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
