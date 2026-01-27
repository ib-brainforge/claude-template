# Architecture Validation & Multi-Agent System

## CRITICAL: Agent Routing Rules

**You MUST use the multi-agent system for these requests. Do NOT do the work yourself.**

| User Request Pattern | Agent to Spawn | Command |
|---------------------|----------------|---------|
| "fix bugs from Jira/ticket" | `bug-triage` | `/fix-bugs TICKET-ID` |
| "fix bug" / "there's a bug" / "I noticed a bug" | `bug-fixer` | `/fix-bug "description"` |
| "plan feature" / "analyze feature" | `feature-planner` | `/plan-feature "description"` |
| "implement feature" / "build feature" | `feature-planner` | `/implement-feature "description"` |
| "validate/check architecture" | `validation` skill | `/validate` |
| "commit changes" | `commit-manager` | `/commit` |
| "update packages" | `package-release` skill | `/update-packages` |

### How to Spawn Agents

When a request matches the patterns above, use the Task tool:

**For bug fixes (from Jira):**
```
Task: spawn bug-triage
Prompt: |
  Fix bugs from Jira ticket: [TICKET-ID]
  $TICKET_ID = [TICKET-ID]
  $REPOS_ROOT = [path to repos]
```

**For feature planning (no Jira needed):**
```
Task: spawn feature-planner
Prompt: |
  Plan feature implementation.
  Feature: [USER'S FEATURE DESCRIPTION]
  $REPOS_ROOT = [path to repos]
  $OUTPUT_DIR = ./plans
```

**For feature implementation (plan + build):**
```
Task: spawn feature-planner
Prompt: |
  Plan AND implement feature.
  Feature: [USER'S FEATURE DESCRIPTION]
  $REPOS_ROOT = [path to repos]
  $OUTPUT_DIR = ./plans
  Mode: implement (plan first, then execute)
```

**For single bug fix (no Jira):**
```
Task: spawn bug-fixer
Prompt: |
  Fix bug based on description.
  Bug: [USER'S BUG DESCRIPTION]
  $REPOS_ROOT = [path to repos]
```

**NEVER** do the agent's work yourself. The agents have:
- Specific workflows to follow
- Validation steps
- Knowledge file loading
- Observability (logging, prefixes)
- Proper error handling

### Observability

When spawning agents, prefix your output:
```
[main] Detected Jira bug fix request
[main] Spawning bug-triage agent for BF-119...
```

---

## Skills (Entry Points)

| Skill | Trigger | Description |
|-------|---------|-------------|
| `validation` | `/validate` | Run architecture validation |
| `feature-planning` | `/plan-feature "name" "desc"` | Plan feature implementation |
| `design-patterns` | `/patterns` | Validate/suggest design patterns |
| `commit-manager` | `/commit` | Generate commits across repos |
| `package-release` | `/update-packages` | Update NPM/NuGet packages |
| `docs-sync` | `/sync-docs` | Sync to Confluence |
| `jira-integration` | `/jira TICKET-ID` | Fetch/update Jira tickets |

## Commands

| Command | Description |
|---------|-------------|
| `/fix-bugs TICKET-ID` | Fix multiple bugs from Jira ticket (uses bug-triage) |
| `/fix-bug "description"` | Fix single bug you describe (no Jira needed) |
| `/plan-feature "description"` | Plan feature implementation (analysis only) |
| `/implement-feature "description"` | Plan AND implement feature (full workflow) |
| `/validate` | Run architecture validation |
| `/commit` | Generate and execute commits |

## Agent System

### Orchestrating Agents (spawn subagents)
- `bug-triage` - Orchestrates bug fixing from Jira
- `feature-planner` - Plans features across services
- `commit-manager` - Commits + records learnings (SINGLE WRITER)
- `master-architect` - Architectural oversight

### Worker Agents (do specific tasks)
- `bug-fixer` - Applies individual bug fixes
- `backend-pattern-validator` - Validates C#/.NET patterns
- `frontend-pattern-validator` - Validates React/TS patterns
- `knowledge-updater` - Writes to learned YAML files

### Workflow Pattern

```
User Request
    │
    ▼
[main] Detect request type
    │
    ▼
Task: spawn [orchestrator-agent]
    │
    ├──► [orchestrator] loads knowledge
    ├──► [orchestrator] spawns worker agents
    ├──► [workers] do actual work
    ├──► [orchestrator] validates results
    └──► [orchestrator] returns report
```

## Knowledge Files

All agents load patterns from `knowledge/`:
- `knowledge/architecture/` - System design, boundaries
- `knowledge/validation/` - Pattern validation rules
- `knowledge/packages/` - Package config
- `knowledge/jira/` - Jira config

## Single Writer Pattern

**ONLY `commit-manager` writes to learned YAML files.**
All other agents READ from knowledge but do NOT write.

This prevents concurrent write conflicts.
