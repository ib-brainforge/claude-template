# Architecture Validation & Release System

<!--
This is your main CLAUDE.md file. Keep it MINIMAL (<50 lines of actual instructions).
Heavy documentation goes in knowledge/, skills/, and agents/.
-->

## Skills (Entry Points)

| Skill | Trigger | Description |
|-------|---------|-------------|
| `validation` | `/validate` | Run architecture validation |
| `feature-planning` | `/plan-feature "name" "desc"` | Plan feature implementation |
| `design-patterns` | `/patterns` | Validate/suggest design patterns |
| `commit-manager` | `/commit` | Generate commits across repos |
| `package-release` | `/update-packages` | Update NPM/NuGet packages |
| `docs-sync` | `/sync-docs` | Sync to Confluence |

## Folder Structure

```
claude-code-setup/
├── CLAUDE.md              # This file (entry point)
├── knowledge/             # Domain-specific content (UPDATE FOR YOUR PROJECT)
│   ├── architecture.md    # System structure, ADRs
│   ├── design-patterns.md # Required patterns
│   ├── anti-patterns.md   # What to avoid
│   ├── core-packages.md   # Shared library APIs
│   ├── tech-stack.md      # Framework versions
│   └── ...
├── skills/                # Entry points with workflows
│   └── {skill}/
│       ├── SKILL.md       # Workflow definition
│       ├── cookbook/      # How-to recipes
│       └── tools/         # Python scripts
└── agents/                # Subagent definitions
```

## Agents

All heavy work is delegated to subagents:

- **Validation**: `validation-orchestrator` → `master-architect`, `*-validator`
- **Design Patterns**: `design-pattern-advisor` (validate/suggest/review modes)
- **Planning**: `feature-planner` → validators → `plan-validator`
- **CI/CD**: `commit-manager`, `release-orchestrator` → package managers
- **Local LLM**: `local-llm-worker`, `lmstudio-llm-worker`

## Workflow Pattern

```
User → Skill (SKILL.md + cookbook + tools) → Agents → knowledge/ → JSON Results
```

## Reusing This Setup

1. Copy this folder to your project
2. Update `knowledge/` files with your domain specifics
3. Skills and agents reference `knowledge/` automatically
