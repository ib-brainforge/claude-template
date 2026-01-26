# Core Package Components

<!--
TODO: Replace these with your actual core package APIs.
This is your canonical reference for what components exist
and when they should be used.
-->

## Frontend Core Packages

### @core/ui

UI component library. **Always use these instead of custom implementations.**

```tsx
// Available components
import {
  // Layout
  Box, Flex, Grid, Stack, Container, Divider,

  // Typography
  Text, Heading, Link,

  // Forms
  Form, Input, Textarea, Select, Checkbox, Radio,
  Switch, DatePicker, TimePicker, FileUploader,

  // Buttons & Actions
  Button, IconButton, ButtonGroup,

  // Feedback
  Alert, Toast, Progress, Spinner, Skeleton,

  // Overlays
  Modal, Drawer, Popover, Tooltip, Menu,

  // Data Display
  DataGrid, Table, List, Card, Badge, Avatar, Tag,

  // Navigation
  Tabs, Breadcrumb, Pagination, Steps,

  // Error Handling
  ErrorBoundary, ErrorMessage,

} from '@core/ui';
```

**Usage Rules:**
- Never create custom buttons - use `Button` with variants
- Never create custom modals - use `Modal`
- Never create custom tables - use `DataGrid`
- Never create custom form inputs - use `Input`, `Select`, etc.

### @core/hooks

Reusable React hooks.

```tsx
import {
  // Data fetching (built on React Query)
  useQuery, useMutation, useInfiniteQuery,

  // Auth
  useAuth, usePermissions, useCurrentUser,

  // UI State
  useDisclosure, useMediaQuery, useLocalStorage,

  // Forms
  useForm, useFieldArray, useFormContext,

  // Utilities
  useDebounce, useThrottle, usePrevious,
  useClickOutside, useKeyPress, useCopyToClipboard,

  // Async
  useAsync, useInterval, useTimeout,

} from '@core/hooks';
```

### @core/api-client

Type-safe API client. **Never use fetch/axios directly.**

```tsx
import { createApiClient } from '@core/api-client';

// Pre-configured clients for each domain
import {
  userApi,
  orderApi,
  productApi,
  // ... other domain APIs
} from '@core/api-client';

// Usage
const users = await userApi.getAll({ page: 1, limit: 10 });
const user = await userApi.getById(123);
const created = await userApi.create({ name: 'John', email: 'john@example.com' });
const updated = await userApi.update(123, { name: 'John Doe' });
await userApi.delete(123);
```

**Features included:**
- Automatic auth token injection
- Request/response interceptors
- Error transformation
- Retry logic
- Request cancellation

### @core/forms

Form utilities built on React Hook Form.

```tsx
import {
  Form, FormField, FormItem, FormLabel, FormMessage,
  useForm, useFormContext, useFieldArray,
  zodResolver,
} from '@core/forms';

// Standard form setup
const form = useForm({
  resolver: zodResolver(schema),
  defaultValues: { name: '', email: '' },
});
```

### @core/state

Global state management (Zustand stores).

```tsx
import {
  useAuthStore,
  useThemeStore,
  useNotificationStore,
  useFeatureFlagStore,
} from '@core/state';

// Usage
const { user, login, logout } = useAuthStore();
const { theme, setTheme } = useThemeStore();
```

---

## Backend Core Packages

### Core.Common

Base types and utilities.

```csharp
using Core.Common;

// Result pattern
Result<T>              // Success or failure with value
Result                 // Success or failure without value
Result.Success(value)  // Create success
Result.Failure(error)  // Create failure

// Errors
Error                  // Error type with code and message
Error.NotFound(...)    // Factory methods
Error.Validation(...)
Error.Conflict(...)
Error.Unauthorized(...)

// Base types
Entity                 // Base entity with Id
AggregateRoot          // Entity with domain events
ValueObject            // Immutable value object

// Extensions
.ToDto()               // Mapping extensions
.ToProblemDetails()    // Convert Result to HTTP response
```

### Core.Data

Data access layer.

```csharp
using Core.Data;

// Repository
IRepository<T>                    // Full CRUD repository
IReadRepository<T>                // Read-only repository

// Methods
GetByIdAsync(id)
GetBySpecAsync(spec)
ListAsync(spec)
AddAsync(entity)
UpdateAsync(entity)
DeleteAsync(entity)
CountAsync(spec)
AnyAsync(spec)

// Unit of Work
IUnitOfWork
SaveChangesAsync()

// Specification
Specification<T>
Query.Where(...)
Query.Include(...)
Query.OrderBy(...)
Query.Skip(...).Take(...)
```

### Core.Validation

Validation utilities.

```csharp
using Core.Validation;

// FluentValidation base
AbstractValidator<T>

// Common rules
RuleFor(x => x.Email).ValidEmail();
RuleFor(x => x.Phone).ValidPhone();
RuleFor(x => x.Date).ValidDateRange(min, max);

// Async validation
RuleFor(x => x.Email)
    .MustAsync(BeUniqueEmail)
    .WithMessage("Email already exists");
```

### Core.Security

Authentication and authorization.

```csharp
using Core.Security;

// Current user
ICurrentUser
  .Id
  .Email
  .Roles
  .Permissions
  .IsAuthenticated
  .HasPermission(permission)
  .HasRole(role)

// JWT
IJwtService
  .GenerateToken(user)
  .ValidateToken(token)
  .RefreshToken(token)

// Password
IPasswordHasher
  .Hash(password)
  .Verify(password, hash)
```

### Core.Events

Domain events.

```csharp
using Core.Events;

// Event interface
IDomainEvent

// Handler interface
IDomainEventHandler<TEvent>

// Publishing (auto via SaveChanges)
entity.AddDomainEvent(new UserCreatedEvent(...));
```

### Core.Logging

Structured logging.

```csharp
using Core.Logging;

// Logger interface
IAppLogger<T>

// Methods
LogInformation(message, args)
LogWarning(message, args)
LogError(exception, message, args)

// Structured logging
_logger.LogInformation(
    "User {UserId} created order {OrderId}",
    userId, orderId);
```

### Core.Configuration

Configuration utilities.

```csharp
using Core.Configuration;

// Options registration
services.AddOptions<MyOptions>("MySection");

// Validation
services.AddOptionsWithValidation<MyOptions>();

// Reload on change
services.AddOptionsWithReload<MyOptions>();
```

---

## Usage Decision Matrix

### When to Use What

| Need | Frontend | Backend |
|------|----------|---------|
| Button | `@core/ui/Button` | N/A |
| Form | `@core/forms` + `@core/ui` | FluentValidation |
| API Call | `@core/api-client` | N/A |
| Auth Check | `useAuth()` | `ICurrentUser` |
| Data Table | `@core/ui/DataGrid` | N/A |
| Modal/Dialog | `@core/ui/Modal` | N/A |
| Toast/Notification | `@core/ui/Toast` | N/A |
| Data Access | N/A | `IRepository<T>` |
| Transactions | N/A | `IUnitOfWork` |
| Error Handling | ErrorBoundary | `Result<T>` |
| Logging | console (dev only) | `IAppLogger<T>` |
| Config | Environment vars | Options pattern |
