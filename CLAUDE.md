# Architecture Validation & Release System

<!--
This is your main CLAUDE.md file. Keep it MINIMAL (<50 lines of actual instructions).
Heavy documentation goes in references/ and is loaded by subagents as needed.
-->

## Quick Reference

| Command | Description |
|---------|-------------|
| `/validate` | Run architecture validation |
| `/commit` | Generate commits for changed repos |
| `/commit --push` | Commit and push all changes |
| `/update-packages --type=npm` | Update NPM packages across repos |
| `/update-packages --type=nuget` | Update NuGet packages across repos |
| `/sync-docs` | Sync documentation to Confluence |

## Agents

All heavy work is delegated to subagents to keep main context clean:

**Validation**
- `validation-orchestrator`: Coordinates full system validation
- `master-architect`: System-wide architecture decisions
- `service-validator` → `frontend-pattern-validator` / `backend-pattern-validator`

**Release & Git**
- `commit-manager`: Intelligent commit generation across 40+ repos
- `release-orchestrator`: Full release workflow coordination

**Package Management (split by tech stack)**
- `npm-package-manager`: NPM/React package CI/CD monitoring & propagation
- `nuget-package-manager`: NuGet/C# package CI/CD monitoring & propagation

**Documentation**
- `docs-sync-agent`: Confluence synchronization

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

<!-- TODO: Update in references/package-config.md -->
- NPM: `@your-org/core-react`, `@your-org/ui-components`
- NuGet: `YourOrg.Core`, `YourOrg.Data`

## Scripts

All scripts return JSON for deterministic processing:
- `git-operations.py`: Multi-repo git, commit analysis
- `npm-package-ops.py`: NPM registry, package.json updates
- `nuget-package-ops.py`: NuGet registry, .csproj updates
