---
name: /fix-bug
description: Fix a bug described directly (no Jira required)
allowed_tools: [Read, Task]
---

# Purpose

Fix a bug based on your description. No Jira ticket needed.

**CRITICAL**: Do NOT attempt to fix bugs yourself. The bug-fixer agent handles everything.

## Usage

```
/fix-bug "Login fails when password contains special characters"
/fix-bug "Dashboard shows wrong date format for Australian users"
/fix-bug "API returns 500 when user has no profile picture"
```

## Arguments

- `BUG_DESCRIPTION`: Description of the bug to fix

## Workflow

### 1. Spawn bug-fixer Agent

```
Task: spawn bug-fixer
Prompt: |
  Fix bug based on description.

  Bug: [BUG_DESCRIPTION]
  $REPOS_ROOT = [current working directory]

  Workflow:
  1. Analyze bug description for keywords
  2. Search codebase for relevant files
  3. Identify root cause
  4. Apply minimal fix
  5. Run tests
  6. Return report with business summary
```

### 2. Validate Fix

```
Task: spawn backend-pattern-validator (if backend code changed)
Task: spawn frontend-pattern-validator (if frontend code changed)
```

### 3. Commit Changes

```
Task: spawn commit-manager
Prompt: |
  Commit bug fix.
  Type: fix
  Description: [BUG_DESCRIPTION]
```

## What Gets Spawned

```
/fix-bug "Login fails with special characters"
       │
       ▼
┌─────────────┐
│  bug-fixer  │ ◄── Analyzes & fixes
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│ pattern-validator       │ ◄── Validates fix
│ (backend or frontend)   │
└──────┬──────────────────┘
       │
       ▼
┌────────────────┐
│ commit-manager │ ◄── Commits with proper message
└────────────────┘
```

## Example

```
/fix-bug "Users see 'undefined' instead of their name on the profile page"
```

Output:
```
[bug-fixer] Analyzing bug: "Users see 'undefined' instead of their name"
[bug-fixer] Keywords: users, undefined, name, profile page
[bug-fixer] Searching frontend code...
[bug-fixer] Found: apps/web/src/components/Profile.tsx
[bug-fixer] Root cause: Missing null check on user.displayName
[bug-fixer] Applying fix...
[bug-fixer] Running tests...
[bug-fixer] Fix complete

[commit-manager] Committing: fix(web): handle missing display name on profile
```

## Related Commands

- `/fix-bugs TICKET-ID` - Fix multiple bugs from Jira ticket
- `/validate` - Validate architecture after changes
