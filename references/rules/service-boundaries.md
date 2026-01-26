# Service Boundary Rules

<!--
TODO: Define your service boundary rules.
These are validated by the master-architect agent.
-->

## Core Principles

1. **Single Responsibility**: Each service owns one bounded context
2. **Data Ownership**: One service owns each data entity
3. **API Contracts**: Services communicate only via defined APIs

## Boundary Violations to Detect

### Database Access
- ❌ Service A directly accessing Service B's database
- ✅ Service A calling Service B's API

**Detection**: Check for database connection strings pointing to other services' DBs.

### Shared Libraries
- ❌ Business logic shared between services
- ✅ Infrastructure utilities shared (logging, auth middleware)

**Detection**: Check shared library dependencies for domain-specific code.

### Direct Dependencies
- ❌ Service A importing Service B's internal modules
- ✅ Service A depending on Service B's published client/SDK

**Detection**: Check import statements for cross-service internal paths.

## Communication Rules

### Allowed Patterns
<!-- TODO: Define your allowed communication patterns -->

| From | To | Allowed Methods |
|------|----|----|
| Frontend | Backend | REST, WebSocket |
| Backend | Backend | REST, gRPC, Events |
| Backend | Core Lib | Direct import |

### API Versioning
- All APIs must be versioned: `/api/v1/...`
- Breaking changes require new version
- Deprecation notice 2 sprints before removal

## Validation Checks

The validator will check:

1. **No circular dependencies** between services
2. **No shared databases** (each service has its own)
3. **No direct imports** of other services' code
4. **Events are typed** and documented
5. **API contracts** are defined (OpenAPI, GraphQL schema, etc.)
