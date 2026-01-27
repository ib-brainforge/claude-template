---
name: design-patterns
description: |
  Validate and suggest design patterns for your applications.
  All specific patterns and packages loaded from knowledge files.
triggers:
  - /patterns
  - /design-patterns
  - check patterns
  - suggest patterns
  - validate patterns
---

# Purpose

Validate existing code against established design patterns, suggest appropriate
patterns for new features, and ensure consistent use of core package components.
All specific patterns are defined in knowledge files.

# Usage

```bash
# Validate existing code
/patterns validate src/components/
/patterns validate src/services/

# Suggest patterns for a feature
/patterns suggest "feature description here"

# Review code changes
/patterns review                    # Review staged changes
/patterns review --pr 123           # Review PR
```

# Variables

- `$MODE (string)`: validate|suggest|review (default: validate)
- `$TARGET (string)`: File, directory, or feature description
- `$TECH_STACK (string)`: frontend|backend|both (auto-detect)
- `$STRICT (bool)`: Fail on pattern violations (default: false)
- `$OUTPUT_DIR (string)`: Where to write reports

# Knowledge References

This skill loads ALL domain-specific information from:

```
knowledge/architecture/design-patterns.md     → Required patterns for frontend/backend
knowledge/validation/backend-patterns.md       → What to avoid with detection rules
knowledge/packages/core-packages.md       → Shared libraries and their APIs
knowledge/architecture/tech-stack.md          → Framework versions and conventions
```

**IMPORTANT**: Do not hardcode any framework names, package names, or specific
patterns in this skill. All such information must come from knowledge files.

# Cookbook

| Recipe | Purpose |
|--------|---------|
| `validate-mode.md` | How to validate existing code |
| `suggest-mode.md` | How to recommend patterns |
| `review-mode.md` | How to review code changes |
| `pattern-matching.md` | Feature-to-pattern mapping rules |

# Tools

| Tool | Purpose |
|------|---------|
| `detect-stack.py` | Detect frameworks and tech stack |
| `pattern-scanner.py` | Scan code for pattern usage |
| `component-checker.py` | Check core component usage |
| `anti-pattern-detector.py` | Find anti-patterns |
| `parse-feature.py` | Extract keywords from feature description |
| `get-changes.py` | Get git diff or PR changes |
| `generate-report.py` | Format output reports |

# Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DESIGN PATTERNS WORKFLOW                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. LOAD KNOWLEDGE                                                           │
│     └──► Read design-patterns.md, anti-patterns.md, core-packages.md         │
│                                                                              │
│  MODE: validate                                                              │
│  ──────────────                                                              │
│  2. Detect tech stack                                                        │
│  3. Scan for pattern usage (against knowledge)                               │
│  4. Check core component usage (against knowledge)                           │
│  5. Detect anti-patterns (against knowledge)                                 │
│  6. Generate compliance report                                               │
│                                                                              │
│  MODE: suggest                                                               │
│  ─────────────                                                               │
│  2. Parse feature requirements                                               │
│  3. Match to pattern categories (from knowledge)                             │
│  4. Identify core components to use (from knowledge)                         │
│  5. Generate recommendations with examples (from knowledge)                  │
│                                                                              │
│  MODE: review                                                                │
│  ────────────                                                                │
│  2. Get code changes (diff/PR)                                               │
│  3. Analyze pattern compliance (against knowledge)                           │
│  4. Generate review comments                                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

# Instructions

## 1. Load Knowledge First
Always start by reading:
- `knowledge/architecture/design-patterns.md` - Get required patterns
- `knowledge/validation/backend-patterns.md` - Get anti-patterns to detect
- `knowledge/packages/core-packages.md` - Get core component list

## Mode: Validate

### 2. Detect Tech Stack
```bash
python skills/design-patterns/tools/detect-stack.py \
  --target "$TARGET" \
  --output /tmp/stack-info.json
```

### 3. Spawn Design Pattern Advisor
```
Task: spawn design-pattern-advisor
Prompt: |
  Validate design patterns in: $TARGET
  Tech stack: [from detection]
  Strict mode: $STRICT

  Use knowledge from:
  - knowledge/architecture/design-patterns.md
  - knowledge/validation/backend-patterns.md
  - knowledge/packages/core-packages.md

  Return detailed report with locations and suggestions.
```

### 4. Generate Report
```bash
python skills/design-patterns/tools/generate-report.py \
  --validation /tmp/validation-result.json \
  --format markdown \
  --output "$OUTPUT_DIR/pattern-report.md"
```

## Mode: Suggest

### 2. Parse Feature Description
```bash
python skills/design-patterns/tools/parse-feature.py \
  --description "$TARGET" \
  --output /tmp/feature-keywords.json
```

### 3. Spawn Design Pattern Advisor
```
Task: spawn design-pattern-advisor
Prompt: |
  Suggest patterns for feature: $TARGET
  Mode: suggest

  Use knowledge from:
  - knowledge/architecture/design-patterns.md
  - knowledge/packages/core-packages.md

  Provide:
  - Recommended patterns with rationale (from knowledge)
  - Core components to use (from knowledge)
  - Code examples for your stack (from knowledge)
  - Common pitfalls to avoid (from knowledge)
```

## Mode: Review

### 2. Get Changes
```bash
python skills/design-patterns/tools/get-changes.py \
  --staged \
  --output /tmp/changes.json
```

### 3. Spawn Design Pattern Advisor
```
Task: spawn design-pattern-advisor
Prompt: |
  Review code changes:
  Changes: [from changes.json]
  Mode: review

  Use knowledge from:
  - knowledge/architecture/design-patterns.md
  - knowledge/validation/backend-patterns.md

  For each file changed:
  - Check pattern compliance
  - Identify improvements
  - Suggest specific changes
```

# Report Format

```json
{
  "skill": "design-patterns",
  "mode": "validate|suggest|review",
  "status": "PASS|WARN|FAIL",
  "target": "",
  "tech_stack": {},
  "score": {
    "pattern_compliance": 0,
    "core_component_usage": 0,
    "anti_pattern_free": 0,
    "overall": 0
  },
  "patterns": {
    "compliant": [],
    "violations": [],
    "missing": []
  },
  "core_components": {
    "used_correctly": [],
    "should_use": [],
    "deprecated_usage": []
  },
  "anti_patterns": [],
  "recommendations": []
}
```
