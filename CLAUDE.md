# Claude Code Setup Repository

## What This Is

This repository contains a **multi-agent framework template** for AI-assisted development across microservices architectures. The `copy-to-repo/.claude/` folder gets copied into actual projects.

## Mission

> **Enable autonomous, parallel, knowledge-driven development across 40+ microservices repositories with minimal context overhead.**

The system delegates all substantial work to specialized subagents that:
- Load only the knowledge they need
- Execute autonomously without constant user approval
- Validate against architectural rules
- Report back clean, structured results

## When Helping With This Repository

### Creating New Agents

Use `generator/templates/AGENT_TEMPLATE.md` as the base. Every agent must:

1. **Be focused** - One clear purpose, not a Swiss army knife
2. **Declare dependencies** - What knowledge files it reads
3. **Define clear inputs** - Variables it expects
4. **Specify output format** - JSON or structured report
5. **Include telemetry prefix** - `[agent-name]` for log correlation

Agent types:
- **Orchestrators** - Spawn other agents, coordinate workflows (e.g., `feature-implementor`)
- **Workers** - Do actual work, read files, make changes (e.g., `backend-implementor`)
- **Validators** - Check code against patterns (e.g., `backend-pattern-validator`)

### Creating New Skills

Use `generator/templates/SKILL_TEMPLATE.md`. Skills are reusable capabilities with:
- `SKILL.md` - Instructions and workflow
- `tools/` - Python scripts for deterministic operations
- `cookbook/` - Step-by-step recipes for common tasks

### Creating New Commands

Use `generator/templates/COMMAND_TEMPLATE.md`. Commands are user-facing entry points that typically spawn an orchestrator agent.

### Key Design Rules

1. **Parallel by default** - When work streams are independent, spawn agents simultaneously
2. **Autonomous execution** - Agents only stop for genuine blockers (security, breaking changes)
3. **Single writer for knowledge** - Only `commit-manager` writes to learned knowledge files
4. **GitFlow enforced** - All code goes through feature branches via `git-workflow-manager`
5. **Minimal knowledge loading** - Each agent reads ONLY what it needs

### File Locations

```
claude-code-setup/
├── CLAUDE.md                   ← THIS FILE (for Claude helping build the system)
├── copy-to-repo/
│   └── .claude/
│       ├── CLAUDE.md           ← For agents IN projects (routing + rules)
│       ├── agents/             ← Agent definitions
│       ├── commands/           ← Slash commands
│       ├── skills/             ← Reusable skills
│       └── knowledge/          ← Domain knowledge (customized per project)
├── generator/
│   └── templates/              ← Templates for creating new agents/skills/commands
├── INIT.md                     ← Setup instructions
└── README.md                   ← User-facing documentation
```

### Agent Hierarchy

```
USER REQUEST
     │
     ▼
MAIN CONTEXT (routes, never implements)
     │
     ├──► ORCHESTRATORS (coordinate, spawn workers)
     │    feature-implementor, bug-fix-orchestrator, release-orchestrator
     │
     └──► WORKERS (do actual work)
          backend-implementor, frontend-implementor, validators, etc.
```

## Why This Architecture

| Problem | Solution |
|---------|----------|
| Context bloats on large tasks | Subagents isolate work, return summaries |
| Manual pattern checking | Validators check against knowledge files |
| Sequential execution | Parallel spawning when independent |
| No memory between sessions | Learned patterns persist in YAML |
| Inconsistent conventions | GitFlow + commit-manager enforce standards |

## Common Tasks

### "Add an agent for X"
1. Identify: orchestrator or worker?
2. Copy appropriate template
3. Define inputs, knowledge dependencies, output format
4. Add to relevant orchestrator's workflow if needed

### "Add validation for Y pattern"
1. Add pattern to `knowledge/validation/backend-patterns.md` or `frontend-patterns.md`
2. Validators will automatically check against it

### "Add a new command"
1. Copy command template
2. Define what orchestrator it spawns
3. Specify required arguments

### "Update workflow for Z"
1. Find the orchestrator agent
2. Modify its workflow steps
3. Update any worker agents if their interfaces change
