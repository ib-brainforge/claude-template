# Backend Design Patterns

<!--
TODO: Customize these patterns for your specific .NET setup.
Update namespaces and examples to match your actual core packages.
-->

## Framework Stack

- **Framework**: .NET 8 / ASP.NET Core
- **ORM**: Entity Framework Core
- **Validation**: FluentValidation
- **Mediator**: MediatR
- **API**: REST / Minimal APIs

## Required Patterns

### 1. Clean Architecture Layers

```
src/
├── Domain/              # Entities, Value Objects, Domain Events
│   └── Entities/
├── Application/         # Use Cases, DTOs, Interfaces
│   ├── Commands/
│   ├── Queries/
│   └── Interfaces/
├── Infrastructure/      # EF Core, External Services
│   ├── Data/
│   └── Services/
└── API/                 # Controllers, Middleware
    └── Controllers/
```

**Rules:**
- Domain has no dependencies
- Application depends only on Domain
- Infrastructure implements Application interfaces
- API depends on all layers

### 2. Repository Pattern

Use Core.Data repositories:

```csharp
// ❌ DON'T: Direct DbContext in controllers
public class UserController : ControllerBase
{
    private readonly AppDbContext _context;

    public async Task<IActionResult> Get(int id)
    {
        var user = await _context.Users.FindAsync(id);
        return Ok(user);
    }
}

// ✅ DO: Repository pattern with Core.Data
public class UserController : ControllerBase
{
    private readonly IRepository<User> _userRepository;

    public async Task<IActionResult> Get(int id)
    {
        var user = await _userRepository.GetByIdAsync(id);
        return user is null ? NotFound() : Ok(user);
    }
}
```

### 3. CQRS Pattern

Separate commands and queries:

```csharp
// ✅ Query
public record GetUserQuery(int Id) : IRequest<UserDto>;

public class GetUserQueryHandler : IRequestHandler<GetUserQuery, UserDto>
{
    private readonly IReadRepository<User> _repository;

    public async Task<UserDto> Handle(GetUserQuery request, CancellationToken ct)
    {
        var user = await _repository.GetByIdAsync(request.Id, ct);
        return user.ToDto();
    }
}

// ✅ Command
public record CreateUserCommand(string Email, string Name) : IRequest<Result<int>>;

public class CreateUserCommandHandler : IRequestHandler<CreateUserCommand, Result<int>>
{
    private readonly IRepository<User> _repository;
    private readonly IUnitOfWork _unitOfWork;

    public async Task<Result<int>> Handle(CreateUserCommand request, CancellationToken ct)
    {
        var user = new User(request.Email, request.Name);
        await _repository.AddAsync(user, ct);
        await _unitOfWork.SaveChangesAsync(ct);
        return Result.Success(user.Id);
    }
}
```

### 4. Result Pattern

Never throw for expected failures:

```csharp
// ❌ DON'T: Throw exceptions for business logic
public User GetUser(int id)
{
    var user = _repository.GetById(id);
    if (user == null)
        throw new NotFoundException("User not found");
    return user;
}

// ✅ DO: Use Result pattern from Core.Common
public async Task<Result<UserDto>> GetUser(int id)
{
    var user = await _repository.GetByIdAsync(id);

    if (user is null)
        return Result.Failure<UserDto>(UserErrors.NotFound(id));

    return Result.Success(user.ToDto());
}

// Usage in controller
[HttpGet("{id}")]
public async Task<IActionResult> Get(int id)
{
    var result = await _mediator.Send(new GetUserQuery(id));

    return result.IsSuccess
        ? Ok(result.Value)
        : result.ToProblemDetails();
}
```

### 5. Specification Pattern

Complex queries as specifications:

```csharp
// ✅ Reusable specification
public class ActiveUsersSpec : Specification<User>
{
    public ActiveUsersSpec()
    {
        Query
            .Where(u => u.IsActive)
            .OrderBy(u => u.Name);
    }
}

public class UsersByRoleSpec : Specification<User>
{
    public UsersByRoleSpec(string role)
    {
        Query
            .Where(u => u.Role == role)
            .Include(u => u.Permissions);
    }
}

// Usage
var activeUsers = await _repository.ListAsync(new ActiveUsersSpec());
var admins = await _repository.ListAsync(new UsersByRoleSpec("Admin"));
```

### 6. Domain Events Pattern

Decouple side effects:

```csharp
// ✅ Domain event
public record UserCreatedEvent(int UserId, string Email) : IDomainEvent;

// ✅ Entity raises events
public class User : Entity
{
    public User(string email, string name)
    {
        Email = email;
        Name = name;
        AddDomainEvent(new UserCreatedEvent(Id, Email));
    }
}

// ✅ Handler for side effects
public class SendWelcomeEmailHandler : IDomainEventHandler<UserCreatedEvent>
{
    private readonly IEmailService _emailService;

    public async Task Handle(UserCreatedEvent @event, CancellationToken ct)
    {
        await _emailService.SendWelcomeEmail(@event.Email);
    }
}
```

### 7. Options Pattern

Configuration as strongly-typed options:

```csharp
// ❌ DON'T: Magic strings
var apiKey = Configuration["ExternalApi:ApiKey"];

// ✅ DO: Options pattern
public class ExternalApiOptions
{
    public const string SectionName = "ExternalApi";

    public string ApiKey { get; init; } = string.Empty;
    public string BaseUrl { get; init; } = string.Empty;
    public int TimeoutSeconds { get; init; } = 30;
}

// Registration
services.Configure<ExternalApiOptions>(
    configuration.GetSection(ExternalApiOptions.SectionName));

// Usage
public class ExternalApiService
{
    private readonly ExternalApiOptions _options;

    public ExternalApiService(IOptions<ExternalApiOptions> options)
    {
        _options = options.Value;
    }
}
```

### 8. Validation Pattern

Use FluentValidation:

```csharp
// ✅ Validator class
public class CreateUserCommandValidator : AbstractValidator<CreateUserCommand>
{
    public CreateUserCommandValidator(IUserRepository userRepository)
    {
        RuleFor(x => x.Email)
            .NotEmpty()
            .EmailAddress()
            .MustAsync(async (email, ct) =>
                !await userRepository.ExistsAsync(email, ct))
            .WithMessage("Email already exists");

        RuleFor(x => x.Name)
            .NotEmpty()
            .MaximumLength(100);
    }
}

// Auto-registered via MediatR pipeline
```

## Core Package Components (Must Use)

| Component | Use Instead Of |
|-----------|---------------|
| `Core.Data.Repository<T>` | Direct DbContext access |
| `Core.Data.UnitOfWork` | Manual transaction management |
| `Core.Common.Result<T>` | Throwing exceptions |
| `Core.Validation` | Manual validation |
| `Core.Events.IDomainEvent` | Direct service calls |
| `Core.Security.ICurrentUser` | HttpContext.User access |
| `Core.Logging.IAppLogger` | Direct ILogger |

## API Controller Pattern

```csharp
// ✅ Standard controller structure
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    private readonly IMediator _mediator;

    public UsersController(IMediator mediator) => _mediator = mediator;

    [HttpGet]
    public async Task<IActionResult> GetAll([FromQuery] GetUsersQuery query)
        => Ok(await _mediator.Send(query));

    [HttpGet("{id:int}")]
    public async Task<IActionResult> Get(int id)
        => (await _mediator.Send(new GetUserQuery(id))).ToActionResult();

    [HttpPost]
    public async Task<IActionResult> Create(CreateUserCommand command)
        => (await _mediator.Send(command)).ToCreatedAtAction(nameof(Get));

    [HttpPut("{id:int}")]
    public async Task<IActionResult> Update(int id, UpdateUserCommand command)
        => (await _mediator.Send(command with { Id = id })).ToActionResult();

    [HttpDelete("{id:int}")]
    public async Task<IActionResult> Delete(int id)
        => (await _mediator.Send(new DeleteUserCommand(id))).ToNoContent();
}
```

## File Naming Conventions

```
Application/
├── Users/
│   ├── Commands/
│   │   ├── CreateUser/
│   │   │   ├── CreateUserCommand.cs
│   │   │   ├── CreateUserCommandHandler.cs
│   │   │   └── CreateUserCommandValidator.cs
│   │   └── UpdateUser/
│   ├── Queries/
│   │   ├── GetUser/
│   │   └── GetUsers/
│   └── UserDto.cs

Domain/
├── Entities/
│   └── User.cs          # Entity
├── ValueObjects/
│   └── Email.cs         # Value object
└── Events/
    └── UserCreatedEvent.cs
```
