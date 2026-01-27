---
name: commit-manager
description: |
  Intelligent commit message generation across multiple repositories.
  Analyzes changes, detects commit type, generates conventional commits.
triggers:
  - /commit
  - commit changes
  - generate commit
  - push changes
---

# Purpose

Generate intelligent, consistent commit messages across all repositories.
Analyzes diffs, detects change types (feat/fix/chore/etc), and optionally
uses local LLM for cost-effective message generation.

# Usage

```
/commit                              # Commit all staged changes
/commit --repo user-service          # Single repo
/commit --scope frontend             # All frontend repos
/commit --dry-run                    # Preview without committing
/commit --push                       # Commit and push
/commit --use-local-llm              # Force local LLM for message generation
```

# Variables

- `$REPOS_ROOT (string)`: Path to repositories (default: .)
- `$REPO (string, optional)`: Specific repo to commit
- `$SCOPE (string, optional)`: frontend|backend|all
- `$DRY_RUN (bool)`: Preview only (default: false)
- `$PUSH (bool)`: Push after commit (default: false)
- `$USE_LOCAL_LLM (bool)`: Use Ollama/LM Studio (default: auto)
- `$FEATURE_TAG (string, optional)`: Feature reference for commits

# Knowledge References

This skill loads domain knowledge from:

```
knowledge/commit-conventions.md  → Commit message format and rules
```

# Cookbook

| Recipe | Purpose |
|--------|---------|
| `discover-changes.md` | How to find repos with changes |
| `generate-message.md` | Message generation with LLM fallback |
| `commit-type-detection.md` | How to detect commit type |

# Tools

| Tool | Purpose |
|------|---------|
| `git-operations.py` | Multi-command git operations tool |

# Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       COMMIT MANAGER WORKFLOW                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. DISCOVER CHANGES                                                         │
│     └──► scripts/git-operations.py status                                    │
│          Find repos with staged/unstaged changes                             │
│                                                                              │
│  2. ANALYZE EACH REPO                                                        │
│     └──► scripts/git-operations.py diff                                      │
│          Get detailed diff for analysis                                      │
│                                                                              │
│  3. DETECT COMMIT TYPE                                                       │
│     └──► scripts/git-operations.py detect-type                               │
│          Determine: feat|fix|chore|refactor|docs|test|style                  │
│                                                                              │
│  4. GENERATE MESSAGE                                                         │
│     ├──► TRY: local-llm-worker (if available)                                │
│     │         Ping → Generate → Validate                                     │
│     │                                                                        │
│     └──► FALLBACK: Claude API                                                │
│               Generate conventional commit message                           │
│                                                                              │
│  5. COMMIT (if not dry-run)                                                  │
│     └──► scripts/git-operations.py commit                                    │
│                                                                              │
│  6. PUSH (if --push)                                                         │
│     └──► scripts/git-operations.py push                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

# Instructions

## 1. Discover Changes

```bash
python skills/commit-manager/tools/git-operations.py status \
  --repos-root $REPOS_ROOT \
  --scope $SCOPE \
  --output /tmp/git-status.json
```

## 2. For Each Repo with Changes

### 2.1 Get Diff
```bash
python skills/commit-manager/tools/git-operations.py diff \
  --repo $REPO_PATH \
  --output /tmp/repo-diff.json
```

### 2.2 Detect Commit Type
```bash
python skills/commit-manager/tools/git-operations.py detect-type \
  --diff /tmp/repo-diff.json \
  --output /tmp/commit-type.json
```

### 2.3 Generate Message

**Try Local LLM First (if enabled):**
```
Task: spawn local-llm-worker
Prompt: |
  Generate commit message:
  Repo: $REPO_NAME
  Type: $COMMIT_TYPE
  Diff Summary: $DIFF_SUMMARY
  Files Changed: $FILES

  Follow conventional commits format.
```

**Handle Response:**
- If `status: UNAVAILABLE` or `status: FAIL` → Use Claude API
- If `status: PASS` → Use generated message

**Claude Fallback:**
Analyze diff and generate message following knowledge/commit-conventions.md

### 2.4 Validate Message
Ensure message follows:
- Conventional commit format: `type(scope): description`
- First line ≤ 72 characters
- Body wrapped at 80 characters
- References issues if applicable

## 3. Execute Commits

```bash
# Dry run - preview only
python skills/commit-manager/tools/git-operations.py commit \
  --repo $REPO_PATH \
  --message "$COMMIT_MESSAGE" \
  --dry-run \
  --output /tmp/commit-preview.json

# Actual commit
python skills/commit-manager/tools/git-operations.py commit \
  --repo $REPO_PATH \
  --message "$COMMIT_MESSAGE" \
  --output /tmp/commit-result.json
```

## 4. Push (if requested)

```bash
python skills/commit-manager/tools/git-operations.py push \
  --repo $REPO_PATH \
  --output /tmp/push-result.json
```

# Commit Type Detection Rules

| Pattern | Type |
|---------|------|
| New files, new functions | `feat` |
| Bug fixes, error handling | `fix` |
| Dependencies, configs | `chore` |
| Code restructuring | `refactor` |
| Documentation changes | `docs` |
| Test files | `test` |
| Formatting only | `style` |
| Performance improvements | `perf` |
| CI/CD changes | `ci` |

# Report Format

```json
{
  "skill": "commit-manager",
  "status": "PASS|WARN|FAIL",
  "summary": {
    "repos_processed": 5,
    "commits_created": 4,
    "pushed": 4,
    "skipped": 1
  },
  "commits": [
    {
      "repo": "user-service",
      "type": "feat",
      "message": "feat(auth): add OAuth2 support for Google login",
      "files_changed": 8,
      "insertions": 245,
      "deletions": 12,
      "sha": "abc123",
      "pushed": true,
      "llm_source": "local-ollama"
    }
  ],
  "skipped": [
    {
      "repo": "docs",
      "reason": "No staged changes"
    }
  ]
}
```

# Local LLM Integration

The skill automatically tries local LLM first for cost savings:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MESSAGE GENERATION FLOW                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. Check $USE_LOCAL_LLM setting                                             │
│     ├── "force" → Always use local, fail if unavailable                      │
│     ├── "never" → Always use Claude                                          │
│     └── "auto" (default) → Try local, fallback to Claude                     │
│                                                                              │
│  2. If local enabled:                                                        │
│     └──► Spawn local-llm-worker or lmstudio-llm-worker                       │
│          └──► Ping first                                                     │
│               ├── Available → Generate message                               │
│               └── Unavailable → Fallback to Claude                           │
│                                                                              │
│  3. Validate generated message regardless of source                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

# Follow-up Skills

After committing:
- `package-release` - If core packages changed, propagate versions
- `validation` - Validate architectural compliance
