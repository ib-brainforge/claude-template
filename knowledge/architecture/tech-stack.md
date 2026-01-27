# Technology Stack

<!--
PROJECT-SPECIFIC: Update this file for your tech stack.
This is referenced by: design-pattern-advisor, validators, feature-planner
-->

## Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.x | UI framework |
| TypeScript | 5.x | Type safety |
| Tailwind CSS | 3.x | Styling |
| React Query | 5.x | Server state |
| Zustand | 4.x | Client state |
| React Hook Form | 7.x | Forms |
| Vite | 5.x | Build tool |

## Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| .NET | 8.0 | Runtime |
| ASP.NET Core | 8.0 | Web framework |
| Entity Framework Core | 8.0 | ORM |
| MediatR | 12.x | CQRS/Mediator |
| FluentValidation | 11.x | Validation |
| Serilog | 3.x | Logging |

## Infrastructure

| Technology | Purpose |
|------------|---------|
| Docker | Containerization |
| Kubernetes | Orchestration |
| GitHub Actions | CI/CD |
| Terraform | IaC |
| PostgreSQL | Primary database |
| Redis | Caching |
| RabbitMQ | Message queue |

## Development Tools

| Tool | Purpose |
|------|---------|
| ESLint | JS/TS linting |
| Prettier | Code formatting |
| Husky | Git hooks |
| Jest | Frontend testing |
| xUnit | Backend testing |

## Version Compatibility

<!-- Important version constraints -->

- Node.js: 20.x LTS
- .NET SDK: 8.0.x
- npm: 10.x
- Docker: 24.x

## Conventions

### File Naming

- **Frontend**: PascalCase for components (`UserCard.tsx`), camelCase for utilities (`formatDate.ts`)
- **Backend**: PascalCase for classes, folders follow feature structure

### Code Style

- Frontend: Prettier + ESLint with Airbnb config
- Backend: .editorconfig + Roslyn analyzers

## References

- Frontend style guide: `docs/frontend-guide.md`
- Backend style guide: `docs/backend-guide.md`
