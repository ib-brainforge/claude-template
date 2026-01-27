---
name: validation
description: |
  Architectural validation across repositories.
  Domain-agnostic - references knowledge/ for project-specific rules.
triggers:
  - /validate
  - validate architecture
  - check architecture
  - run validation
---

# Purpose

Run comprehensive architectural validation across all services. Domain-agnostic skill that references `knowledge/` for project-specific rules.

# Usage

```bash
/validate                           # Validate all services
/validate --scope frontend          # Frontend services only
/validate --scope backend           # Backend services only
/validate --service user-service    # Single service
/validate --quick                   # Structure only (fast)
```

# Variables

- `$SCOPE (string)`: all|frontend|backend|infrastructure
- `$SERVICE (string, optional)`: Specific service
- `$QUICK (bool)`: Skip deep analysis
- `$OUTPUT_DIR (string)`: Report output location

# Knowledge References

This skill loads domain knowledge from:

```
knowledge/architecture/system-architecture.md        → System structure
knowledge/architecture/service-boundaries.md  → Interaction rules
knowledge/architecture/design-patterns.md     → Required patterns
knowledge/validation/backend-patterns.md       → What to avoid
knowledge/architecture/tech-stack.md          → Framework versions
```

# Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    VALIDATION WORKFLOW                           │
├─────────────────────────────────────────────────────────────────┤
│  1. DISCOVER       → tools/discover-services.py                  │
│  2. STRUCTURE      → tools/validate-structure.py                 │
│  3. PATTERNS       → Spawn: design-pattern-advisor               │
│  4. BOUNDARIES     → Spawn: master-architect                     │
│  5. DEPENDENCIES   → tools/check-dependencies.py                 │
│  6. AGGREGATE      → tools/aggregate-results.py                  │
└─────────────────────────────────────────────────────────────────┘
```

# Instructions

## Step 1: Discover Services

```bash
python skills/validation/tools/discover-services.py \
  --root $REPOS_ROOT \
  --output /tmp/discovered-services.json
```

See `cookbook/discover-services.md` for details.

## Step 2: Validate Structure

```bash
python skills/validation/tools/validate-structure.py \
  --services /tmp/discovered-services.json \
  --output /tmp/structure-validation.json
```

See `cookbook/validate-structure.md` for expected structure rules.

## Step 3: Pattern Validation (Parallel)

```
Task: spawn design-pattern-advisor
Prompt: |
  Mode: validate
  Target: [discovered services]
  Load: knowledge/architecture/design-patterns.md, knowledge/validation/backend-patterns.md
  Return: JSON validation report
```

## Step 4: Boundary Validation

```
Task: spawn master-architect
Prompt: |
  Validate service boundaries and architecture.
  Services: [from discovery]
  Load: knowledge/architecture/service-boundaries.md, knowledge/architecture/system-architecture.md
  Return: JSON validation report
```

## Step 5: Check Dependencies

```bash
python skills/validation/tools/check-dependencies.py \
  --services /tmp/discovered-services.json \
  --output /tmp/dependency-check.json
```

## Step 6: Aggregate Results

```bash
python skills/validation/tools/aggregate-results.py \
  --inputs /tmp/*-validation.json \
  --output "$OUTPUT_DIR/validation-report.json"
```

See `cookbook/aggregate-results.md` for aggregation logic.

# Report Format

```json
{
  "skill": "validation",
  "status": "PASS|WARN|FAIL",
  "summary": {
    "services_checked": 40,
    "passed": 38,
    "warnings": 1,
    "failures": 1
  },
  "categories": {
    "structure": { "status": "PASS" },
    "patterns": { "status": "WARN", "issues": [...] },
    "boundaries": { "status": "PASS" },
    "dependencies": { "status": "FAIL", "issues": [...] }
  },
  "critical_issues": [...],
  "recommendations": [...]
}
```

# Cookbook

| Recipe | Purpose |
|--------|---------|
| `discover-services.md` | How service discovery works |
| `validate-structure.md` | Structure validation rules |
| `aggregate-results.md` | Result aggregation logic |

# Tools

| Tool | Purpose |
|------|---------|
| `discover-services.py` | Find and classify services |
| `validate-structure.py` | Check directory layout |
| `check-dependencies.py` | Analyze dependency graph |
| `aggregate-results.py` | Combine validation results |

# Related Skills

- `design-patterns` - Detailed pattern validation
- `feature-planning` - Plan fixes for issues
- `commit-manager` - Commit validation fixes
