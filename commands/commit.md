---
name: /commit
description: Intelligently commit changes across repositories
allowed_tools: [Task, Bash, Read]
---

# Purpose
Analyze changes, generate conventional commit messages, and commit across multiple repos.

# Arguments
- `--repos`: all|changed|<repo-name> (default: changed)
- `--dry-run`: Preview commits without executing (default: true)
- `--push`: Push after commit (default: false)
- `--ticket`: Ticket/issue ID to include
- `--message`: Override auto-generated message

# Workflow

1. Parse arguments
2. Spawn commit-manager agent:
   ```
   Task: commit-manager
   Variables:
     $REPOS_ROOT = <configured repos root>
     $TARGET_REPOS = <from args>
     $DRY_RUN = <from args>
     $AUTO_PUSH = <from args>
     $TICKET_ID = <from args>
   ```
3. Display results

# Examples

```
/commit
→ Preview commits for all changed repos (dry run)

/commit --dry-run=false --push
→ Commit and push all changed repos

/commit --repos=user-api --push
→ Commit and push specific repo

/commit --ticket=JIRA-123
→ Include ticket reference in commits
```

# Output

**Dry run:**
```
Commit Preview
==============

Repository: user-api (feature/auth)
  Type: feat(auth)
  Subject: add OAuth2 support
  Files: 5 changed (+120, -30)

  Would commit:
  ---
  feat(auth): add OAuth2 support

  Changes:
  - Add src/auth/oauth.ts
  - Update src/auth/middleware.ts
  - Add tests/auth/oauth.test.ts
  ---

Repository: frontend-app (feature/auth)
  Type: feat(login)
  Subject: add OAuth login button
  Files: 3 changed (+45, -10)

Run with --dry-run=false to execute
```

**After commit:**
```
Commits Created
===============

✅ user-api
   feat(auth): add OAuth2 support
   SHA: abc123
   Pushed: yes

✅ frontend-app
   feat(login): add OAuth login button
   SHA: def456
   Pushed: yes

2 repositories committed and pushed
```
