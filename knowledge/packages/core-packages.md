# Core Packages

<!--
PROJECT-SPECIFIC: Update this file with your actual core package APIs.
This is referenced by: design-pattern-advisor, core-validator, package managers
-->

## Frontend Packages

### @core/ui

UI component library. **Always use instead of custom implementations.**

```tsx
import {
  // Layout
  Box, Flex, Grid, Stack, Container,

  // Forms
  Form, Input, Select, Checkbox, DatePicker,

  // Buttons
  Button, IconButton,

  // Feedback
  Alert, Toast, Spinner, Skeleton,

  // Overlays
  Modal, Drawer, Popover, Tooltip,

  // Data Display
  DataGrid, Table, Card, Badge,

  // Navigation
  Tabs, Breadcrumb, Pagination,

  // Error Handling
  ErrorBoundary,
} from '@core/ui';
```

### @core/hooks

```tsx
import {
  useAuth, useCurrentUser, usePermissions,
  useQuery, useMutation,
  useForm, useFieldArray,
  useDebounce, useLocalStorage,
} from '@core/hooks';
```

### @core/api-client

```tsx
import { userApi, orderApi, productApi } from '@core/api-client';

// Usage
const users = await userApi.getAll();
const user = await userApi.getById(id);
const created = await userApi.create(data);
```

---

## Backend Packages

### Core.Common

```csharp
// Result pattern
Result<T>, Result.Success(), Result.Failure()

// Base types
Entity, AggregateRoot, ValueObject

// Errors
Error, Error.NotFound(), Error.Validation()
```

### Core.Data

```csharp
// Repository
IRepository<T>, IReadRepository<T>

// Unit of Work
IUnitOfWork

// Specification
Specification<T>
```

### Core.Validation

```csharp
// FluentValidation extensions
AbstractValidator<T>
// Custom rules: ValidEmail(), ValidPhone(), etc.
```

### Core.Security

```csharp
ICurrentUser, IJwtService, IPasswordHasher
```

### Core.Events

```csharp
IDomainEvent, IDomainEventHandler<T>
```

---

## Usage Rules

| Need | Use This | Not This |
|------|----------|----------|
| Button | `@core/ui/Button` | `<button>`, custom |
| Modal | `@core/ui/Modal` | Custom modal |
| Data Table | `@core/ui/DataGrid` | Custom table |
| API Call | `@core/api-client` | fetch, axios |
| DB Access | `IRepository<T>` | Direct DbContext |
| Error Handling | `Result<T>` | throw Exception |

## Package Versions

<!-- Current versions of core packages -->

| Package | Version |
|---------|---------|
| @core/ui | 2.x |
| @core/hooks | 1.x |
| @core/api-client | 1.x |
| Core.Common | 3.x |
| Core.Data | 3.x |

## References

- Frontend package docs: `core/frontend/README.md`
- Backend package docs: `core/backend/README.md`
