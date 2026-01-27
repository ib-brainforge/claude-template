# Repository Configuration

<!--
PROJECT-SPECIFIC: Configure repo-specific settings.
This is referenced by: commit-manager
-->

## Repository Types

| Type | Path Pattern | Commit Prefix |
|------|--------------|---------------|
| Frontend app | `apps/web-*` | `web:` |
| Backend service | `services/*` | `svc:` |
| Core library | `packages/*` | `core:` |
| Infrastructure | `infra/*` | `infra:` |

## Branch Naming

| Branch Type | Pattern | Example |
|-------------|---------|---------|
| Feature | `feature/<ticket>-<desc>` | `feature/PROJ-123-add-auth` |
| Bugfix | `fix/<ticket>-<desc>` | `fix/PROJ-456-login-error` |
| Hotfix | `hotfix/<desc>` | `hotfix/critical-security` |
| Release | `release/<version>` | `release/1.2.0` |

## Protected Branches

| Branch | Rules |
|--------|-------|
| main | Require PR, require reviews |
| develop | Require PR |
| release/* | Require PR, require reviews |

## Repo-Specific Commit Rules

Add repo-specific overrides here:
```yaml
# Example:
# repos:
#   web-app:
#     require_ticket: true
#     ticket_pattern: "PROJ-\\d+"
#   core-utils:
#     require_ticket: false
#     scope_required: true
```
