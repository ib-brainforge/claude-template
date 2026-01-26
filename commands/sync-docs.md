---
name: /sync-docs
description: Synchronize documentation with Confluence
allowed_tools: [Task, Bash, Read]
---

# Purpose
Sync architecture documentation between repositories and Confluence.

# Arguments
- `--mode`: preview|apply|pull (default: preview)
- `--types`: Comma-separated doc types (adr,architecture,runbook)
- `--space`: Confluence space key (uses default if not specified)

# Workflow

1. Parse arguments
2. Spawn docs-sync-agent:
   ```
   Task: docs-sync-agent
   Variables:
     $REPOS_ROOT = <configured repos root>
     $CONFLUENCE_SPACE = <from args or default>
     $SYNC_MODE = <from args>
     $DOC_TYPES = <from args if specified>
   ```
3. Display results

# Examples

```
/sync-docs
→ Preview what would be synced (dry run)

/sync-docs --mode=apply
→ Actually sync documentation to Confluence

/sync-docs --mode=pull
→ Pull documentation from Confluence to local repos

/sync-docs --types=adr --mode=apply
→ Sync only ADR documents
```

# Output

**Preview mode:**
```
Documentation Sync Preview
==========================
Space: ARCH

Would create (3):
  - ADR-0024: Use Event Sourcing for Audit
  - ADR-0025: GraphQL for Public API
  - user-service Architecture

Would update (1):
  - auth-service Architecture (local changes)

Unchanged (12)

Conflicts (0)

Run with --mode=apply to execute
```

**Apply mode:**
```
Documentation Sync Complete
===========================
Created: 3 pages
Updated: 1 page
Conflicts: 0

View in Confluence: https://...
```
