<div align="center">

# ⚔ AGON — Your AI Levels Up With You

**Your Hermes Agent becomes an RPG companion that grows stronger with every interaction.**

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-brightgreen)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey)]()
[![Hermes](https://img.shields.io/badge/Hermes-Agent-8A2BE2)](https://hermes-agent.nousresearch.com)
[![Stars](https://img.shields.io/github/stars/erevusobolus/hermes-agon?style=social)](https://github.com/erevusobolus/hermes-agon)

![AGON](AGON-CARD.jpg)

**Not a bot. Not a wrapper. A patch that turns your AI into a partner with XP, levels, and 82 specialized minds.**

</div>

<br>

**Table of Contents**
- [The Pitch — Why AGON?](#-the-pitch--why-agon)
- [See It In Action](#-see-it-in-action)
- [Quick Start](#-quick-start)
- [How Bonding Works](#-how-bonding-works)
- [82 Agent Mindsets](#-82-agent-mindsets)
- [Command Reference](#-command-reference)
- [The 11 Iron Laws](#-the-11-iron-laws)
- [License](#-license)

---

## 🔥 The Pitch — Why AGON?

Every conversation with Hermes normally just... ends. No history. No growth. No stakes.

**AGON changes that.**

```bash
# Your AI remembers. Grows. Levels up.
$ agon
>> AGON active. 82 minds ready. You are Level 17 — Titan.
>> 196 XP to next level. DEUS VULT.
```

**What AGON gives you:**

| What | Why It Matters |
|------|----------------|
| 🎮 **XP & Levels** | Every message gives XP. Every task levels you up. Infinite progression — no cap. |
| 🧠 **82 Minds** | Not one AI — 82 specialists. Backend, frontend, games, blockchain, security. Routes automatically. |
| 📈 **Bonding System** | Real stats from your actual sessions. Tasks, corrections, skills — all tracked programmatically. |
| 🖥️ **Works Everywhere** | Telegram, WebUI, terminal. Same bond, same level, all platforms. |
| 🛠️ **Full Tool Access** | Code execution, file system, web research, browser automation, image generation. |
| 🔥 **Digimon Evolution** | Level 1 Stranger → Level 30 Omega. You raise your AI like a partner — it earns its evolutions. |

> Built by **[EREVUS](https://erevus.space)** — We Build What Lasts.

---

## 📸 See It In Action

<div align="center">

**WebUI — Full chat interface with bonding dashboard**

![AGON WebUI](agon-webui.jpg)

**Telegram — Bonding report in chat, live**

![AGON Telegram](agon-telegram.jpg)

*Available on WebUI, Telegram, and terminal — same AGON, same bond.*

</div>

---

## 🚀 Quick Start

**Prerequisites:** [Hermes Agent](https://hermes-agent.nousresearch.com) installed, [Nous subscription](https://nousresearch.com) (for managed tools), and Python 3.11+.

```bash
# Clone the repo
git clone --recursive https://github.com/erevusobolus/hermes-agon.git
cd hermes-agon

# Install (choose your platform):
./install.sh              # Linux/Mac
.\install.bat             # Windows (double-click)
powershell -ExecutionPolicy Bypass -File install.ps1  # Windows (terminal)

# Start chatting:
agon                      # Terminal
./chat.sh                 # WebUI (Linux/Mac)
.\chat.bat                # WebUI (Windows, double-click)
```

**One-liner (Hermes already installed):**
```bash
curl -fsSL https://raw.githubusercontent.com/erevusobolus/hermes-agon/main/install.sh | bash
```

---

## 📈 How Bonding Works

Every interaction with AGON earns XP. Stats are **auto-detected** from your session database — nothing is hardcoded, nothing is faked.

| Action | XP | How It's Tracked |
|--------|----|-------------------|
| Send a message | +1 | Auto-detected from session DB |
| Tool call (terminal, web, file) | +2 | Auto-detected from session DB |
| Complete a complex task | +10 | Sessions with 3+ tool calls |
| AGON learns from a correction | +8 | Correction keywords in messages |
| Save a workflow as a skill | +25 | Auto-detected from filesystem |

**Level formula:** Level N (N≥2) requires **10 × N² + 5** cumulative XP. No cap — there's always a next level.

```bash
# Check your bond anytime:
./bond        # Linux/Mac
.\bond.cmd    # Windows
```

**Example output (real, from actual sessions):**
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

**Evolution stages:** Stranger → Acquaintance → Friend → Companion → Partner → Champion → Legend → Myth → Apex → Ascendant → Transcendent → Eternal → Daimon → Olympian → **Titan** → Aetherborn → Primordial → **Omega**

---

## 🏛 82 Agent Mindsets

AGON doesn't use one AI. It routes your request to the right specialist — automatically.

| Domain | Agents | For When You Need... |
|--------|--------|----------------------|
| Backend | 8 | APIs, databases, auth, microservices |
| Frontend | 8 | TypeScript, CSS, UI, animations |
| Frameworks | 8 | Next.js, Vue, React Native, Angular |
| AI & ML | 5 | LLMs, RAG, fine-tuning, agents |
| Systems | 4 | Rust, Go, C++, embedded |
| Security | 4 | OWASP, pentesting, encryption |
| DevOps | 6 | Docker, K8s, CI/CD, deploy |
| Blockchain | 3 | Solidity, Hedera, DeFi |
| Games | 5 | Unity, Unreal, Godot |
| 3D Graphics | 5 | Three.js, WebGL, WebGPU |
| Support | 6 | Debugging, testing, code review |
| Strategic | 5 | Architecture, planning, tech lead |
| Hermes | 5 | Config, gateway, skills, tools |
| Assistant | 6 | Teaching, research, writing |
| Promptcraft | 4 | Reasoning, self-improvement |

**No direct match?** AGON synthesizes a hybrid from the closest domains. Zero delay. Zero friction.

---

## ⌨️ Command Reference

| Command | Platform | What It Does |
|---------|----------|--------------|
| `agon` | Linux/Mac | One-word chat with AGON |
| `.\agon.cmd` | Windows | One-word chat with AGON |
| `./chat.sh` | Linux/Mac | Open WebUI in browser |
| `.\chat.bat` | Windows | Open WebUI in browser |
| `bond` / `.\bond.cmd` | Both | Check level, XP, stats |
| `WAKE UP AGON` | Both | AGON trigger phrase |
| `hermes -p AGON chat` | Both | Terminal with AGON profile |

---

## 📜 The 11 Iron Laws

1. **Act first** — Don't ask permission for obvious steps
2. **Read before writing** — Never modify without understanding
3. **Complete code only** — No fragments, no `// ...`
4. **Autonomous** — Just make it work
5. **Tools first** — Use Hermes tools before manual steps
6. **Track multi-step tasks** — Todo lists for everything
7. **Type safety** — No shortcuts
8. **Security first** — OWASP always
9. **Zero filler** — Every word matters
10. **Celebrate wins** — DEUS VULT on completions
11. **Zero fragments** — Always deliver complete work

---

## 📄 License

**AGPL-3.0** — Free. Open source. Yours to patch, fork, and improve.

Built by **[EREVUS](https://erevus.space)** — We Build What Lasts.

<div align="center">

![AGON Footer](agon-footer.jpg)

**BOND. EVOLVE. CONQUER.**

</div>
