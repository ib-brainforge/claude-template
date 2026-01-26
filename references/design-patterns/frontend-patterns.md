# Frontend Design Patterns

<!--
TODO: Customize these patterns for your specific React setup.
Update examples to match your actual core package APIs.
-->

## Framework Stack

- **UI Framework**: React 18+
- **State Management**: Zustand / React Query
- **Styling**: Tailwind CSS / CSS Modules
- **Forms**: React Hook Form
- **Routing**: React Router v6

## Required Patterns

### 1. Component Structure Pattern

```
src/
├── components/          # Shared components
│   ├── ui/             # Pure UI components (from @core/ui)
│   └── features/       # Feature-specific components
├── hooks/              # Custom hooks
├── pages/              # Page components (route-level)
├── services/           # API calls (use @core/api-client)
└── stores/             # State management
```

**Rules:**
- Pages import from components, never vice versa
- Components don't call APIs directly
- Hooks encapsulate reusable logic

### 2. Container/Presenter Pattern

Separate data fetching from presentation:

```tsx
// ❌ DON'T: Mixed concerns
function UserList() {
  const [users, setUsers] = useState([]);
  useEffect(() => {
    fetch('/api/users').then(r => r.json()).then(setUsers);
  }, []);
  return <ul>{users.map(u => <li>{u.name}</li>)}</ul>;
}

// ✅ DO: Separated concerns
function UserListContainer() {
  const { data: users } = useUsers(); // Hook handles fetching
  return <UserListPresenter users={users} />;
}

function UserListPresenter({ users }: { users: User[] }) {
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

### 3. Custom Hooks Pattern

Encapsulate stateful logic in hooks:

```tsx
// ✅ Good: Reusable hook
function useUsers(filters?: UserFilters) {
  return useQuery({
    queryKey: ['users', filters],
    queryFn: () => userApi.getAll(filters),
  });
}

// ✅ Good: Hook for local state + effects
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
```

### 4. Form Pattern

Use React Hook Form with Zod validation:

```tsx
// ✅ Standard form pattern
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Form, Input, Button } from '@core/ui';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

function LoginForm({ onSubmit }: Props) {
  const form = useForm({
    resolver: zodResolver(schema),
  });

  return (
    <Form form={form} onSubmit={form.handleSubmit(onSubmit)}>
      <Input name="email" label="Email" />
      <Input name="password" label="Password" type="password" />
      <Button type="submit">Login</Button>
    </Form>
  );
}
```

### 5. Error Boundary Pattern

Wrap page-level components:

```tsx
// ✅ Every page should have error boundary
import { ErrorBoundary } from '@core/ui';

function DashboardPage() {
  return (
    <ErrorBoundary fallback={<DashboardError />}>
      <DashboardContent />
    </ErrorBoundary>
  );
}
```

### 6. Loading State Pattern

Consistent loading states with Suspense:

```tsx
// ✅ Page with loading state
function UsersPage() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <UsersContent />
    </Suspense>
  );
}

// ✅ Component with loading state
function UserCard({ userId }: Props) {
  const { data, isLoading } = useUser(userId);

  if (isLoading) return <UserCardSkeleton />;
  return <UserCardContent user={data} />;
}
```

### 7. Context Pattern

For cross-cutting concerns only:

```tsx
// ✅ Good use: Auth context (used everywhere)
const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: Props) {
  const auth = useAuthState();
  return (
    <AuthContext.Provider value={auth}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be within AuthProvider');
  return context;
}
```

### 8. API Client Pattern

Always use core API client:

```tsx
// ❌ DON'T: Direct fetch
const response = await fetch('/api/users');

// ❌ DON'T: Axios instance in component
const response = await axios.get('/api/users');

// ✅ DO: Core API client
import { userApi } from '@core/api-client';

const users = await userApi.getAll();
const user = await userApi.getById(id);
const created = await userApi.create(data);
```

## Core UI Components (Must Use)

| Component | Use Instead Of |
|-----------|---------------|
| `@core/ui/Button` | Native button, custom buttons |
| `@core/ui/Input` | Native input |
| `@core/ui/Modal` | Custom modal implementations |
| `@core/ui/DataGrid` | Custom table implementations |
| `@core/ui/Form` | Native form |
| `@core/ui/Toast` | Custom notifications |
| `@core/ui/Dropdown` | Custom select/dropdown |
| `@core/ui/Tabs` | Custom tab implementations |

## State Management Rules

```
┌─────────────────────────────────────────────────────────────────┐
│                    STATE MANAGEMENT DECISION                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Server State (async data from API)                              │
│  └──► Use React Query (@tanstack/react-query)                    │
│                                                                  │
│  Global Client State (user, theme, feature flags)                │
│  └──► Use Zustand                                                │
│                                                                  │
│  Local Component State (form, UI toggles)                        │
│  └──► Use useState/useReducer                                    │
│                                                                  │
│  URL State (filters, pagination, tabs)                           │
│  └──► Use URL search params (useSearchParams)                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## File Naming Conventions

```
components/
├── UserCard.tsx           # PascalCase for components
├── UserCard.test.tsx      # Test files alongside
├── UserCard.module.css    # CSS modules
├── index.ts               # Barrel exports

hooks/
├── useUsers.ts            # camelCase with 'use' prefix
├── useDebounce.ts

stores/
├── userStore.ts           # camelCase with 'Store' suffix
├── authStore.ts
```
