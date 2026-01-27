# Validation Configuration

<!--
PROJECT-SPECIFIC: Configure validation behavior.
This is referenced by: validation-orchestrator
-->

## Validation Levels

| Level | Description | Time | Use Case |
|-------|-------------|------|----------|
| quick | Structure only | ~30s | Pre-commit hook |
| standard | + patterns, security | ~2min | PR validation |
| thorough | + cross-service, ADR | ~5min | Release validation |

## Scope Configuration

| Scope | What's Validated |
|-------|------------------|
| all | All discovered services |
| changed | Services with git changes |
| service | Single named service |

## Validators by Level

### Quick

- Structure validation
- Dependency check

### Standard (includes Quick)

- Pattern compliance
- Security basics
- Core package usage

### Thorough (includes Standard)

- Cross-service dependencies
- ADR compliance
- Full security audit
- Performance patterns

## Severity Configuration

| Severity | Blocks PR | Blocks Release |
|----------|-----------|----------------|
| error | Yes | Yes |
| warning | No | Yes |
| info | No | No |

## Excluded Paths

Paths to skip during validation:
```
**/node_modules/**
**/bin/**
**/obj/**
**/.git/**
**/dist/**
**/build/**
```

## Custom Rules

Add project-specific validation rules here:
```yaml
# Example:
# custom_rules:
#   - name: "require-readme"
#     check: "file_exists"
#     path: "README.md"
#     severity: "warning"
```
