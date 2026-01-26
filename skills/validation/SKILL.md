---
name: validation
description: |
  Architectural validation across microservices repositories.
  Validates service structure, patterns, dependencies, and compliance.
triggers:
  - /validate
  - validate architecture
  - check architecture
  - run validation
---

# Purpose

Run comprehensive architectural validation across all microservices. Spawns specialized
validator subagents to check different aspects of the system.

# Usage

```
/validate                           # Validate all services
/validate --scope frontend          # Frontend services only
/validate --scope backend           # Backend services only
/validate --service user-service    # Single service
/validate --quick                   # Fast check (structure only)
```

# Variables

- `$SCOPE (string)`: all|frontend|backend|infrastructure (default: all)
- `$SERVICE (string, optional)`: Specific service to validate
- `$QUICK (bool)`: Skip deep analysis (default: false)
- `$OUTPUT_DIR (string)`: Where to write reports (default: ./validation-reports)

# Context Requirements

- references/system-architecture.md
- references/rules/*.md
- Access to repository roots

# Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         VALIDATION WORKFLOW                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. DISCOVERY                                                                │
│     └──► scripts/discover-services.py                                        │
│          Find all services, classify by type                                 │
│                                                                              │
│  2. STRUCTURE VALIDATION                                                     │
│     └──► scripts/validate-structure.py                                       │
│          Check directory layout, required files                              │
│                                                                              │
│  3. PATTERN VALIDATION (Parallel Subagents)                                  │
│     ├──► master-architect ──► System-wide rules                              │
│     ├──► frontend-pattern-validator ──► UI patterns                          │
│     ├──► backend-pattern-validator ──► API patterns                          │
│     ├──► infrastructure-validator ──► IaC patterns                           │
│     └──► core-validator ──► Shared library usage                             │
│                                                                              │
│  4. DEPENDENCY CHECK                                                         │
│     └──► scripts/check-dependencies.py                                       │
│          Circular deps, version conflicts                                    │
│                                                                              │
│  5. AGGREGATE                                                                │
│     └──► scripts/aggregate-results.py                                        │
│          Combine all results into final report                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

# Instructions

## 1. Discover Services

```bash
python skills/validation/scripts/discover-services.py \
  --root $REPOS_ROOT \
  --output /tmp/discovered-services.json
```

## 2. Validate Structure

```bash
python skills/validation/scripts/validate-structure.py \
  --services /tmp/discovered-services.json \
  --rules references/rules/ \
  --output /tmp/structure-validation.json
```

## 3. Spawn Pattern Validators (Parallel)

Based on $SCOPE, spawn appropriate validators:

### For Frontend Services
```
Task: spawn frontend-pattern-validator
Prompt: |
  Validate frontend patterns for services: [frontend services list]
  Rules: references/rules/frontend-patterns.md
  Return JSON report.
```

### For Backend Services
```
Task: spawn backend-pattern-validator
Prompt: |
  Validate backend patterns for services: [backend services list]
  Rules: references/rules/backend-patterns.md
  Return JSON report.
```

### For Infrastructure
```
Task: spawn infrastructure-validator
Prompt: |
  Validate infrastructure configs.
  Rules: references/rules/infrastructure.md
  Return JSON report.
```

### System-Wide
```
Task: spawn master-architect
Prompt: |
  Validate system-wide architectural compliance.
  Check service boundaries, communication patterns.
  Return JSON report.
```

## 4. Check Dependencies

```bash
python skills/validation/scripts/check-dependencies.py \
  --services /tmp/discovered-services.json \
  --output /tmp/dependency-check.json
```

## 5. Aggregate Results

```bash
python skills/validation/scripts/aggregate-results.py \
  --structure /tmp/structure-validation.json \
  --frontend /tmp/frontend-validation.json \
  --backend /tmp/backend-validation.json \
  --infra /tmp/infra-validation.json \
  --master /tmp/master-validation.json \
  --dependencies /tmp/dependency-check.json \
  --output "$OUTPUT_DIR/validation-report.json"
```

# Report Format

```json
{
  "skill": "validation",
  "status": "PASS|WARN|FAIL",
  "timestamp": "2024-01-15T10:30:00Z",
  "scope": "all",
  "summary": {
    "services_checked": 40,
    "passed": 38,
    "warnings": 1,
    "failures": 1
  },
  "by_category": {
    "structure": { "status": "PASS", "issues": [] },
    "frontend_patterns": { "status": "PASS", "issues": [] },
    "backend_patterns": { "status": "WARN", "issues": [...] },
    "infrastructure": { "status": "PASS", "issues": [] },
    "dependencies": { "status": "FAIL", "issues": [...] }
  },
  "critical_issues": [
    {
      "service": "order-service",
      "category": "dependencies",
      "issue": "Circular dependency with payment-service",
      "severity": "error"
    }
  ],
  "recommendations": [
    "Break circular dependency via event-driven pattern",
    "Update deprecated API calls in user-service"
  ]
}
```

# Scripts Reference

| Script | Purpose |
|--------|---------|
| `discover-services.py` | Find and classify all services |
| `validate-structure.py` | Check directory structure compliance |
| `check-dependencies.py` | Analyze dependency graph |
| `aggregate-results.py` | Combine validation results |

# Integration with Other Skills

After validation, you might want to:
- `/plan-feature` - Plan fixes for issues found
- `/commit` - Commit validation fixes
- `/sync-docs` - Update architecture docs
