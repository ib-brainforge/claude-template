# System Architecture

<!--
PROJECT-SPECIFIC: Update this file for your system.
This is referenced by: master-architect, validation-orchestrator, feature-planner
-->

## Overview

<!-- Describe your system at a high level -->

## Repository Structure

```
$REPOS_ROOT/
├── services/           # Microservices
│   ├── frontend/       # React/Vue/Angular apps
│   └── backend/        # API services
├── core/               # Shared packages
│   ├── frontend/       # NPM packages
│   └── backend/        # NuGet/Maven packages
├── infrastructure/     # IaC, Kubernetes, CI/CD
└── docs/               # Documentation
```

## Services Map

<!-- List your services and their responsibilities -->

| Service | Type | Responsibility | Dependencies |
|---------|------|----------------|--------------|
| user-service | backend | User management | database, auth |
| order-service | backend | Order processing | user-service, payment |
| user-frontend | frontend | User-facing UI | user-service, order-service |

## Communication Patterns

<!-- How services communicate -->

- **Sync**: REST APIs for queries
- **Async**: Message queue for events
- **Real-time**: WebSocket for live updates

## Data Stores

<!-- Databases and their ownership -->

| Store | Type | Owner Service |
|-------|------|---------------|
| users-db | PostgreSQL | user-service |
| orders-db | PostgreSQL | order-service |
| cache | Redis | shared |

## External Integrations

<!-- Third-party services -->

- Payment: Stripe
- Email: SendGrid
- Storage: AWS S3

## Architectural Decisions (ADRs)

<!-- Link to or summarize key decisions -->

1. **ADR-001**: Use CQRS for order processing
2. **ADR-002**: Event sourcing for audit trail
3. **ADR-003**: API Gateway for external access

## References

- Architecture diagrams: `docs/architecture/`
- ADR documents: `docs/adr/`
