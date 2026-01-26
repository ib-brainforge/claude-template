# Anti-Patterns to Detect and Avoid

<!--
This file defines anti-patterns that the design-pattern-advisor should flag.
Each anti-pattern includes detection rules and remediation suggestions.
-->

## Frontend Anti-Patterns

### 1. Prop Drilling

**Detection:** Props passed through 3+ component levels without being used.

```tsx
// ❌ Anti-pattern
function App() {
  const user = useUser();
  return <Layout user={user} />;
}
function Layout({ user }) {
  return <Sidebar user={user} />;
}
function Sidebar({ user }) {
  return <UserMenu user={user} />;
}
function UserMenu({ user }) {
  return <span>{user.name}</span>;  // Finally used here
}

// ✅ Solution: Context
function App() {
  return (
    <UserProvider>
      <Layout />
    </UserProvider>
  );
}
function UserMenu() {
  const { user } = useUser();
  return <span>{user.name}</span>;
}
```

### 2. God Component

**Detection:** Component with >500 lines or >10 props.

```tsx
// ❌ Anti-pattern
function Dashboard({
  users, orders, products, analytics,
  settings, notifications, filters,
  onUserClick, onOrderClick, onFilterChange,
  // ... 15 more props
}) {
  // 600 lines of mixed logic
}

// ✅ Solution: Composition
function Dashboard() {
  return (
    <DashboardLayout>
      <UserSection />
      <OrderSection />
      <ProductSection />
      <AnalyticsSection />
    </DashboardLayout>
  );
}
```

### 3. Direct API Calls in Components

**Detection:** fetch(), axios, or XMLHttpRequest in component files.

```tsx
// ❌ Anti-pattern
function UserList() {
  useEffect(() => {
    fetch('/api/users')
      .then(r => r.json())
      .then(setUsers);
  }, []);
}

// ✅ Solution: Use API client and hooks
function UserList() {
  const { data: users } = useUsers();
}
```

### 4. Inline Styles

**Detection:** style={{ }} props with >3 properties (except dynamic values).

```tsx
// ❌ Anti-pattern
<div style={{
  display: 'flex',
  justifyContent: 'center',
  padding: '20px',
  backgroundColor: '#f0f0f0',
  borderRadius: '8px'
}}>

// ✅ Solution: Tailwind or CSS modules
<div className="flex justify-center p-5 bg-gray-100 rounded-lg">
```

### 5. useEffect for Derived State

**Detection:** useEffect that only sets state based on other state/props.

```tsx
// ❌ Anti-pattern
function Component({ items }) {
  const [filteredItems, setFilteredItems] = useState([]);

  useEffect(() => {
    setFilteredItems(items.filter(i => i.active));
  }, [items]);
}

// ✅ Solution: useMemo or compute directly
function Component({ items }) {
  const filteredItems = useMemo(
    () => items.filter(i => i.active),
    [items]
  );
}
```

### 6. Index as Key in Dynamic Lists

**Detection:** `key={index}` in .map() for lists that can be reordered/filtered.

```tsx
// ❌ Anti-pattern
{items.map((item, index) => (
  <Item key={index} item={item} />
))}

// ✅ Solution: Use stable unique identifier
{items.map(item => (
  <Item key={item.id} item={item} />
))}
```

### 7. State for URL-based Data

**Detection:** useState for filters, pagination, or tabs that should persist in URL.

```tsx
// ❌ Anti-pattern
const [page, setPage] = useState(1);
const [filter, setFilter] = useState('all');

// ✅ Solution: URL state
const [searchParams, setSearchParams] = useSearchParams();
const page = Number(searchParams.get('page')) || 1;
const filter = searchParams.get('filter') || 'all';
```

---

## Backend Anti-Patterns

### 1. Anemic Domain Model

**Detection:** Entities with only properties, no methods. All logic in services.

```csharp
// ❌ Anti-pattern
public class Order
{
    public int Id { get; set; }
    public decimal Total { get; set; }
    public OrderStatus Status { get; set; }
}

public class OrderService
{
    public void Cancel(Order order)
    {
        if (order.Status == OrderStatus.Shipped)
            throw new Exception("Cannot cancel shipped order");
        order.Status = OrderStatus.Cancelled;
    }
}

// ✅ Solution: Rich domain model
public class Order : AggregateRoot
{
    public decimal Total { get; private set; }
    public OrderStatus Status { get; private set; }

    public Result Cancel()
    {
        if (Status == OrderStatus.Shipped)
            return Result.Failure(OrderErrors.CannotCancelShipped);

        Status = OrderStatus.Cancelled;
        AddDomainEvent(new OrderCancelledEvent(Id));
        return Result.Success();
    }
}
```

### 2. Service Locator

**Detection:** IServiceProvider.GetService() or Activator.CreateInstance() in application code.

```csharp
// ❌ Anti-pattern
public class OrderService
{
    private readonly IServiceProvider _serviceProvider;

    public void ProcessOrder(Order order)
    {
        var emailService = _serviceProvider.GetService<IEmailService>();
        emailService.Send(...);
    }
}

// ✅ Solution: Constructor injection
public class OrderService
{
    private readonly IEmailService _emailService;

    public OrderService(IEmailService emailService)
    {
        _emailService = emailService;
    }
}
```

### 3. N+1 Queries

**Detection:** Database calls inside loops.

```csharp
// ❌ Anti-pattern
var orders = await _orderRepository.GetAllAsync();
foreach (var order in orders)
{
    order.Customer = await _customerRepository.GetByIdAsync(order.CustomerId);
}

// ✅ Solution: Eager loading or batch fetch
var orders = await _orderRepository
    .GetBySpecAsync(new OrdersWithCustomersSpec());

// Or batch fetch
var customerIds = orders.Select(o => o.CustomerId).Distinct();
var customers = await _customerRepository
    .GetBySpecAsync(new CustomersByIdsSpec(customerIds));
```

### 4. Throwing Exceptions for Business Logic

**Detection:** throw new Exception/throw new ApplicationException for expected conditions.

```csharp
// ❌ Anti-pattern
public User GetUser(int id)
{
    var user = _repository.GetById(id);
    if (user == null)
        throw new NotFoundException($"User {id} not found");
    return user;
}

// ✅ Solution: Result pattern
public async Task<Result<User>> GetUser(int id)
{
    var user = await _repository.GetByIdAsync(id);
    return user is null
        ? Result.Failure<User>(UserErrors.NotFound(id))
        : Result.Success(user);
}
```

### 5. Magic Strings

**Detection:** Hardcoded strings for configuration, error messages, or keys.

```csharp
// ❌ Anti-pattern
var connection = Configuration["ConnectionStrings:DefaultConnection"];
var apiKey = Configuration["ExternalApi:Key"];

if (user.Role == "Admin") { ... }

// ✅ Solution: Options pattern + constants
public static class Roles
{
    public const string Admin = "Admin";
    public const string User = "User";
}

services.Configure<DatabaseOptions>(Configuration.GetSection("Database"));
services.Configure<ExternalApiOptions>(Configuration.GetSection("ExternalApi"));
```

### 6. Direct DbContext in Controllers

**Detection:** DbContext injected/used directly in controllers.

```csharp
// ❌ Anti-pattern
public class UsersController : ControllerBase
{
    private readonly AppDbContext _context;

    public async Task<IActionResult> Get()
    {
        return Ok(await _context.Users.ToListAsync());
    }
}

// ✅ Solution: Repository + MediatR
public class UsersController : ControllerBase
{
    private readonly IMediator _mediator;

    public async Task<IActionResult> Get([FromQuery] GetUsersQuery query)
    {
        return Ok(await _mediator.Send(query));
    }
}
```

### 7. Synchronous I/O

**Detection:** Non-async database or HTTP calls.

```csharp
// ❌ Anti-pattern
public User GetUser(int id)
{
    return _context.Users.Find(id);  // Sync call
}

// ✅ Solution: Async everywhere
public async Task<User?> GetUserAsync(int id, CancellationToken ct = default)
{
    return await _context.Users.FindAsync(new object[] { id }, ct);
}
```

### 8. Missing Cancellation Token

**Detection:** Async methods without CancellationToken parameter.

```csharp
// ❌ Anti-pattern
public async Task<User> GetUserAsync(int id)
{
    return await _repository.GetByIdAsync(id);
}

// ✅ Solution: Always accept and pass CancellationToken
public async Task<User> GetUserAsync(int id, CancellationToken ct = default)
{
    return await _repository.GetByIdAsync(id, ct);
}
```

---

## Detection Rules Summary

| Anti-Pattern | Severity | Detection Pattern |
|--------------|----------|-------------------|
| Prop Drilling | Warning | Props passed >3 levels |
| God Component | Error | >500 lines or >10 props |
| Direct API Calls | Error | fetch/axios in components |
| Inline Styles | Warning | style={{ }} with >3 props |
| useEffect Derived State | Warning | useEffect only setting state |
| Index as Key | Warning | key={index} in map |
| Anemic Domain | Warning | Entities with only getters/setters |
| Service Locator | Error | IServiceProvider.GetService |
| N+1 Queries | Error | DB call inside loop |
| Exception Business Logic | Warning | throw for expected conditions |
| Magic Strings | Warning | Hardcoded config values |
| Direct DbContext | Error | DbContext in controllers |
| Synchronous I/O | Error | Non-async DB/HTTP calls |
| Missing CancellationToken | Warning | Async without CT parameter |
