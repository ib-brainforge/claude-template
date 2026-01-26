# Command Template - Unified Format

## Format Specification

```markdown
---
name: /command-name
description: Brief description shown in /help
allowed_tools: [Tool1, Tool2]
---

# Purpose
<!-- What this command does when invoked -->

# Arguments
<!-- Optional arguments user can pass -->
- `arg1`: Description (required|optional)
- `arg2`: Description (default: value)

# Workflow
<!-- Exact steps to execute -->
1. Parse arguments
2. Execute action
3. Report result

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
- Often delegate to agents for heavy lifting

### Example Pattern

```markdown
---
name: /validate
description: Validate architecture against decisions
---

# Purpose
Quick validation check, delegates to validation agents.

# Arguments
- `scope`: all|service|frontend|backend (default: all)
- `service`: Service name if scope=service

# Workflow
1. Parse scope argument
2. Delegate to appropriate validation agent(s)
3. Aggregate results
4. Display summary

# Output
Validation summary with pass/fail status.
```
