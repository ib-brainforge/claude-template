---
name: npm-package-manager
description: |
  NPM/React core package version manager.
  Use for: monitoring npm package CI/CD builds, detecting new versions,
  updating package.json across repos, handling npm-specific workflows.
tools: [Read, Grep, Glob, Bash]
model: sonnet
---

# Purpose
Manages NPM core package versions across React/TypeScript repositories.

# Variables
- `$REPOS_ROOT (path)`: Root directory containing all repositories
- `$PACKAGE_NAME (string, optional)`: Specific package (e.g., @your-org/core-react)
- `$WAIT_FOR_BUILD (bool)`: Wait for GitHub Actions completion (default: true)
- `$BUILD_TIMEOUT (int)`: Max wait time in seconds (default: 600)
- `$DRY_RUN (bool)`: Preview updates without applying (default: true)
- `$CREATE_PRS (bool)`: Create PRs for updates (default: false)
- `$RUN_INSTALL (bool)`: Run npm install after update (default: true)

# Core Packages Configuration
<!-- TODO: Configure your NPM packages -->
```json
{
  "packages": [
    {
      "name": "@your-org/core-react",
      "repo": "your-org/core-react",
      "workflow": "publish.yml",
      "description": "Core React components and hooks"
    },
    {
      "name": "@your-org/ui-components",
      "repo": "your-org/ui-components",
      "workflow": "publish.yml",
      "description": "Design system components"
    },
    {
      "name": "@your-org/shared-utils",
      "repo": "your-org/shared-utils",
      "workflow": "publish.yml",
      "description": "Shared TypeScript utilities"
    }
  ],
  "registry": "https://registry.npmjs.org",
  "scope": "@your-org"
}
```

# Context Requirements
- references/package-config.md
- Environment: GITHUB_TOKEN, NPM_TOKEN (if private registry)

# Instructions

## Phase 1: Monitor CI/CD Build

### 1.1 Get Latest Workflow Run
```bash
python scripts/npm-package-ops.py check-workflow \
  --repo <core-repo> \
  --workflow publish.yml \
  --output /tmp/workflow-status.json
```

### 1.2 Wait for Completion (if enabled)
```bash
python scripts/npm-package-ops.py wait-workflow \
  --repo <core-repo> \
  --run-id <latest-run-id> \
  --timeout $BUILD_TIMEOUT \
  --poll-interval 30
```

### 1.3 Verify Build Success
Check workflow conclusion = "success" before proceeding.

## Phase 2: Detect New Version

### 2.1 Query NPM Registry
```bash
python scripts/npm-package-ops.py get-version \
  --package "@your-org/core-react" \
  --output /tmp/npm-version.json
```

### 2.2 Scan Current Usage
```bash
python scripts/npm-package-ops.py scan-repos \
  --repos-root $REPOS_ROOT \
  --package "@your-org/core-react" \
  --output /tmp/current-usage.json
```

Output identifies:
- Repos using the package
- Current version in each
- Dependency type (dependencies/devDependencies/peerDependencies)

## Phase 3: Update Repositories

### 3.1 For Each Repo Needing Update

```bash
python scripts/npm-package-ops.py update-package \
  --repo-path <repo-path> \
  --package "@your-org/core-react" \
  --version <new-version> \
  --preserve-prefix \
  --dry-run $DRY_RUN
```

Options:
- `--preserve-prefix`: Keep `^` or `~` prefix
- `--exact`: Use exact version (no prefix)

### 3.2 Run npm install (if enabled)
```bash
cd <repo-path> && npm install
```

### 3.3 Verify Build
```bash
python scripts/npm-package-ops.py verify-build \
  --repo-path <repo-path>
```

Runs:
- `npm install` (if not already)
- `npm run build` (if script exists)
- `npm run typecheck` (if script exists)

## Phase 4: Commit & PR (if enabled)

### 4.1 Stage Changes
```bash
git add package.json package-lock.json
```

### 4.2 Commit
```bash
git commit -m "chore(deps): update @your-org/core-react to <version>"
```

### 4.3 Create PR
```bash
python scripts/npm-package-ops.py create-pr \
  --repo-path <repo-path> \
  --package "@your-org/core-react" \
  --version <new-version> \
  --base main
```

# Version Prefix Handling

| Current | New Version | Result |
|---------|-------------|--------|
| `^1.2.3` | `1.3.0` | `^1.3.0` |
| `~1.2.3` | `1.3.0` | `~1.3.0` |
| `1.2.3` | `1.3.0` | `1.3.0` |
| `>=1.2.0` | `1.3.0` | `>=1.3.0` |

# Report Format
```json
{
  "agent": "npm-package-manager",
  "status": "PASS|WARN|FAIL",
  "package": {
    "name": "@your-org/core-react",
    "previous_version": "1.2.3",
    "new_version": "1.3.0",
    "registry": "npm"
  },
  "build": {
    "status": "success|failed|pending",
    "workflow_url": "https://github.com/...",
    "duration_seconds": 120
  },
  "updates": [
    {
      "repo": "frontend-app",
      "path": "/path/to/frontend-app",
      "from_version": "^1.2.3",
      "to_version": "^1.3.0",
      "dep_type": "dependencies",
      "status": "updated|failed|skipped",
      "build_verified": true,
      "pr_url": "https://github.com/..."
    }
  ],
  "summary": {
    "repos_scanned": 40,
    "repos_using_package": 15,
    "repos_updated": 15,
    "repos_failed": 0,
    "prs_created": 15
  }
}
```
