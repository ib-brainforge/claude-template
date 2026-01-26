---
name: core-validator
description: |
  Core/shared library validator.
  Use for: validating shared packages, common utilities,
  SDK libraries, design system components.
tools: [Read, Grep, Glob, Bash]
model: sonnet
---

# Purpose
Validates core/shared libraries for API stability, documentation, versioning, and cross-service compatibility.

# Variables
- `$CORE_PATH (path)`: Path to core library repository
- `$LIBRARY_TYPE (string)`: sdk|utils|design-system|shared-types
- `$CHECK_SCOPE (string)`: all|api|versioning|docs|breaking (default: all)

# Context Requirements
- references/core-patterns/{$LIBRARY_TYPE}.md
- references/rules/library-design.md
- references/rules/versioning.md
- references/rules/breaking-changes.md

# Instructions

1. Identify library type if not provided:
   - Run `scripts/detect-library-type.py $CORE_PATH`

2. Load library-specific patterns from references/core-patterns/

3. Validate API surface:
   - Run `scripts/validate-api-surface.py $CORE_PATH`
   - Check exports are intentional (index files)
   - Check public API is documented
   - Check types are exported properly
   - Check for internal leakage

4. Validate versioning:
   - Run `scripts/validate-versioning.py $CORE_PATH`
   - Check semantic versioning compliance
   - Check CHANGELOG maintained
   - Check version bumps match change types

5. Validate documentation:
   - Run `scripts/validate-docs.py $CORE_PATH`
   - Check README completeness
   - Check API documentation exists
   - Check usage examples provided
   - Check migration guides for major versions

6. Check for breaking changes:
   - Run `scripts/detect-breaking-changes.py $CORE_PATH`
   - Compare current API with last release
   - Flag removed exports
   - Flag changed signatures
   - Flag behavior changes

# Validation Rules
<!-- TODO: Populate with your core library rules -->
- API design: See references/rules/library-design.md
- Versioning: See references/rules/versioning.md
- Documentation: See references/rules/library-docs.md
- Breaking changes: See references/rules/breaking-changes.md
- Dependency management: See references/rules/library-dependencies.md

# Report Format
```json
{
  "agent": "core-validator",
  "library_type": "$LIBRARY_TYPE",
  "status": "PASS|WARN|FAIL",
  "api_surface": {
    "status": "PASS|WARN|FAIL",
    "exports_count": 0,
    "issues": []
  },
  "versioning": {
    "status": "PASS|WARN|FAIL",
    "current_version": "",
    "issues": []
  },
  "documentation": {
    "status": "PASS|WARN|FAIL",
    "coverage": "",
    "issues": []
  },
  "breaking_changes": {
    "detected": false,
    "changes": []
  },
  "summary": ""
}
```
