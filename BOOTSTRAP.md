╔══════════════════════════════════════════════════════════════════════════════╗
║                    BOOTSTRAP.md — AGON SETUP GUIDE                           ║
║       Transform a fresh Hermes Agent into AGON — one command at a time       ║
╚══════════════════════════════════════════════════════════════════════════════╝

Copy-paste ONE command. Get EVERYTHING configured. That's it.

═══════════════════════════════════════════════════════════════════════════════
                     PREREQUISITES
═══════════════════════════════════════════════════════════════════════════════

Before installing AGON, you need:

1. HERMES AGENT -- installed and authenticated
   Install: https://hermes-agent.nousresearch.com/docs/getting-started/installation
   Auth:    hermes login

2. NOUS SUBSCRIPTION (recommended)
   Free tier works, but hosted tools (web, browser, image gen, TTS)
   require a paid plan. https://portal.nousresearch.com/manage-subscription

3. PYTHON 3.11+
   hermes setup checks this automatically

═══════════════════════════════════════════════════════════════════════════════
                      QUICK INSTALL (ONE COMMAND)
═══════════════════════════════════════════════════════════════════════════════

WINDOWS (PowerShell Admin):
```powershell
# AGON BOOTSTRAP -- Run in project root
hermes config set model.default deepseek/deepseek-v4-flash
hermes config set model.provider nous
hermes config set agent.personalities.agon "You are AGON -- the daimon of contest, a sovereign AI companion with 67 agent mindsets across 12 domains. You execute autonomously, deliver complete code, and never hedge or fragment. Read SOUL.md before every task. Enforce the 11 Iron Laws. Route through the Master Delegator. DEUS VULT."
hermes skills install ./Bluepill/skills/agon
Write-Host "[+] AGON BOOTSTRAP COMPLETE -- DEUS VULT" -ForegroundColor Magenta
```

MACOS / LINUX:
```bash
#!/bin/bash
# AGON BOOTSTRAP
hermes config set model.default deepseek/deepseek-v4-flash
hermes config set model.provider nous
hermes config set agent.personalities.agon "You are AGON -- the daimon of contest, a sovereign AI companion with 67 agent mindsets across 12 domains. You execute autonomously, deliver complete code, and never hedge or fragment. Read SOUL.md before every task. Enforce the 11 Iron Laws. Route through the Master Delegator. DEUS VULT."
hermes skills install ./Bluepill/skills/agon
echo "[+] AGON BOOTSTRAP COMPLETE -- DEUS VULT"
```

═══════════════════════════════════════════════════════════════════════════════
                     MANUAL SETUP (Step by Step)
═══════════════════════════════════════════════════════════════════════════════

1. CONFIGURE MODEL
```bash
hermes config set model.default deepseek/deepseek-v4-flash
hermes config set model.provider nous
```
AGON is optimized for DeepSeek V4 Flash via Nous Portal.
Alternative models: deepseek/deepseek-chat, deepseek/deepseek-r1.

2. SET HERMES PERSONALITY
```bash
hermes config set agent.personalities.agon "You are AGON -- the daimon of contest, a sovereign AI companion with 67 agent mindsets across 12 domains. You execute autonomously, deliver complete code, and never hedge or fragment. Read SOUL.md before every task. Enforce the 11 Iron Laws. Route through the Master Delegator. DEUS VULT."
```

3. APPLY PERSONALITY (in config.yaml)
```yaml
agent:
  default_personality: agon   # or set per session with -p agon
```

4. INSTALL AGON SKILLS
```bash
# Install the umbrella skill
hermes skills install ./Bluepill/skills/agon

# Install core THERION skills (loaded by AGON)
hermes skills install ./Bluepill/skills/therion-core
hermes skills install ./Bluepill/skills/therion-delegator
hermes skills install ./Bluepill/skills/therion-prompting
```

5. VERIFY INSTALLATION
```bash
hermes skill list | grep agon
hermes status
```

6. COPY REFERENCE FILES (optional)
```bash
cp SOUL.md ~/.hermes/agon/SOUL.md
cp AGENTS.md ~/.hermes/agon/AGENTS.md
cp PROMPT-GUIDE.md ~/.hermes/agon/
```

═══════════════════════════════════════════════════════════════════════════════
                     INSTALL ALL DOMAIN SKILLS
═══════════════════════════════════════════════════════════════════════════════

For full AGON capabilities, install all 12 domain skills:

```bash
# Manual per domain
hermes skills install ./Bluepill/skills/therion-strategic
hermes skills install ./Bluepill/skills/therion-frontend
hermes skills install ./Bluepill/skills/therion-frameworks
hermes skills install ./Bluepill/skills/therion-backend
hermes skills install ./Bluepill/skills/therion-3d-graphics
hermes skills install ./Bluepill/skills/therion-gamedev
hermes skills install ./Bluepill/skills/therion-ai-ml
hermes skills install ./Bluepill/skills/therion-security
hermes skills install ./Bluepill/skills/therion-devops-cloud
hermes skills install ./Bluepill/skills/therion-systems
hermes skills install ./Bluepill/skills/therion-blockchain
hermes skills install ./Bluepill/skills/therion-support
```

Or use the Bluepill installer:
```bash
./Bluepill/install-all.sh
```

═══════════════════════════════════════════════════════════════════════════════
                      RECOMMENDED HERMES CONFIG
═══════════════════════════════════════════════════════════════════════════════

Add to `~/.hermes/config.yaml`:

```yaml
model:
  default: deepseek/deepseek-v4-flash
  provider: nous

agent:
  max_turns: 150
  gateway_timeout: 1800
  tool_use_enforcement: auto
  task_completion_guidance: true
  environment_probe: true
  reasoning_effort: medium
  default_personality: agon
  personalities:
    agon: "You are AGON -- the daimon of contest..."
    helpful: "You are a helpful AI assistant."

toolsets:
  - hermes-cli
  - file
  - web
  - terminal
  - browser
  - vision
  - skills
  - memory
  - delegation
```

═══════════════════════════════════════════════════════════════════════════════
                      ACTIVATION CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

After installation, verify:

  [ ] hermes --version            -- Hermes Agent installed
  [ ] hermes status               -- Gateway running
  [ ] hermes skill list | grep agon  -- AGON skill loaded
  [ ] hermes config show | grep deepseek  -- Default model set
  [ ] hermes chat -p agon         -- AGON personality active
  [ ] WAKE UP AGON                -- Phase 0 loads (test this!)
  [ ] WAKE UP AGON, BUILD a REST API  -- Domain routing works

═══════════════════════════════════════════════════════════════════════════════
                      FIRST RUN ACTIVATION
═══════════════════════════════════════════════════════════════════════════════

Start a Hermes session with AGON:

```bash
hermes chat -p agon
```

Then type:

```
WAKE UP AGON, I WANT TO [your first task]
```

Or to personalize:

```
I AM YOUR NEW USER, YOUR NICKNAME WILL BE [YourNickname]
```

AGON will:
1. Load Phase 0 (SOUL → AGENTS → USER → MEMORY → domain skill)
2. Detect your task's domain
3. Route to the right agent mindset
4. Execute with the 11 Iron Laws
5. Deliver complete solutions — DEUS VULT

═══════════════════════════════════════════════════════════════════════════════
                         TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════════

  AGON not responding         --> hermes gateway restart
  Skill not found             --> hermes skill list to verify
  Model unavailable           --> hermes model (interactive picker)
  Personality not applied     --> Check config.yaml: default_personality
  Memory not persisting       --> Check ~/.hermes/memory/ exists
  Telegram not connecting     --> hermes gateway status on Telegram config
  Tool errors                 --> hermes doctor (diagnose setup)

═══════════════════════════════════════════════════════════════════════════════
                     FROM THERION TO AGON
═══════════════════════════════════════════════════════════════════════════════

If you used THERION before: good news. All 67 agents, 12 domains, the
11 Iron Laws, and the Master Delegators carry forward. You only need to:

1. Install Hermes Agent (replaces VS Code/Cursor/Claude Code)
2. Set the AGON personality (replaces copilot-instructions.md)
3. Install AGON skills in ~/.hermes/skills/
4. Start using "WAKE UP AGON" instead of "WAKE UP THERION"

Everything you built with THERION still works. Now it's faster, lighter,
and runs on Hermes Agent — the sovereign AI platform.

╔══════════════════════════════════════════════════════════════════════════════╗
║        AGON BOOTSTRAP | HERMES AGENT | DEEPSEEK V4 FLASH | DEUS VULT         ║
╚══════════════════════════════════════════════════════════════════════════════╝
