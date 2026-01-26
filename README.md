# Claude Code Architecture Validation Setup

Multi-agent system for architectural validation, feature planning, and CI/CD management across microservices.

## Structure

```
claude-code-setup/
├── agents/           # Subagent definitions (.md files)
├── skills/           # Reusable skills with resources
├── commands/         # Slash commands for quick actions
├── scripts/          # Python utilities for deterministic operations
├── references/       # Shared architectural documentation
└── templates/        # Output templates for reports
```

## Quick Start Commands

| Command | Purpose |
|---------|---------|
| `/validate` | Run architectural validation |
| `/plan-feature "name" "desc"` | Plan new feature implementation |
| `/commit` | Generate intelligent commit messages |
| `/update-packages` | Propagate package versions |
| `/sync-docs` | Sync with Confluence |

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          AGENT HIERARCHY                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  COMMANDS (Entry Points)                                                     │
│  ───────────────────────                                                     │
│  /validate ──────────► validation-orchestrator                               │
│  /plan-feature ──────► feature-planner                                       │
│  /commit ────────────► commit-manager                                        │
│  /update-packages ───► release-orchestrator                                  │
│  /sync-docs ─────────► docs-sync-agent                                       │
│                                                                              │
│  VALIDATION AGENTS                    PLANNING AGENTS                        │
│  ─────────────────                    ───────────────                        │
│  validation-orchestrator              feature-planner                        │
│    ├── master-architect                 ├── (discovery phase)                │
│    ├── service-validator                ├── master-architect                 │
│    ├── frontend-pattern-validator       ├── frontend-pattern-validator       │
│    ├── backend-pattern-validator        ├── backend-pattern-validator        │
│    ├── infrastructure-validator         ├── core-validator                   │
│    └── core-validator                   ├── infrastructure-validator         │
│                                         └── plan-validator                   │
│                                                                              │
│  CI/CD AGENTS                         LOCAL LLM WORKERS                      │
│  ────────────                         ─────────────────                      │
│  commit-manager                       local-llm-worker (Ollama)              │
│  release-orchestrator                 lmstudio-llm-worker (LM Studio)        │
│    ├── npm-package-manager                                                   │
│    └── nuget-package-manager                                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Feature Planning Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    /plan-feature "user-auth" "description"                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. DISCOVERY                                                                │
│     └──► Scan repos, identify affected services                              │
│                                                                              │
│  2. ARCHITECTURAL CONSULTATION (Parallel)                                    │
│     ├──► master-architect ──► System constraints                             │
│     ├──► frontend-validator ──► UI patterns                                  │
│     ├──► backend-validator ──► API patterns                                  │
│     ├──► core-validator ──► Library impacts                                  │
│     └──► infra-validator ──► Deployment needs                                │
│                                                                              │
│  3. SYNTHESIS                                                                │
│     └──► Combine inputs into implementation plan                             │
│                                                                              │
│  4. VALIDATION                                                               │
│     └──► plan-validator ──► Check against all rules                          │
│                                                                              │
│  5. OUTPUT                                                                   │
│     ├──► feature-{name}-plan.md                                              │
│     └──► feature-{name}-tasks.json                                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Context Management Strategy

```
User Request
    ↓
Main Context (CLAUDE.md) - minimal, decision-focused
    ↓
Orchestrator Agent - delegates to specialists
    ├── Subagent 1 (isolated context)
    ├── Subagent 2 (isolated context)
    └── Subagent N (isolated context)
    ↓
Results aggregated → Clean summary returned
```

### Key Principles

1. **Minimal main context**: CLAUDE.md stays <50 lines
2. **Delegation**: Heavy work happens in subagents
3. **Isolation**: Each subagent has fresh context
4. **Determinism**: Python scripts for repeatable operations
5. **Structured reports**: Consistent JSON output format

## Local LLM Integration

Reduce API costs by offloading suitable tasks to local LLMs:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LOCAL LLM WORKER PATTERN                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Parent Agent (e.g., commit-manager)                                         │
│       │                                                                      │
│       ├──► Spawn: local-llm-worker                                           │
│       │         │                                                            │
│       │         ├──► Step 1: Ping check                                      │
│       │         │     └──► If unavailable → return {status: "UNAVAILABLE"}   │
│       │         │                                                            │
│       │         └──► If available → process task → return result             │
│       │                                                                      │
│       └──► Handle response:                                                  │
│             ├──► UNAVAILABLE → Use Claude API instead                        │
│             ├──► FAIL → Use Claude API instead                               │
│             └──► PASS → Use local result                                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

Supported backends: **Ollama** (automation) | **LM Studio** (GUI/testing)

## File Format Standard

All `.md` agent/skill files follow unified format - see `templates/AGENT_TEMPLATE.md`

## TODO: Configuration Required

Before using, populate these files with your specific settings:

- `references/system-architecture.md` - Your system architecture
- `references/rules/*.md` - Validation rules
- `references/package-config.md` - NPM/NuGet package settings
- `skills/docs-sync/references/confluence-structure.md` - Confluence spaces
