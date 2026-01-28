# Security Standards

<!--
PROJECT-SPECIFIC: Update with your security requirements.
This is referenced by: plan-validator
-->

## Authentication Requirements

| Requirement | Description | Check |
|-------------|-------------|-------|
| All API endpoints | Must require authentication | `[Authorize]` or equivalent |
| Public endpoints | Must be explicitly marked | `[AllowAnonymous]` |
| Admin endpoints | Must require role | `[Authorize(Roles = "Admin")]` |

## Authorization Patterns

| Pattern | When Required |
|---------|---------------|
| Role-based | Admin functions |
| Resource-based | User data access |
| Policy-based | Complex rules |

## Data Protection

| Data Type | Requirement |
|-----------|-------------|
| PII | Encrypt at rest, mask in logs |
| Credentials | Never store plaintext |
| Tokens | Short expiry, secure storage |

## Input Validation

| Input Type | Validation Required |
|------------|---------------------|
| User input | Sanitize, validate length |
| File uploads | Type check, size limit, scan |
| API parameters | Type validation, bounds check |

## Audit Logging

| Event | Must Log |
|-------|----------|
| Authentication | Success/failure, IP, timestamp |
| Authorization | Access denied events |
| Data changes | Who, what, when |
| Admin actions | All actions |

## Security Anti-Patterns

| Anti-Pattern | Grep Pattern | Severity |
|--------------|--------------|----------|
| Hardcoded secrets | `password\s*=\s*['"]` | error |
| SQL injection | `"SELECT.*"\s*\+` | error |
| Disabled auth | `[AllowAnonymous]` on sensitive | warning |
