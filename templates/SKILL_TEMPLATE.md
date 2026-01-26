# Skill Template - Unified Format

## Format Specification

```markdown
---
name: skill-name
description: |
  What this skill provides.
  Trigger conditions: when to load this skill.
---

# Purpose
<!-- 1-2 sentences: What capability this skill adds -->

# Resources
<!-- What's bundled with this skill -->
- scripts/: Executable utilities
- references/: Documentation to load as needed
- assets/: Templates, configs to copy/use

# Usage
<!-- How to use this skill's resources -->

## Scripts
- `scripts/do-thing.py`: Description, usage example

## References
- `references/guide.md`: When to read this

# Workflow
<!-- If skill has a multi-step process -->
1. Step one
2. Step two

# Output
<!-- What this skill produces -->
```

## Structure

```
skill-name/
├── SKILL.md           # This file - instructions
├── scripts/           # Python/Bash utilities
│   └── utility.py
├── references/        # Documentation loaded as needed
│   └── detailed-guide.md
└── assets/            # Templates, configs
    └── template.json
```

## Design Principles

### Progressive Disclosure
- SKILL.md: Core workflow (<500 lines)
- references/: Detailed docs (loaded when needed)
- scripts/: Executed without reading into context

### Token Efficiency
- Scripts run without loading into context
- References loaded only when explicitly needed
- Assets copied/used, never loaded

### Determinism
- Prefer scripts over inline instructions for:
  - File parsing
  - Validation checks
  - Format conversions
  - API calls
