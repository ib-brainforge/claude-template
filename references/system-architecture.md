# System Architecture Overview

<!--
TODO: Document your system architecture here.
This file is loaded by the master-architect agent for system-wide validation.
Keep it focused on architectural decisions, not implementation details.
-->

## System Context

<!-- TODO: High-level description of your system -->

**System Name**: [Your System Name]
**Purpose**: [What the system does]
**Users**: [Who uses it]

## Service Map

<!-- TODO: List your services and their responsibilities -->

| Service | Type | Responsibility | Depends On |
|---------|------|---------------|------------|
| user-api | backend | User management | auth-service, postgres |
| auth-service | backend | Authentication | redis, postgres |
| frontend-app | frontend | Web UI | user-api, auth-service |
| ... | ... | ... | ... |

## Communication Patterns

<!-- TODO: Define how services communicate -->

### Synchronous
- REST APIs for client-to-service
- gRPC for service-to-service (optional)

### Asynchronous
- Event bus (Kafka/RabbitMQ/etc.) for:
  - Domain events
  - Saga orchestration
  - Notifications

## Data Ownership

<!-- TODO: Define which service owns which data -->

| Domain | Owner Service | Storage |
|--------|--------------|---------|
| Users | user-api | PostgreSQL |
| Sessions | auth-service | Redis |
| ... | ... | ... |

## Cross-Cutting Concerns

<!-- TODO: Document how these are handled -->

### Authentication
- JWT tokens issued by auth-service
- Token validation middleware in each service

### Logging
- Structured JSON logs
- Correlation IDs for request tracing

### Monitoring
- Metrics exported to Prometheus
- Distributed tracing via OpenTelemetry

## Deployment Topology

<!-- TODO: Document your deployment structure -->

```
Production:
├── Region A (Primary)
│   ├── Kubernetes Cluster
│   │   ├── user-api (3 replicas)
│   │   ├── auth-service (3 replicas)
│   │   └── frontend-app (2 replicas)
│   └── Databases
│       ├── PostgreSQL (Primary)
│       └── Redis Cluster
└── Region B (DR)
    └── ...
```

## Key Constraints

<!-- TODO: List architectural constraints -->

1. Services must be stateless (state in databases/cache)
2. All inter-service communication must be authenticated
3. No direct database access across service boundaries
4. All changes require ADR if they affect architecture
