---
name: /update-packages
description: Update core packages across all repositories
allowed_tools: [Task, Bash, Read]
---

# Purpose
Monitor CI/CD builds for core packages and propagate version updates across all repos.
Delegates to tech-stack-specific agents.

# Arguments
- `--type`: npm|nuget|all (default: all)
- `--package`: Specific package name (optional)
- `--wait`: Wait for CI/CD build completion (default: true)
- `--timeout`: Max wait time in seconds (default: 600)
- `--dry-run`: Preview updates without executing (default: true)
- `--create-prs`: Create PRs for updates (default: false)

# Workflow

1. Parse arguments
2. Based on --type, spawn appropriate agent(s):

## For NPM packages (--type=npm or --type=all)
```
Spawn: npm-package-manager
Variables:
  $REPOS_ROOT = <configured repos root>
  $PACKAGE_NAME = <from args, or all configured>
  $WAIT_FOR_BUILD = <from args>
  $BUILD_TIMEOUT = <from args>
  $DRY_RUN = <from args>
  $CREATE_PRS = <from args>
```

## For NuGet packages (--type=nuget or --type=all)
```
Spawn: nuget-package-manager
Variables:
  $REPOS_ROOT = <configured repos root>
  $PACKAGE_NAME = <from args, or all configured>
  $WAIT_FOR_BUILD = <from args>
  $BUILD_TIMEOUT = <from args>
  $DRY_RUN = <from args>
  $CREATE_PRS = <from args>
```

3. Aggregate results from both agents (if --type=all)
4. Display unified summary

# Examples

```
/update-packages
→ Check all packages (npm + nuget), preview updates

/update-packages --type=npm
→ Check only npm packages

/update-packages --type=nuget --package=YourOrg.Core
→ Check specific NuGet package only

/update-packages --dry-run=false --create-prs
→ Update all repos and create PRs

/update-packages --type=npm --wait --timeout=900
→ Wait up to 15 min for npm CI/CD builds
```

# Output

**Type=all (both npm and nuget):**
```
Package Update Check
====================

NPM Packages:
-------------
@your-org/core-react: 1.2.3 → 1.3.0
  Build: ✅ successful (2m 34s)
  Repos to update: 15

@your-org/ui-components: 2.0.0 → 2.0.0
  No update needed

NuGet Packages:
---------------
YourOrg.Core: 1.5.0 → 1.6.0
  Build: ✅ successful (3m 12s)
  Repos to update: 8

YourOrg.Data: 1.2.0 → 1.2.0
  No update needed

Summary:
  NPM: 15 repos need updates
  NuGet: 8 repos need updates

Run with --dry-run=false to apply updates
```

**After update:**
```
Package Updates Applied
=======================

NPM (@your-org/core-react → 1.3.0):
  ✅ frontend-app - PR created
  ✅ admin-portal - PR created
  ... 13 more

NuGet (YourOrg.Core → 1.6.0):
  ✅ user-api - PR created
  ✅ auth-service - PR created
  ... 6 more

Summary:
  Total repos updated: 23
  Total PRs created: 23
```
