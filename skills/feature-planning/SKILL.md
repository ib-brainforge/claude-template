---
name: feature-planning
description: |
  Comprehensive feature analysis and implementation planning.
  Gathers architectural inputs, generates phased plans, validates against rules.
triggers:
  - /plan-feature
  - plan feature
  - create implementation plan
  - design feature
---

# Purpose

Analyze feature requests, consult architectural subagents, and produce validated
implementation plans for full-stack features (frontend + backend slices).

# Usage

```
/plan-feature "user-auth" "Login, logout, password reset with OAuth"
/plan-feature "notifications" "Real-time notifications via WebSocket"
/plan-feature "dashboard" "Admin analytics dashboard with charts"
```

# Variables

- `$FEATURE_NAME (string)`: Short identifier (kebab-case)
- `$DESCRIPTION (string)`: Detailed feature requirements
- `$REPOS_ROOT (string)`: Path to repositories (default: .)
- `$OUTPUT_DIR (string)`: Where to write plans (default: ./feature-plans)
- `$VALIDATION_LEVEL (string)`: strict|standard|lenient (default: standard)

# Context Requirements

- references/system-architecture.md
- references/rules/*.md
- references/design-patterns/*.md
- Access to all repository roots

# Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FEATURE PLANNING WORKFLOW                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PHASE 1: DISCOVERY                                                          │
│  ─────────────────                                                           │
│  scripts/feature-analysis.py discover                                        │
│    • Extract keywords from description                                       │
│    • Scan repos for affected services                                        │
│    • Classify: frontend, backend, shared, infra                              │
│                                                                              │
│  PHASE 2: DESIGN PATTERNS                                                    │
│  ────────────────────────                                                    │
│  Spawn: design-pattern-advisor (suggest mode)                                │
│    • Recommend patterns for the feature                                      │
│    • Identify core components to use                                         │
│    • Provide code examples                                                   │
│                                                                              │
│  PHASE 3: ARCHITECTURAL CONSULTATION                                         │
│  ───────────────────────────────────                                         │
│  Spawn parallel subagents:                                                   │
│    ├──► master-architect ──► System constraints                              │
│    ├──► frontend-pattern-validator ──► UI patterns                           │
│    ├──► backend-pattern-validator ──► API patterns                           │
│    ├──► core-validator ──► Library impacts                                   │
│    └──► infrastructure-validator ──► Deployment needs                        │
│                                                                              │
│  PHASE 4: SYNTHESIS                                                          │
│  ─────────────────                                                           │
│  scripts/feature-analysis.py synthesize                                      │
│    • Combine all architectural inputs                                        │
│    • Include design pattern recommendations                                  │
│    • Identify dependencies                                                   │
│    • Generate phased task breakdown                                          │
│                                                                              │
│  PHASE 5: VALIDATION                                                         │
│  ───────────────────                                                         │
│  Spawn: plan-validator                                                       │
│    • Check 8 validation dimensions                                           │
│    • Verify pattern compliance                                               │
│    • Security compliance                                                     │
│    • Dependency ordering                                                     │
│                                                                              │
│  PHASE 6: OUTPUT                                                             │
│  ────────────────                                                            │
│  scripts/feature-analysis.py write-plan                                      │
│    • feature-{name}-plan.md                                                  │
│    • feature-{name}-tasks.json                                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

# Instructions

## Phase 1: Discovery

```bash
python skills/feature-planning/scripts/feature-analysis.py discover \
  --feature "$FEATURE_NAME" \
  --description "$DESCRIPTION" \
  --repos-root $REPOS_ROOT \
  --output /tmp/affected-services.json
```

## Phase 2: Design Pattern Recommendations

```
Task: spawn design-pattern-advisor
Prompt: |
  Suggest design patterns for feature:
  Feature: $FEATURE_NAME
  Description: $DESCRIPTION
  Mode: suggest

  Provide:
  - Recommended patterns with rationale
  - Core components to use (@core/ui, Core.Data, etc.)
  - Code examples for frontend and backend
  - Common pitfalls to avoid
```

Save output to `/tmp/design-patterns-input.json`

## Phase 3: Architectural Consultation

**Spawn these subagents in PARALLEL:**

### Master Architect
```
Task: spawn master-architect
Prompt: |
  Analyze feature for architectural fit:
  Feature: $FEATURE_NAME
  Description: $DESCRIPTION
  Affected: [from discovery]

  Provide: constraints, communication patterns, concerns
```

### Frontend Analysis
```
Task: spawn frontend-pattern-validator
Prompt: |
  Analyze frontend requirements:
  Feature: $FEATURE_NAME
  Description: $DESCRIPTION

  Provide: component patterns, state management, UI consistency
```

### Backend Analysis
```
Task: spawn backend-pattern-validator
Prompt: |
  Analyze backend requirements:
  Feature: $FEATURE_NAME
  Description: $DESCRIPTION

  Provide: API design, database changes, security requirements
```

### Core Library Impact
```
Task: spawn core-validator
Prompt: |
  Analyze core library impact:
  Feature: $FEATURE_NAME

  Provide: shared utilities needed, breaking change risks
```

### Infrastructure
```
Task: spawn infrastructure-validator
Prompt: |
  Analyze infrastructure needs:
  Feature: $FEATURE_NAME

  Provide: deployment changes, CI/CD updates, scaling needs
```

## Phase 4: Synthesis

```bash
python skills/feature-planning/scripts/feature-analysis.py synthesize \
  --master-input /tmp/master-input.json \
  --frontend-input /tmp/frontend-input.json \
  --backend-input /tmp/backend-input.json \
  --core-input /tmp/core-input.json \
  --infra-input /tmp/infra-input.json \
  --design-patterns-input /tmp/design-patterns-input.json \
  --output /tmp/synthesized.json
```

## Phase 5: Validation

```
Task: spawn plan-validator
Prompt: |
  Validate implementation plan:
  Feature: $FEATURE_NAME
  Plan: [synthesized plan]
  Level: $VALIDATION_LEVEL

  Check all 8 dimensions, return issues and recommendations.
```

## Phase 6: Output

```bash
# Generate plan document
python skills/feature-planning/scripts/feature-analysis.py write-plan \
  --feature "$FEATURE_NAME" \
  --plan /tmp/validated-plan.json \
  --output "$OUTPUT_DIR/feature-$FEATURE_NAME-plan.md"

# Generate task export (optional)
python skills/feature-planning/scripts/feature-analysis.py export-tasks \
  --plan /tmp/validated-plan.json \
  --format github-issues \
  --output "$OUTPUT_DIR/feature-$FEATURE_NAME-tasks.json"
```

# Report Format

```json
{
  "skill": "feature-planning",
  "status": "PASS|WARN|FAIL",
  "feature": {
    "name": "user-auth",
    "description": "Login, logout, password reset"
  },
  "discovery": {
    "affected_services": ["auth-service", "user-frontend"],
    "frontend_components": ["LoginForm", "ResetPassword"],
    "backend_endpoints": ["/api/auth/*"],
    "database_changes": true
  },
  "plan": {
    "phases": 5,
    "total_tasks": 24,
    "estimated_days": 8,
    "complexity": "medium"
  },
  "validation": {
    "status": "PASS",
    "warnings": [],
    "blockers": []
  },
  "artifacts": {
    "plan_document": "feature-user-auth-plan.md",
    "task_export": "feature-user-auth-tasks.json"
  }
}
```

# Output Files

| File | Format | Purpose |
|------|--------|---------|
| `feature-{name}-plan.md` | Markdown | Human-readable implementation plan |
| `feature-{name}-tasks.json` | JSON | Import to Jira/GitHub/Linear |
| `feature-{name}-validation.json` | JSON | Validation results |

# Scripts Reference

| Script | Purpose |
|--------|---------|
| `feature-analysis.py discover` | Find affected services |
| `feature-analysis.py synthesize` | Combine architectural inputs |
| `feature-analysis.py generate-tasks` | Create task breakdown |
| `feature-analysis.py write-plan` | Generate plan document |
| `feature-analysis.py export-tasks` | Export for trackers |
| `plan-validation.py` | Validate plan against rules |

# Task Export Formats

```bash
# GitHub Issues
--format github-issues

# Jira
--format jira

# Linear
--format linear
```

# Follow-up Skills

After plan is approved:
- `design-patterns` - Validate implementation follows recommended patterns
- `validation` - Validate implementation as you build
- `commit-manager` - Generate commit messages for changes
- `package-release` - Update packages if core changes made
