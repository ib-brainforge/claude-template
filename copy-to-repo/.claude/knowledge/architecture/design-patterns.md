# Design Patterns

<!--
PROJECT-SPECIFIC: Update with your required patterns.
This is referenced by: design-pattern-advisor, feature-planner
NOTE: Grep patterns for validators are in knowledge/validation/
-->

## Frontend Patterns

### Required Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| Container/Presenter | Separating data from UI | `UserListContainer` + `UserList` |
| Custom Hooks | Reusable stateful logic | `useUsers()`, `useDebounce()` |
| Error Boundary | Page-level error handling | Wrap all pages |
| Form Pattern | Any form | React Hook Form + Zod |
| API Client | Any API call | `@core/api-client` |

### Component Structure

```
src/
├── components/       # Shared components
├── hooks/            # Custom hooks
├── pages/            # Route-level components
├── services/         # API layer
└── stores/           # State management
```

### State Management Rules

| State Type | Solution |
|------------|----------|
| Server state | React Query |
| Global client state | Zustand |
| Local component state | useState |
| URL state | useSearchParams |

---

## Backend Patterns

### Required Patterns

| Pattern | When to Use | Core Component |
|---------|-------------|----------------|
| Repository | Data access | `IRepository<T>` |
| CQRS | Commands & Queries | MediatR |
| Result Pattern | Error handling | `Result<T>` |
| Specification | Complex queries | `Specification<T>` |
| Domain Events | Side effects | `IDomainEvent` |
| Options Pattern | Configuration | `IOptions<T>` |

### Clean Architecture Layers

```
Domain/          # Entities, Value Objects (no dependencies)
Application/     # Use Cases, DTOs, Interfaces
Infrastructure/  # EF Core, External Services
API/             # Controllers, Middleware
```

### Folder Structure

```
Application/
├── Users/
│   ├── Commands/
│   │   └── CreateUser/
│   │       ├── CreateUserCommand.cs
│   │       ├── CreateUserCommandHandler.cs
│   │       └── CreateUserCommandValidator.cs
│   ├── Queries/
│   └── UserDto.cs
```

---

## Pattern Selection Guide

| Feature Type | Frontend Pattern | Backend Pattern |
|--------------|------------------|-----------------|
| Data listing | DataGrid + useQuery | Query + Specification |
| Form submission | Form Pattern | Command + Validation |
| Authentication | Auth Context | JWT + ICurrentUser |
| File upload | FileUploader hook | IFileService |
| Real-time | WebSocket hook | SignalR Hub |

## References

- Pattern examples: `docs/patterns/`
- Code templates: `templates/`
