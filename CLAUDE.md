# Architecture Validation & Release System

<!--
This is your main CLAUDE.md file. Keep it MINIMAL (<50 lines of actual instructions).
Heavy documentation goes in skills/ and references/ - loaded by subagents as needed.
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

## Agents

All heavy work is delegated to subagents to keep main context clean:

**Validation**: `validation-orchestrator` → `master-architect`, `service-validator`, `frontend-pattern-validator`, `backend-pattern-validator`, `infrastructure-validator`, `core-validator`

**Design Patterns**: `design-pattern-advisor` (validate/suggest/review modes)

**Planning**: `feature-planner` → `design-pattern-advisor` → validators → `plan-validator`

**CI/CD**: `commit-manager`, `release-orchestrator` → `npm-package-manager`, `nuget-package-manager`

**Local LLM**: `local-llm-worker` (Ollama), `lmstudio-llm-worker` (LM Studio)

**Docs**: `docs-sync-agent`

## Repository Structure

<!-- TODO: Document your actual repo structure -->
```
$REPOS_ROOT/
├── services/           # ~40 microservices (frontend/backend)
├── core/
│   ├── react/         # NPM packages (@your-org/*)
│   └── dotnet/        # NuGet packages (YourOrg.*)
├── infrastructure/    # IaC and deployment
└── docs/              # Central documentation
```

## Core Packages

<!-- TODO: Update in skills/package-release/references/package-config.md -->
- NPM: `@your-org/core-react`, `@your-org/ui-components`
- NuGet: `YourOrg.Core`, `YourOrg.Data`

## Workflow Pattern

```
User → Skill (SKILL.md + scripts) → Agents (subagents) → JSON Results
```

All scripts are inside skills/ folders and return JSON for deterministic processing.
