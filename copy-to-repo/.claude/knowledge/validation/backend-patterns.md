# Backend Validation Patterns

<!--
PROJECT-SPECIFIC: Update with your backend patterns and grep patterns.
This is referenced by: backend-pattern-validator
-->

## Stack Detection

| Stack | Detection File | File Extension |
|-------|----------------|----------------|
| .NET | `*.csproj` or `*.sln` | `.cs` |
| Go | `go.mod` | `.go` |
| Java/Maven | `pom.xml` | `.java` |
| Java/Gradle | `build.gradle` | `.java` |
| Node.js | `package.json` | `.ts`, `.js` |
| Python | `requirements.txt` or `pyproject.toml` | `.py` |

## API Style Detection

| Style | Grep Pattern | File Pattern |
|-------|--------------|--------------|
| GraphQL | `GraphQL\|graphql` | `**/*` |
| gRPC | `\.proto$` | `**/*.proto` |
| REST | default if no others found | - |

---

## .NET Patterns

### API Patterns

| Check | Grep Pattern | Description |
|-------|--------------|-------------|
| Endpoint attributes | `\[Route\(\|ApiController\]` | Route definitions |
| HTTP methods | `\[HttpGet\|HttpPost\|HttpPut\|HttpDelete\]` | HTTP verb attributes |
| API versioning | `ApiVersion\|/api/v` | Version support |
| Response type | `IActionResult\|ActionResult<` | Return types |

### Database Patterns

| Check | Grep Pattern | Description |
|-------|--------------|-------------|
| Repository pattern | `IRepository\|Repository<` | Repository interfaces |
| DbContext | `DbContext\|DbSet<` | EF Core context |
| Eager loading | `Include\(\|ThenInclude\(` | N+1 prevention |
| Migrations | `Migrations/` (path) | Migration files |

### Security Patterns

| Check | Grep Pattern | Description |
|-------|--------------|-------------|
| Authorization | `\[Authorize\]\|\[AllowAnonymous\]` | Auth attributes |
| Authentication | `UseAuthentication\|AddAuthentication` | Auth setup |
| Input validation | `DataAnnotations\|FluentValidation` | Validation libs |

### Logging Patterns

| Check | Grep Pattern | Description |
|-------|--------------|-------------|
| Logger injection | `ILogger<\|ILoggerFactory` | Structured logging |
| Log methods | `_logger\.Log\|\.LogInformation\|\.LogError` | Log calls |

---

## Java/Spring Patterns

### API Patterns

| Check | Grep Pattern | Description |
|-------|--------------|-------------|
| Endpoint annotations | `@RestController\|@Controller` | Controller classes |
| HTTP methods | `@GetMapping\|@PostMapping\|@PutMapping\|@DeleteMapping` | Method mappings |
| Request body | `@RequestBody` | Request binding |
| Response entity | `ResponseEntity<` | Response wrapping |

### Database Patterns

| Check | Grep Pattern | Description |
|-------|--------------|-------------|
| Repository | `@Repository\|JpaRepository` | Spring Data repos |
| Entity | `@Entity` | JPA entities |
| Fetch strategy | `fetch\s*=\s*FetchType` | Eager/Lazy config |

### Security Patterns

| Check | Grep Pattern | Description |
|-------|--------------|-------------|
| Security annotations | `@PreAuthorize\|@Secured\|@RolesAllowed` | Method security |
| Input validation | `@Valid\|@Validated` | Bean validation |

### Logging Patterns

| Check | Grep Pattern | Description |
|-------|--------------|-------------|
| SLF4J | `LoggerFactory\.getLogger\|@Slf4j` | Logger setup |
| Log4j | `Logger\.getLogger` | Log4j usage |

---

## Node.js/Express Patterns

### API Patterns

| Check | Grep Pattern | Description |
|-------|--------------|-------------|
| Route definitions | `app\.get\|app\.post\|app\.put\|app\.delete\|router\.` | Express routes |
| Middleware | `app\.use\(` | Middleware registration |

### Logging Patterns

| Check | Grep Pattern | Description |
|-------|--------------|-------------|
| Winston/Pino | `winston\|pino` | Proper loggers |

---

## Go Patterns

### API Patterns

| Check | Grep Pattern | Description |
|-------|--------------|-------------|
| HTTP handlers | `http\.HandleFunc\|mux\.Handle` | Route registration |
| Gin routes | `gin\.Default\|router\.GET\|router\.POST` | Gin framework |

---

## Anti-Patterns to Detect

### .NET

| Anti-Pattern | Grep Pattern | Severity | Suggestion |
|--------------|--------------|----------|------------|
| Direct DbContext | `DbContext\s+_\|private.*DbContext` | error | Use Repository pattern |
| Throwing exceptions | `throw\s+new\s+\w*Exception` | warning | Use Result pattern |
| Service Locator | `GetService<\|GetRequiredService<` | error | Use constructor injection |
| N+1 query risk | `foreach.*await.*Get\|\.ToList\(\).*foreach` | warning | Use eager loading |
| Missing async | `\.Result\|\.Wait\(\)` | error | Use async/await |
| Empty catch | `catch\s*\{[^}]*\}` | warning | Handle or log errors |

### Java/Spring

| Anti-Pattern | Grep Pattern | Severity | Suggestion |
|--------------|--------------|----------|------------|
| Field injection | `@Autowired\s+private` | warning | Use constructor injection |
| Raw JDBC | `DriverManager\.getConnection` | error | Use JPA/Repository |
| Print statements | `System\.out\.print` | warning | Use SLF4J logger |

### Node.js

| Anti-Pattern | Grep Pattern | Severity | Suggestion |
|--------------|--------------|----------|------------|
| Console in prod | `console\.log\|console\.error` | warning | Use Winston/Pino |
| Callback hell | `function.*function.*function` | warning | Use async/await |
| SQL injection | `\$\{.*\}.*SELECT\|SELECT.*\+` | error | Use parameterized queries |

### Security (All Stacks)

| Anti-Pattern | Grep Pattern | Severity | Description |
|--------------|--------------|----------|-------------|
| Hardcoded secrets | `password\s*=\s*['"].\|apikey\s*=\s*['"].\|secret\s*=\s*['".]` | error | Never hardcode secrets |
| SQL concatenation | `"SELECT.*"\s*\+\|f"SELECT.*\{` | error | SQL injection risk |
| Disabled SSL | `verify\s*=\s*False\|rejectUnauthorized.*false` | error | Security risk |
