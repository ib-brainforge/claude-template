# Service Boundaries

<!--
PROJECT-SPECIFIC: Update with your service interaction rules.
This is referenced by: master-architect, validation-orchestrator, plan-validator
-->

## Service Ownership

| Service | Owns | Can Access |
|---------|------|------------|
| user-service | users-db, profiles | auth-service (read) |
| order-service | orders-db | user-service (read), payment (external) |
| notification-service | notifications-db | user-service (read) |
| auth-service | sessions, tokens | user-service (read) |

## Communication Rules

### Allowed Patterns

| From | To | Method |
|------|-----|--------|
| Frontend | API Gateway | REST/GraphQL |
| API Gateway | Any Service | REST |
| Service | Service | REST (sync), Events (async) |
| Service | External | Via dedicated integration service |

### Forbidden Patterns

| Pattern | Reason |
|---------|--------|
| Frontend → Service directly | Bypass security |
| Service → Another's DB | Violates ownership |
| Circular sync calls | Deadlock risk |
| Shared mutable state | Race conditions |

## Database Access Rules

```
┌─────────────────────────────────────────────────────────────────┐
│  Service A          Service B          Service C                │
│      │                  │                  │                    │
│      ▼                  ▼                  ▼                    │
│  ┌───────┐          ┌───────┐          ┌───────┐               │
│  │ DB A  │          │ DB B  │          │ DB C  │               │
│  └───────┘          └───────┘          └───────┘               │
│                                                                  │
│  ✅ Service A reads/writes DB A                                 │
│  ✅ Service B reads/writes DB B                                 │
│  ❌ Service A writes to DB B (forbidden)                        │
│  ⚠️ Service A reads DB B via API (allowed with caution)         │
└─────────────────────────────────────────────────────────────────┘
```

## Event-Driven Boundaries

### Events Published

| Service | Events |
|---------|--------|
| user-service | UserCreated, UserUpdated, UserDeleted |
| order-service | OrderCreated, OrderCompleted, OrderCancelled |
| payment-service | PaymentReceived, PaymentFailed |

### Events Consumed

| Service | Listens To |
|---------|------------|
| notification-service | UserCreated, OrderCompleted |
| analytics-service | All events |
| order-service | PaymentReceived, PaymentFailed |

## API Versioning Rules

- All APIs must be versioned: `/api/v1/...`
- Breaking changes require new version
- Support previous version for 6 months
- Deprecation notice 3 months before removal

## Schema Change Rules

1. **Additive changes**: Can deploy anytime
2. **Breaking changes**: Require migration plan
3. **Cross-service impact**: Notify affected teams

## Validation Checks

Used by `plan-validator` to verify plans:

```yaml
checks:
  - name: db_ownership
    rule: "Service only accesses owned database"
    severity: error

  - name: sync_calls
    rule: "No circular synchronous dependencies"
    severity: error

  - name: direct_db_access
    rule: "No cross-service direct DB access"
    severity: error

  - name: api_versioning
    rule: "Breaking API changes bump version"
    severity: warning
```

## References

- Service contracts: `docs/contracts/`
- Event schemas: `docs/events/`
