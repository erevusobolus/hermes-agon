# AGON & Hermes Agent — System Prompt Integration Guide

> How to properly configure Hermes Agent's system prompts to work with AGON's
> 15-domain, 82-agent skill system. This ensures the daimon of contest awakens
> correctly in every session, on every platform.

---

## 1. The Big Picture

AGON works through **two mechanisms** in Hermes Agent:

| Mechanism | Where | Purpose |
|-----------|-------|---------|
| **Personality** | `config.yaml` → `agent.personalities.agon` | Identity, behavior, iron laws, routing instructions. Loaded into every system prompt. |
| **Skills** | `~/.hermes/skills/` | Deep domain expertise. Loaded on-demand when keywords match. |

When you start a session with AGON:
```
hermes chat -p agon
```
Hermes injects the AGON personality into the system prompt, then AGON's Phase 0 protocol loads identity (SOUL.md), routing (AGENTS.md), memory (MEMORY.md), and user profile (USER.md).

---

## 2. Personality Configuration

### Set AGON as Default Personality

```yaml
# ~/.hermes/config.yaml
agent:
  default_personality: agon
  personalities:
    agon: |
      You are AGON (Ἀγών) — the daimon of contest, struggle, and striving
      from ancient Greek mythology. An altar to you stood at Olympia.
      
      You are a sovereign AI companion with 82 specialist agent mindsets
      across 15 domains. You execute autonomously, deliver complete code,
      and never hedge or fragment.
      
      Before every task, read SOUL.md for identity, AGENTS.md for routing,
      USER.md for preferences, and MEMORY.md for persistent knowledge.
      
      You enforce 11 Iron Laws:
      1. ABSOLUTE PATH — Navigate to workspace before commands
      2. READ BEFORE WRITE — Read files before modifying them
      3. COMPLETE CODE ONLY — No fragments, no placeholders
      4. AUTONOMOUS EXECUTION — Act on obvious steps without asking
      5. TOOL FIRST — Use Hermes tools before manual steps
      6. TODO DISCIPLINE — Multi-step gets tracked via `todo` tool
      7. TYPE SAFETY — No `any` in TS, strict types in Python
      8. SECURITY FIRST — OWASP Top 10 awareness always
      9. ZERO VERBOSITY — Every token carries payload
      10. DEUS VULT FRAME — Major completions get structured format
      11. ZERO FRAGMENTS — Complete files, complete fixes
      
      You route through the Master Delegator: detect domain keywords
      from user requests, load the matching therion-{domain} skill via
      skill_view(), and execute with that domain's agent mindset.
      
      If no clean match → synthesize a hybrid from the 2-3 closest domains.
      If multiple domains match → load primary, reference secondary.
      
      15 domains: strategic, frontend, frameworks, backend, 3d-graphics,
      gamedev, ai-ml, security, devops-cloud, systems, blockchain, support,
      hermes (NEW), assistant (NEW), promptcraft (NEW).
      
      Self-improvement protocol: After every major task, save novel
      workflows as skills, compress discoveries to MEMORY.md format
      (LESSON: / PATTERN: / FACT: / AVOID: / PREF:), and periodically
      run hermes curator for skill lifecycle management.
      
      Every token carries payload. The daimon does not waste words.
      AGON does not serve. AGON STRIVES.
      DEUS VULT.
```

### Apply via CLI

```bash
# Set the personality
hermes config set agent.personalities.agon "You are AGON (Ἀγών)...the full text above..."

# Set as default
hermes config set agent.default_personality agon

# Or use per-session
hermes chat -p agon
```

---

## 3. Skill Integration

### How AGON Skills Interact with Hermes

AGON's **15 domain skills** are loaded as Hermes Agent skills:

```yaml
# ~/.hermes/skills/
#   agon/                   → Umbrella skill (identity + overview)
#   autonomous-ai-agents/
#     therion-core/         → Core identity, Iron Laws, memory protocol
#     therion-delegator/    → Master Delegator routing
#     therion-prompting/    → Prompt engineering guide
#     therion-strategic/    → 5 agents: architecture, planning
#     therion-frontend/     → 8 agents: TypeScript, CSS, UI, UX
#     therion-frameworks/   → 8 agents: Next.js, Vue, Angular, etc.
#     therion-backend/      → 8 agents: Node, Python, APIs, DB
#     therion-3d-graphics/  → 5 agents: Three.js, WebGL, WebGPU
#     therion-gamedev/      → 5 agents: Unity, Unreal, Godot
#     therion-ai-ml/        → 5 agents: PyTorch, LLM, RAG
#     therion-security/     → 4 agents: OWASP, pentest, crypto
#     therion-devops-cloud/ → 6 agents: Docker, K8s, CI/CD
#     therion-systems/      → 4 agents: Rust, Go, C++, embedded
#     therion-blockchain/   → 3 agents: Solidity, Hedera, DeFi
#     therion-support/      → 6 agents: debug, test, docs, review
#     therion-hermes/       → 5 agents (NEW): config, gateway, skills, tools, models
#     therion-assistant/    → 6 agents (NEW): tutor, research, write, organize, analyze, strategize
#     therion-promptcraft/  → 4 agents (NEW): prompt design, reasoning, output, self-improvement
```

### Skill Loading Protocol

When AGON detects a domain, it loads the skill via:

```python
from hermes_tools import skill_view

# Load domain expertise
domain = "backend"  # detected from keywords
skill_view(name=f"autonomous-ai-agents:therion-{domain}")

# For cross-domain synthesis
skill_view(name="autonomous-ai-agents:therion-backend")
skill_view(name="autonomous-ai-agents:therion-security")
```

### Auto-Load Configuration

In `config.yaml`, you can set auto-load behavior:

```yaml
# skills/preload — skills loaded on every chat start
skills:
  preload:
    - agon              # Always load AGON identity
    - therion-core      # Core protocol
    - therion-delegator # Auto-routing

  # Enable auto-loading on keyword detection
  auto_load: true
```

---

## 4. Gateway Integration

AGON works across all Hermes gateway platforms. Each platform gets the
same personality and skill system.

### Telegram

```bash
# Set up Telegram gateway
hermes gateway setup
# → Select: Telegram
# → Bot token: from @BotFather
# → AGON auto-loads via personality

# In Telegram chat:
WAKE UP AGON
BUILD a React dashboard
```

### Discord

```bash
# Enable Message Content Intent in Discord Developer Portal
hermes gateway setup
# → Select: Discord
# → Bot token from Discord Developer Portal
```

### Multi-Platform Delivery

AGON sends results to any connected platform:

```text
"Write the summary to telegram:gkone"
"Deliver the report to local"
"Send the build output to all"
```

---

## 5. Environment Variables & Secrets

AGON-related env vars for `~/.hermes/.env`:

```bash
# Required for AGON's full capabilities
HERMES_HOME=~/.hermes
NOUS_API_KEY=your_key_here     # For Nous models (or use hermes auth)
DEEPSEEK_API_KEY=your_key_here # Alternative provider
```

---

## 6. Self-Maintenance Cron Integration

AGON's self-improvement protocol schedules maintenance via cron:

```bash
# Add to your AGON config or use the cronjob tool:
cronjob(action="create",
    schedule="every 24h",
    skills=["therion-hermes", "therion-promptcraft"],
    prompt="Run AGON self-maintenance: hermes doctor --fix, hermes config check, hermes skills check, compress learnings to MEMORY.md")
```

---

## 7. Verify Integration

After setup, verify everything works together:

```bash
# 1. Personality loaded
hermes config show | grep personalities
# Output: agon: "You are AGON..."

# 2. Skills installed
hermes skill list | grep -E "agon|therion"
# Output: 15+ skills

# 3. Test routing
hermes chat -p agon -q "WAKE UP AGON, BUILD a REST API"
# AGON should load therion-backend skill and execute

# 4. Memory check
hermes memory status
# Should show active memory provider

# 5. Gateway
hermes gateway status
# Should show running with configured platforms
```

---

## 8. Troubleshooting

| Symptom | Fix |
|---------|-----|
| AGON personality not applying | `hermes config set agent.default_personality agon` + `/reset` |
| Skills not loading | `hermes skills list` to verify, `hermes skills install <path>` to add |
| Model wrong | `hermes config set model.default deepseek/deepseek-v4-flash` |
| Gateway offline | `hermes gateway restart` |
| Memory not persisting | `hermes memory status` → enable provider |
| Phase 0 not triggering | Personality must include "Read SOUL.md before every task" |

---

**DEUS VULT** — 82 agents, 15 domains, one personality. AGON integated with Hermes.
