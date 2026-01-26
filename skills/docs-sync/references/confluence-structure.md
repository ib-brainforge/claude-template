# Confluence Space Structure

<!-- TODO: Document your Confluence space organization -->

## Space Overview

**Space Key**: `ARCH` (change to your space key)
**Space Name**: Architecture Documentation

## Page Hierarchy

```
Architecture Documentation (Space Home)
├── Architecture Decision Records
│   ├── ADR-0001: Title
│   ├── ADR-0002: Title
│   └── ...
├── Service Architecture
│   ├── service-name Architecture
│   └── ...
├── System Overview
│   ├── System Diagram
│   ├── Data Flow
│   └── Integration Points
├── Runbooks
│   ├── Deployment Runbook
│   ├── Incident Response
│   └── ...
└── API Documentation
    ├── Public API
    └── Internal APIs
```

## Page Naming Conventions

<!-- TODO: Define your naming conventions -->

| Doc Type | Confluence Title Format | Example |
|----------|------------------------|---------|
| ADR | `ADR-{number}: {title}` | `ADR-0023: Use PostgreSQL for Persistence` |
| Service Arch | `{service-name} Architecture` | `user-service Architecture` |
| Runbook | `{topic} Runbook` | `Deployment Runbook` |

## Labels

<!-- TODO: Define labels you use for organization -->

| Label | Usage |
|-------|-------|
| `adr` | All ADR pages |
| `architecture` | Architecture documentation |
| `runbook` | Operational runbooks |
| `api-docs` | API documentation |
| `auto-synced` | Pages managed by docs-sync |

## Sync Ownership

Pages created/managed by docs-sync are marked with the `auto-synced` label.

**Rules**:
- Do not manually edit `auto-synced` pages in Confluence
- Changes should be made in the source repository
- Run sync to propagate changes to Confluence
