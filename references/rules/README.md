# Validation Rules

This directory contains architectural rules used by validation agents.

## Structure

Each rule file defines:
1. The principle being enforced
2. What violations look like
3. How to detect violations
4. Specific checks the validator performs

## Rule Files

<!-- TODO: Create rule files for your organization -->

| File | Used By | Description |
|------|---------|-------------|
| service-boundaries.md | master-architect | Service boundary rules |
| communication-patterns.md | master-architect | Inter-service communication |
| dependencies.md | service-validator | Dependency management |
| service-structure.md | service-validator | Directory structure |
| component-patterns.md | frontend-pattern-validator | Frontend component rules |
| state-management.md | frontend-pattern-validator | State management rules |
| api-design.md | backend-pattern-validator | API design standards |
| database-patterns.md | backend-pattern-validator | Database access patterns |
| security-patterns.md | backend-pattern-validator | Security requirements |

## Adding New Rules

1. Create `rules/{rule-name}.md`
2. Follow the standard structure:
   ```markdown
   # Rule Name

   ## Core Principles
   <!-- What this rule enforces -->

   ## Violations to Detect
   <!-- Examples of violations -->

   ## Validation Checks
   <!-- Specific checks the validator performs -->
   ```
3. Reference from appropriate agent's "Validation Rules" section

## Rule Severity

Rules should indicate severity:
- **ERROR**: Must fix, blocks deployment
- **WARNING**: Should fix, doesn't block
- **INFO**: Suggestion for improvement
