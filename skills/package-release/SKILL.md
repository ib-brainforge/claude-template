---
name: package-release
description: |
  Package version management and release orchestration.
  Monitors CI/CD, propagates versions across repositories.
  Supports NPM and NuGet ecosystems.
triggers:
  - /update-packages
  - /release
  - update packages
  - propagate versions
  - check package versions
---

# Purpose

Monitor core package CI/CD pipelines, detect new versions, and propagate updates
across all dependent repositories. Handles both NPM (React) and NuGet (C#) ecosystems.

# Usage

```
/update-packages                     # Check and update all packages
/update-packages --npm               # NPM packages only
/update-packages --nuget             # NuGet packages only
/update-packages --check-only        # Check for updates, don't apply
/update-packages --package @core/ui  # Specific package
/release                             # Full release workflow
```

# Variables

- `$REPOS_ROOT (string)`: Path to repositories (default: .)
- `$ECOSYSTEM (string)`: npm|nuget|all (default: all)
- `$CHECK_ONLY (bool)`: Don't apply updates (default: false)
- `$PACKAGE (string, optional)`: Specific package to update
- `$AUTO_COMMIT (bool)`: Commit changes automatically (default: false)
- `$AUTO_PR (bool)`: Create PRs for updates (default: false)

# Context Requirements

- references/package-config.md
- Access to NPM registry / NuGet feed
- GitHub Actions API access (for CI monitoring)

# Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     PACKAGE RELEASE WORKFLOW                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. CHECK CI/CD STATUS                                                       │
│     ├──► NPM: Check GitHub Actions for @core/* packages                      │
│     └──► NuGet: Check GitHub Actions for Core.* packages                     │
│                                                                              │
│  2. DETECT NEW VERSIONS                                                      │
│     ├──► scripts/npm-package-ops.py check-registry                           │
│     └──► scripts/nuget-package-ops.py check-registry                         │
│                                                                              │
│  3. FIND DEPENDENTS                                                          │
│     ├──► Scan package.json files for NPM                                     │
│     └──► Scan .csproj files for NuGet                                        │
│                                                                              │
│  4. UPDATE DEPENDENTS (Parallel by ecosystem)                                │
│     ├──► Spawn: npm-package-manager                                          │
│     └──► Spawn: nuget-package-manager                                        │
│                                                                              │
│  5. COMMIT & PR (if enabled)                                                 │
│     └──► Use commit-manager skill                                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

# Instructions

## 1. Check CI/CD Status

```bash
# Check NPM package builds
python skills/package-release/scripts/npm-package-ops.py check-ci \
  --packages "@core/ui,@core/utils,@core/api-client" \
  --output /tmp/npm-ci-status.json

# Check NuGet package builds
python skills/package-release/scripts/nuget-package-ops.py check-ci \
  --packages "Core.Common,Core.Data,Core.Security" \
  --output /tmp/nuget-ci-status.json
```

## 2. Detect New Versions

```bash
# NPM registry check
python skills/package-release/scripts/npm-package-ops.py check-registry \
  --packages "@core/ui,@core/utils" \
  --output /tmp/npm-versions.json

# NuGet registry check
python skills/package-release/scripts/nuget-package-ops.py check-registry \
  --packages "Core.Common,Core.Data" \
  --output /tmp/nuget-versions.json
```

## 3. Find Dependent Repositories

```bash
# Find NPM dependents
python skills/package-release/scripts/npm-package-ops.py find-dependents \
  --repos-root $REPOS_ROOT \
  --packages "@core/ui,@core/utils" \
  --output /tmp/npm-dependents.json

# Find NuGet dependents
python skills/package-release/scripts/nuget-package-ops.py find-dependents \
  --repos-root $REPOS_ROOT \
  --packages "Core.Common,Core.Data" \
  --output /tmp/nuget-dependents.json
```

## 4. Update Dependencies

### NPM Updates (spawn subagent)
```
Task: spawn npm-package-manager
Prompt: |
  Update NPM packages in repositories:
  Updates needed: [from npm-versions.json]
  Dependents: [from npm-dependents.json]

  Preserve version prefixes (^, ~).
  Return list of updated files.
```

### NuGet Updates (spawn subagent)
```
Task: spawn nuget-package-manager
Prompt: |
  Update NuGet packages in repositories:
  Updates needed: [from nuget-versions.json]
  Dependents: [from nuget-dependents.json]

  Update both .csproj and Directory.Packages.props.
  Return list of updated files.
```

## 5. Commit Changes (if enabled)

If $AUTO_COMMIT:
```
Use skill: commit-manager
  --scope all
  --feature-tag "deps-update"
```

## 6. Create PRs (if enabled)

If $AUTO_PR:
```bash
python skills/package-release/scripts/npm-package-ops.py create-pr \
  --repos [updated repos] \
  --title "chore(deps): update core packages" \
  --output /tmp/pr-results.json
```

# Report Format

```json
{
  "skill": "package-release",
  "status": "PASS|WARN|FAIL",
  "ci_status": {
    "npm": {
      "@core/ui": { "status": "success", "version": "2.3.1" },
      "@core/utils": { "status": "success", "version": "1.5.0" }
    },
    "nuget": {
      "Core.Common": { "status": "success", "version": "3.1.0" },
      "Core.Data": { "status": "running", "version": null }
    }
  },
  "updates": {
    "npm": {
      "available": 2,
      "applied": 2,
      "repos_updated": ["user-frontend", "admin-frontend"]
    },
    "nuget": {
      "available": 1,
      "applied": 1,
      "repos_updated": ["user-service", "order-service"]
    }
  },
  "commits": [
    { "repo": "user-frontend", "sha": "abc123" }
  ],
  "prs": [
    { "repo": "user-frontend", "pr_number": 142, "url": "..." }
  ],
  "warnings": [
    "Core.Data build still running - skipped"
  ]
}
```

# Package Configuration

Configure in `references/package-config.md`:

```yaml
npm:
  scope: "@core"
  packages:
    - "@core/ui"
    - "@core/utils"
    - "@core/api-client"
  registry: "https://npm.pkg.github.com"

nuget:
  prefix: "Core."
  packages:
    - "Core.Common"
    - "Core.Data"
    - "Core.Security"
  feed: "https://nuget.pkg.github.com/OWNER/index.json"

github:
  owner: "your-org"
  ci_workflow: "build-and-publish.yml"
```

# Scripts Reference

| Script | Command | Purpose |
|--------|---------|---------|
| `npm-package-ops.py` | `check-ci` | Monitor GitHub Actions |
| `npm-package-ops.py` | `check-registry` | Get latest versions |
| `npm-package-ops.py` | `find-dependents` | Find repos using package |
| `npm-package-ops.py` | `update` | Update package.json |
| `nuget-package-ops.py` | `check-ci` | Monitor GitHub Actions |
| `nuget-package-ops.py` | `check-registry` | Get latest versions |
| `nuget-package-ops.py` | `find-dependents` | Find repos using package |
| `nuget-package-ops.py` | `update` | Update .csproj files |

# Version Prefix Preservation (NPM)

The skill preserves your version prefixes:
- `^1.2.3` → `^1.3.0` (caret preserved)
- `~1.2.3` → `~1.3.0` (tilde preserved)
- `1.2.3` → `1.3.0` (exact preserved)

# Central Package Management (NuGet)

Supports `Directory.Packages.props` for centralized version management:
- Updates central file first
- Then updates individual `.csproj` files
- Maintains consistency across solution

# Follow-up Skills

After package updates:
- `validation` - Validate builds pass with new versions
- `commit-manager` - Commit the version updates
