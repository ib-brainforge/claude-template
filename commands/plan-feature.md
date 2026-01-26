---
name: plan-feature
description: Create comprehensive implementation plan for a new feature
usage: /plan-feature "<feature-name>" "<description>"
examples:
  - /plan-feature "user-auth" "Implement user authentication with login, logout, and password reset"
  - /plan-feature "notifications" "Real-time notification system for order updates"
  - /plan-feature "dashboard-analytics" "Admin dashboard with user activity charts and metrics"
---

# Purpose
Entry point for feature planning workflow. Spawns feature-planner agent to analyze
requirements, consult architectural subagents, generate implementation plan, and validate.

# Arguments
- `$1 (feature-name)`: Short identifier for the feature (kebab-case)
- `$2 (description)`: Detailed description of feature requirements

# Environment Variables
- `REPOS_ROOT`: Path to repositories root (default: current directory)
- `OUTPUT_DIR`: Where to write plan artifacts (default: ./feature-plans)
- `VALIDATION_LEVEL`: strict|standard|lenient (default: standard)

# Workflow

```
/plan-feature "user-auth" "Login, logout, password reset with email verification"
                                          │
                                          ▼
                                 ┌─────────────────┐
                                 │ Parse Arguments │
                                 └────────┬────────┘
                                          │
                                          ▼
                                 ┌─────────────────┐
                                 │ Spawn           │
                                 │ feature-planner │
                                 │ (subagent)      │
                                 └────────┬────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
                    ▼                     ▼                     ▼
             ┌───────────┐        ┌───────────┐        ┌───────────┐
             │ Discovery │        │ Arch      │        │ Pattern   │
             │ Phase     │        │ Consult   │        │ Analysis  │
             └─────┬─────┘        └─────┬─────┘        └─────┬─────┘
                   │                    │                    │
                   └────────────────────┼────────────────────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │ Plan Synthesis  │
                               └────────┬────────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │ plan-validator  │
                               │ (subagent)      │
                               └────────┬────────┘
                                        │
                          ┌─────────────┼─────────────┐
                          │             │             │
                          ▼             ▼             ▼
                    ┌──────────┐ ┌──────────┐ ┌──────────┐
                    │   PASS   │ │   WARN   │ │   FAIL   │
                    │ Output   │ │ Output + │ │ Show     │
                    │ Plan     │ │ Warnings │ │ Issues   │
                    └──────────┘ └──────────┘ └──────────┘
```

# Instructions

## 1. Validate Input
```
If $1 (feature-name) empty:
  → Error: "Usage: /plan-feature <name> <description>"

If $2 (description) empty:
  → Error: "Please provide a feature description"
```

## 2. Spawn Feature Planner
```
Task: spawn feature-planner
Prompt: |
  Create implementation plan for feature:

  Feature Name: $1
  Description: $2

  Repository Root: $REPOS_ROOT
  Output Directory: $OUTPUT_DIR
  Validation Level: $VALIDATION_LEVEL

  Execute full workflow:
  1. Discover affected services
  2. Consult all architectural subagents
  3. Synthesize requirements
  4. Generate phased implementation plan
  5. Validate plan against architecture
  6. Output plan document and task breakdown
```

## 3. Handle Result

### On PASS
```
✅ Feature plan created successfully!

📄 Plan document: $OUTPUT_DIR/feature-$1-plan.md
📋 Task breakdown: $OUTPUT_DIR/feature-$1-tasks.json

Summary:
- Phases: {plan.phases}
- Tasks: {plan.total_tasks}
- Estimated effort: {plan.estimated_days} days
- Affected services: {plan.affected_services}

Plan is approved for implementation.
```

### On WARN
```
⚠️ Feature plan created with warnings

📄 Plan document: $OUTPUT_DIR/feature-$1-plan.md
📋 Task breakdown: $OUTPUT_DIR/feature-$1-tasks.json

Warnings:
{list warnings}

Review warnings before proceeding with implementation.
```

### On FAIL
```
❌ Feature plan validation failed

Blocking Issues:
{list blocking issues with suggestions}

Please address these issues and run /plan-feature again.
```

# Output Files

| File | Description |
|------|-------------|
| `feature-{name}-plan.md` | Full implementation plan document |
| `feature-{name}-tasks.json` | Task breakdown for import to tracker |
| `feature-{name}-validation.json` | Validation results |

# Examples

## Simple Feature
```
/plan-feature "dark-mode" "Add dark mode toggle to application settings"
```

## Complex Feature
```
/plan-feature "multi-tenant" "Convert single-tenant app to multi-tenant with organization isolation, tenant-specific configurations, and data segregation"
```

## With Environment Variables
```
REPOS_ROOT=/home/dev/projects \
OUTPUT_DIR=/home/dev/plans \
VALIDATION_LEVEL=strict \
/plan-feature "payment-integration" "Integrate Stripe for subscription billing"
```

# Follow-up Commands

After plan is approved:
```
# Start implementation with commit tracking
/commit --feature "user-auth"

# Validate changes against architecture
/validate --scope affected-services

# Update packages if core changes made
/update-packages
```
