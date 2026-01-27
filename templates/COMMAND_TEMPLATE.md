# Command Template - Unified Format

## Format Specification

```markdown
---
name: /command-name
description: Brief description shown in /help
allowed_tools: [Read, Grep, Glob, Task]
---

# Purpose
<!-- What this command does when invoked -->

# Arguments
<!-- Optional arguments user can pass -->
- `arg1`: Description (required|optional)
- `arg2`: Description (default: value)

# Knowledge References
<!-- If command needs knowledge context -->
```
knowledge/[category]/[topic].md              → Base patterns
knowledge/[category]/[topic].learned.yaml    → Learned patterns
```

# Workflow
<!-- Exact steps to execute -->
1. Parse arguments
2. Load knowledge (if needed)
3. Execute action or delegate to agent
4. Report result

# Output
<!-- What user sees -->
```

## Design Principles

### Commands vs Agents vs Skills

| Type | Invocation | Context | Use For |
|------|------------|---------|---------|
| Command | `/command` | Main | Quick actions, shortcuts |
| Agent | Auto/delegated | Subagent | Heavy work, isolation |
| Skill | Auto-loaded | Any | Reusable capabilities |

### Commands Should Be
- Quick to execute
- User-invoked explicitly
- Minimal context impact
- Delegate to agents for heavy lifting (via Task tool)

### Tool Usage Rules
- Use built-in tools (Read, Grep, Glob) for analysis
- Use Task to spawn agents for complex work
- Use Bash ONLY for git commands or build tools
- **NEVER** use Python scripts for analysis

## Example: Validation Command

```markdown
---
name: /validate
description: Validate architecture against patterns and decisions
allowed_tools: [Read, Task]
---

# Purpose
Quick validation check, delegates to validation agents.

# Arguments
- `scope`: all|service|frontend|backend (default: all)
- `service`: Service name if scope=service

# Knowledge References
```
knowledge/architecture/system-architecture.md
knowledge/architecture/system-architecture.learned.yaml
```

# Workflow
1. Parse scope argument
2. Load system architecture for context:
   ```
   Read: knowledge/architecture/system-architecture.md
   Read: knowledge/architecture/system-architecture.learned.yaml
   ```
3. Delegate to appropriate validation agent(s):
   ```
   Task: spawn backend-pattern-validator (if scope includes backend)
   Task: spawn frontend-pattern-validator (if scope includes frontend)
   Task: spawn service-validator (if scope=service)
   ```
4. Aggregate results from all validators
5. Display summary with pass/fail status

# Output
Validation summary with pass/fail status and issue counts.
```

## Example: Commit Command

```markdown
---
name: /commit
description: Generate and execute conventional commits across repos
allowed_tools: [Read, Bash, Task]
---

# Purpose
Analyze changes and create semantic commit messages.

# Arguments
- `scope`: all|changed|[repo-name] (default: changed)
- `dry-run`: Preview without committing (default: true)
- `push`: Push after commit (default: false)

# Knowledge References
```
knowledge/commit-conventions.md
knowledge/commit-conventions.learned.yaml
```

# Workflow
1. Parse arguments
2. Load commit conventions:
   ```
   Read: knowledge/commit-conventions.md
   Read: knowledge/commit-conventions.learned.yaml
   ```
3. Delegate to commit-manager agent:
   ```
   Task: spawn commit-manager
   Prompt: |
     $REPOS_ROOT = [path]
     $TARGET_REPOS = [scope]
     $DRY_RUN = [dry-run]
     $AUTO_PUSH = [push]
   ```
4. Display commit summary

# Output
List of commits created (or previewed) per repository.
```

## Example: Plan Command

```markdown
---
name: /plan
description: Create implementation plan for a feature
allowed_tools: [Read, Task]
---

# Purpose
Generate architectural implementation plan with file changes.

# Arguments
- `feature`: Feature description (required)
- `detail`: brief|full (default: brief)

# Knowledge References
```
knowledge/architecture/system-architecture.md
knowledge/architecture/system-architecture.learned.yaml
knowledge/architecture/service-boundaries.md
knowledge/architecture/service-boundaries.learned.yaml
```

# Workflow
1. Parse feature description
2. Load architecture knowledge for context
3. Delegate to feature-planner agent:
   ```
   Task: spawn feature-planner
   Prompt: |
     $FEATURE_DESCRIPTION = [feature]
     $DETAIL_LEVEL = [detail]
   ```
4. Display implementation plan

# Output
Structured plan with affected services, files, and steps.
```

## Command Categories

### Quick Actions (No Agent Delegation)
- `/status` - Check git status across repos
- `/diff` - Show changes across repos
- `/list` - List services/packages

### Delegated Actions (Spawn Agents)
- `/validate` → validation agents
- `/commit` → commit-manager agent
- `/plan` → feature-planner agent
- `/analyze` → master-architect agent

### Knowledge Commands
- `/patterns` - Show available patterns from knowledge
- `/adrs` - List architectural decisions
- `/boundaries` - Show service boundaries

## Tool Selection Guide

| Task | Tool | When |
|------|------|------|
| Read knowledge | Read | Always for loading context |
| Find files | Glob | Quick file discovery |
| Search patterns | Grep | Quick pattern check |
| Complex validation | Task | Delegate to validator agents |
| Git operations | Bash | Status, diff, log |
| Build/test | Bash | npm, dotnet commands |
