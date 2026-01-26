# Claude Code Architecture Validation Setup

Multi-agent system for architectural validation, feature planning, and CI/CD management across microservices.

## Structure

```
claude-code-setup/
├── agents/           # Subagent definitions (.md files)
├── skills/           # Reusable skills with scripts & references
│   ├── validation/           # Architectural validation
│   ├── feature-planning/     # Feature analysis & planning
│   ├── commit-manager/       # Intelligent commits
│   ├── package-release/      # Version propagation
│   └── docs-sync/            # Confluence sync
├── references/       # Shared architectural documentation
└── templates/        # Output templates
```

## Skills (Entry Points)

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `validation` | `/validate` | Run architectural validation |
| `feature-planning` | `/plan-feature "name" "desc"` | Plan feature implementation |
| `commit-manager` | `/commit` | Generate intelligent commits |
| `package-release` | `/update-packages` | Propagate package versions |
| `docs-sync` | `/sync-docs` | Sync with Confluence |

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SKILLS + AGENTS HIERARCHY                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SKILLS (Entry Points with Scripts)                                          │
│  ──────────────────────────────────                                          │
│                                                                              │
│  validation/                        feature-planning/                        │
│    ├── SKILL.md                       ├── SKILL.md                           │
│    ├── scripts/                       ├── scripts/                           │
│    │   ├── discover-services.py       │   ├── feature-analysis.py            │
│    │   ├── validate-structure.py      │   └── plan-validation.py             │
│    │   ├── check-dependencies.py      └── references/                        │
│    │   └── aggregate-results.py                                              │
│    └── references/                                                           │
│                                                                              │
│  commit-manager/                    package-release/                         │
│    ├── SKILL.md                       ├── SKILL.md                           │
│    ├── scripts/                       ├── scripts/                           │
│    │   └── git-operations.py          │   ├── npm-package-ops.py             │
│    └── references/                    │   └── nuget-package-ops.py           │
│        └── commit-conventions.md      └── references/                        │
│                                           └── package-config.md              │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  AGENTS (Spawned by Skills)                                                  │
│  ──────────────────────────                                                  │
│                                                                              │
│  Validation Agents:                   Planning Agents:                       │
│    • master-architect                   • feature-planner                    │
│    • service-validator                  • plan-validator                     │
│    • frontend-pattern-validator                                              │
│    • backend-pattern-validator        CI/CD Agents:                          │
│    • infrastructure-validator           • commit-manager                     │
│    • core-validator                     • release-orchestrator               │
│    • validation-orchestrator            • npm-package-manager                │
│                                         • nuget-package-manager              │
│  Local LLM Workers:                                                          │
│    • local-llm-worker (Ollama)        Docs:                                  │
│    • lmstudio-llm-worker              • docs-sync-agent                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Skills vs Agents: When to Use Each

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SKILLS                               AGENTS                                 │
│  ──────                               ──────                                 │
│                                                                              │
│  • Entry points for workflows         • Specialized reasoning units          │
│  • Contain scripts + references       • Spawned by skills or other agents    │
│  • User-facing triggers               • Isolated context                     │
│  • Self-contained packages            • Return structured JSON               │
│                                                                              │
│  Example: validation/SKILL.md         Example: master-architect.md           │
│  - Has discover-services.py           - Pure reasoning about architecture    │
│  - Has validate-structure.py          - Spawned by validation skill          │
│  - Orchestrates the workflow          - Returns validation findings          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Feature Planning Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    /plan-feature "user-auth" "description"                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. DISCOVERY (script)                                                       │
│     └──► feature-analysis.py discover                                        │
│                                                                              │
│  2. ARCHITECTURAL CONSULTATION (parallel agents)                             │
│     ├──► master-architect                                                    │
│     ├──► frontend-pattern-validator                                          │
│     ├──► backend-pattern-validator                                           │
│     ├──► core-validator                                                      │
│     └──► infrastructure-validator                                            │
│                                                                              │
│  3. SYNTHESIS (script)                                                       │
│     └──► feature-analysis.py synthesize                                      │
│                                                                              │
│  4. VALIDATION (agent)                                                       │
│     └──► plan-validator                                                      │
│                                                                              │
│  5. OUTPUT (script)                                                          │
│     └──► feature-analysis.py write-plan                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Context Management Strategy

```
User Request
    ↓
Main Context (CLAUDE.md) - minimal, decision-focused
    ↓
Skill (SKILL.md + scripts) - orchestrates workflow
    ↓
Spawned Agents (subagents) - isolated context each
    ├── Agent 1: specific validation
    ├── Agent 2: specific validation
    └── Agent N: specific validation
    ↓
Results aggregated → Clean summary returned
```

### Key Principles

1. **Skills are entry points**: User-facing, contain all resources
2. **Agents are reasoning units**: Spawned for specific tasks
3. **Scripts are deterministic**: Python for repeatable operations
4. **Context isolation**: Each subagent has fresh context
5. **Structured reports**: Consistent JSON output format

## Local LLM Integration

Reduce API costs by offloading suitable tasks to local LLMs:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LOCAL LLM WORKER PATTERN                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Skill (e.g., commit-manager)                                                │
│       │                                                                      │
│       ├──► Spawn: local-llm-worker                                           │
│       │         │                                                            │
│       │         ├──► Ping check first                                        │
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
- `skills/package-release/references/package-config.md` - NPM/NuGet settings
- `skills/docs-sync/references/confluence-structure.md` - Confluence spaces
