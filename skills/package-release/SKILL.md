---
name: package-release
description: |
  Package version management and release orchestration.
  Monitors CI/CD, propagates versions across repositories.
  All package names and registries loaded from knowledge files.
triggers:
  - /update-packages
  - /release
  - update packages
  - propagate versions
  - check package versions
---

# Purpose

Monitor core package CI/CD pipelines, detect new versions, and propagate updates
across all dependent repositories. All package-specific configuration is loaded
from knowledge files.

# Usage

```
/update-packages                     # Check and update all packages
/update-packages --ecosystem npm     # Frontend packages only
/update-packages --ecosystem nuget   # Backend packages only
/update-packages --check-only        # Check for updates, don't apply
/update-packages --package [name]    # Specific package
/release                             # Full release workflow
```

# Variables

- `$REPOS_ROOT (string)`: Path to repositories (default: .)
- `$ECOSYSTEM (string)`: frontend|backend|all (default: all)
- `$CHECK_ONLY (bool)`: Don't apply updates (default: false)
- `$PACKAGE (string, optional)`: Specific package to update
- `$AUTO_COMMIT (bool)`: Commit changes automatically (default: false)
- `$AUTO_PR (bool)`: Create PRs for updates (default: false)

# Knowledge References

This skill loads ALL package configuration from:

```
knowledge/packages/package-config.md      → Package names, registries, feeds, workflows
knowledge/packages/core-packages.md       → Core package list
```

**IMPORTANT**: Do not hardcode any package names, registry URLs, or specific
packages in this skill. All such information must come from knowledge files.

# Cookbook

| Recipe | Purpose |
|--------|---------|
| `check-ci-status.md` | Monitor CI/CD pipelines |
| `detect-versions.md` | Find new package versions |
| `update-dependents.md` | Update consuming repos |
| `create-prs.md` | Create update PRs |

# Tools

| Tool | Purpose |
|------|---------|
| `npm-package-ops.py` | Frontend package operations |
| `nuget-package-ops.py` | Backend package operations |

# Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     PACKAGE RELEASE WORKFLOW                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  0. LOAD KNOWLEDGE                                                           │
│     └──► Read package-config.md for package names and registries             │
│                                                                              │
│  1. CHECK CI/CD STATUS                                                       │
│     ├──► Check frontend package builds (from knowledge)                      │
│     └──► Check backend package builds (from knowledge)                       │
│                                                                              │
│  2. DETECT NEW VERSIONS                                                      │
│     ├──► Query frontend registry (from knowledge)                            │
│     └──► Query backend registry (from knowledge)                             │
│                                                                              │
│  3. FIND DEPENDENTS                                                          │
│     ├──► Scan frontend dependency files                                      │
│     └──► Scan backend dependency files                                       │
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

## 0. Load Knowledge First
Read `knowledge/packages/package-config.md` to get:
- Frontend package names and registry
- Backend package names and feed
- CI workflow names
- Organization/scope info

## 1. Check CI/CD Status

```bash
# Check frontend package builds (packages from knowledge)
python skills/package-release/tools/npm-package-ops.py check-ci \
  --packages "[from knowledge/packages/package-config.md]" \
  --output /tmp/frontend-ci-status.json

# Check backend package builds (packages from knowledge)
python skills/package-release/tools/nuget-package-ops.py check-ci \
  --packages "[from knowledge/packages/package-config.md]" \
  --output /tmp/backend-ci-status.json
```

## 2. Detect New Versions

```bash
# Frontend registry check (packages from knowledge)
python skills/package-release/tools/npm-package-ops.py check-registry \
  --packages "[from knowledge]" \
  --output /tmp/frontend-versions.json

# Backend registry check (packages from knowledge)
python skills/package-release/tools/nuget-package-ops.py check-registry \
  --packages "[from knowledge]" \
  --output /tmp/backend-versions.json
```

## 3. Find Dependent Repositories

```bash
# Find frontend dependents (packages from knowledge)
python skills/package-release/tools/npm-package-ops.py find-dependents \
  --repos-root $REPOS_ROOT \
  --packages "[from knowledge]" \
  --output /tmp/frontend-dependents.json

# Find backend dependents (packages from knowledge)
python skills/package-release/tools/nuget-package-ops.py find-dependents \
  --repos-root $REPOS_ROOT \
  --packages "[from knowledge]" \
  --output /tmp/backend-dependents.json
```

## 4. Update Dependencies

### Frontend Updates (spawn subagent)
```
Task: spawn npm-package-manager
Prompt: |
  Update frontend packages in repositories:
  Updates needed: [from frontend-versions.json]
  Dependents: [from frontend-dependents.json]

  Preserve version prefixes.
  Return list of updated files.
```

### Backend Updates (spawn subagent)
```
Task: spawn nuget-package-manager
Prompt: |
  Update backend packages in repositories:
  Updates needed: [from backend-versions.json]
  Dependents: [from backend-dependents.json]

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

If $AUTO_PR: Create PRs for each updated repository.

# Report Format

```json
{
  "skill": "package-release",
  "status": "PASS|WARN|FAIL",
  "ci_status": {
    "frontend": {},
    "backend": {}
  },
  "updates": {
    "frontend": {
      "available": 0,
      "applied": 0,
      "repos_updated": []
    },
    "backend": {
      "available": 0,
      "applied": 0,
      "repos_updated": []
    }
  },
  "commits": [],
  "prs": [],
  "warnings": []
}
```

# Follow-up Skills

After package updates:
- `validation` - Validate builds pass with new versions
- `commit-manager` - Commit the version updates
