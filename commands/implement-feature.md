---
name: /implement-feature
description: Implement a feature using the multi-agent system (plan + execute)
allowed_tools: [Read, Task]
---

# Purpose

Plan AND implement a feature using the agent swarm. This is the full workflow from description to committed code.

**CRITICAL**: Do NOT attempt to implement features yourself. The agent system handles everything.

## Usage

```
/implement-feature "Add user authentication with OAuth2"
/implement-feature "Create dashboard widget for sales metrics"
```

## Arguments

- `FEATURE_DESCRIPTION`: Description of what the feature should do

## Workflow

### 1. Spawn feature-planner Agent (Planning Phase)

```
Task: spawn feature-planner
Prompt: |
  Plan feature implementation.

  Feature: [FEATURE_DESCRIPTION]
  $REPOS_ROOT = [current working directory]
  $OUTPUT_DIR = ./plans

  Workflow:
  1. Analyze feature requirements
  2. Discover affected services
  3. Spawn architectural subagents (parallel)
  4. Synthesize implementation plan
  5. Validate plan
  6. Return plan for implementation
```

### 2. Review Plan with User

Present the plan summary:
- Affected services
- Implementation phases
- Estimated effort
- Any warnings or concerns

Ask: "Proceed with implementation?"

### 3. Execute Implementation (if approved)

For each task in the plan, spawn appropriate agents:

**Backend tasks:**
```
Task: spawn backend-pattern-validator
Prompt: |
  Implement backend task: [task description]
  Service: [affected service]
  Follow plan: [relevant plan section]
```

**Frontend tasks:**
```
Task: spawn frontend-pattern-validator
Prompt: |
  Implement frontend task: [task description]
  Service: [affected service]
  Follow plan: [relevant plan section]
```

### 4. Validate All Changes

```
Task: spawn validation-orchestrator
Prompt: |
  Validate all changes for feature: [FEATURE_DESCRIPTION]
  Changed services: [list]
```

### 5. Commit Changes

```
Task: spawn commit-manager
Prompt: |
  Commit all changes for feature: [FEATURE_DESCRIPTION]
  Type: feat
  Scope: [affected services]
```

## What Gets Spawned

```
/implement-feature "Add OAuth2 authentication"
       │
       ▼
┌─────────────────┐
│ feature-planner │ ◄── Phase 1: Planning
└────────┬────────┘
         │
         ├──► master-architect
         ├──► frontend-pattern-validator
         ├──► backend-pattern-validator
         ├──► core-validator
         └──► infrastructure-validator
                    │
                    ▼
           [User approves plan]
                    │
                    ▼
┌─────────────────────────────┐
│ Implementation Workers      │ ◄── Phase 2: Build
├─────────────────────────────┤
│ (spawned per task in plan)  │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│ validation-orchestrator     │ ◄── Phase 3: Validate
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│ commit-manager              │ ◄── Phase 4: Commit
└─────────────────────────────┘
```

## Related Commands

- `/plan-feature` - Planning only (no implementation)
- `/fix-bugs TICKET-ID` - Fix bugs from Jira
- `/validate` - Validate current architecture
