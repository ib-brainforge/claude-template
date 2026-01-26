---
name: design-patterns
description: |
  Validate and suggest design patterns for your applications.
  Knows your frameworks, core packages, and established patterns.
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

# Usage

```bash
# Validate existing code
/patterns validate src/components/UserList.tsx
/patterns validate src/services/

# Suggest patterns for a feature
/patterns suggest "file upload with progress tracking"
/patterns suggest "user authentication flow"

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

# Context Requirements

- references/design-patterns/frontend-patterns.md
- references/design-patterns/backend-patterns.md
- references/design-patterns/core-components.md
- references/design-patterns/anti-patterns.md

# Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DESIGN PATTERNS WORKFLOW                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  MODE: validate                                                              │
│  ──────────────                                                              │
│  1. Detect tech stack                                                        │
│  2. Scan for pattern usage                                                   │
│  3. Check core component usage                                               │
│  4. Detect anti-patterns                                                     │
│  5. Generate compliance report                                               │
│                                                                              │
│  MODE: suggest                                                               │
│  ─────────────                                                               │
│  1. Parse feature requirements                                               │
│  2. Match to pattern categories                                              │
│  3. Identify core components to use                                          │
│  4. Generate recommendations with examples                                   │
│                                                                              │
│  MODE: review                                                                │
│  ────────────                                                                │
│  1. Get code changes (diff/PR)                                               │
│  2. Analyze pattern compliance                                               │
│  3. Generate review comments                                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

# Instructions

## Mode: Validate

### 1. Detect Tech Stack
```bash
python skills/design-patterns/scripts/detect-stack.py \
  --target "$TARGET" \
  --output /tmp/stack-info.json
```

### 2. Spawn Design Pattern Advisor
```
Task: spawn design-pattern-advisor
Prompt: |
  Validate design patterns in: $TARGET
  Tech stack: [from detection]
  Strict mode: $STRICT

  Check:
  - Pattern compliance (frontend-patterns.md / backend-patterns.md)
  - Core component usage (core-components.md)
  - Anti-patterns (anti-patterns.md)

  Return detailed report with locations and suggestions.
```

### 3. Generate Report
```bash
python skills/design-patterns/scripts/generate-report.py \
  --validation /tmp/validation-result.json \
  --format markdown \
  --output "$OUTPUT_DIR/pattern-report.md"
```

## Mode: Suggest

### 1. Parse Feature Description
```bash
python skills/design-patterns/scripts/parse-feature.py \
  --description "$TARGET" \
  --output /tmp/feature-keywords.json
```

### 2. Spawn Design Pattern Advisor
```
Task: spawn design-pattern-advisor
Prompt: |
  Suggest patterns for feature: $TARGET
  Mode: suggest

  Provide:
  - Recommended patterns with rationale
  - Core components to use
  - Code examples for your stack
  - Common pitfalls to avoid
```

### 3. Output Recommendations

## Mode: Review

### 1. Get Changes
```bash
# For staged changes
python skills/design-patterns/scripts/get-changes.py \
  --staged \
  --output /tmp/changes.json

# For PR
python skills/design-patterns/scripts/get-changes.py \
  --pr $PR_NUMBER \
  --output /tmp/changes.json
```

### 2. Spawn Design Pattern Advisor
```
Task: spawn design-pattern-advisor
Prompt: |
  Review code changes:
  Changes: [from changes.json]
  Mode: review

  For each file changed:
  - Check pattern compliance
  - Identify improvements
  - Suggest specific changes
```

### 3. Format Review Comments

# Report Format

## Validation Report
```json
{
  "skill": "design-patterns",
  "mode": "validate",
  "status": "PASS|WARN|FAIL",
  "target": "src/components/",
  "tech_stack": {
    "frontend": "react",
    "frameworks": ["react-query", "zustand"]
  },
  "score": {
    "pattern_compliance": 85,
    "core_component_usage": 70,
    "anti_pattern_free": 90,
    "overall": 82
  },
  "patterns": {
    "compliant": [...],
    "violations": [...],
    "missing": [...]
  },
  "core_components": {
    "used_correctly": [...],
    "should_use": [...],
    "deprecated_usage": [...]
  },
  "anti_patterns": [...],
  "recommendations": [...]
}
```

## Suggestion Report
```json
{
  "skill": "design-patterns",
  "mode": "suggest",
  "feature": "file upload with progress",
  "recommendations": [
    {
      "pattern": "File Upload Pattern",
      "rationale": "Handles chunking, progress, and errors",
      "frontend": {
        "components": ["@core/ui/FileUploader"],
        "hooks": ["@core/hooks/useUpload"],
        "example": "..."
      },
      "backend": {
        "services": ["Core.Storage.IFileService"],
        "pattern": "Chunked upload with resume",
        "example": "..."
      },
      "pitfalls": [
        "Don't forget progress callback",
        "Handle network interruptions"
      ]
    }
  ]
}
```

# Scripts Reference

| Script | Purpose |
|--------|---------|
| `detect-stack.py` | Detect frameworks and tech stack |
| `pattern-scanner.py` | Scan code for pattern usage |
| `component-checker.py` | Check core component usage |
| `anti-pattern-detector.py` | Find anti-patterns |
| `parse-feature.py` | Extract keywords from feature description |
| `get-changes.py` | Get git diff or PR changes |
| `generate-report.py` | Format output reports |

# Integration with Feature Planning

The feature-planner skill automatically consults design-patterns:

```
/plan-feature "file upload" "Multi-file upload with drag-drop"
    │
    ├──► Discovery phase
    │
    ├──► design-pattern-advisor (suggest mode)
    │     └──► Recommends: File Upload Pattern
    │         - Use @core/ui/FileUploader
    │         - Use Core.Storage.IFileService
    │
    └──► Plan includes pattern recommendations
```

# Common Pattern Suggestions

| Feature Keywords | Suggested Patterns |
|-----------------|-------------------|
| list, table, grid | DataGrid Pattern, Pagination |
| form, input, validation | Form Pattern, Validation |
| login, auth, session | Auth Flow Pattern |
| upload, file, image | File Upload Pattern |
| search, filter | Search Pattern with debounce |
| modal, dialog, popup | Modal Pattern |
| notification, toast | Toast Pattern |
| real-time, live, websocket | WebSocket Pattern |
| crud, create, update, delete | Repository + CQRS |
