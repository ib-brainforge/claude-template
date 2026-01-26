# Package Configuration

<!--
TODO: Configure your core packages here.
This file defines which packages are tracked for CI/CD monitoring
and version propagation.
-->

## Core Packages

### NPM Packages (React/TypeScript)

```json
{
  "packages": [
    {
      "name": "@your-org/core-react",
      "description": "Core React components and hooks",
      "type": "npm",
      "repo": "your-org/core-react",
      "registry": "npm",
      "workflow": "publish.yml",
      "dependent_repos": "auto"
    },
    {
      "name": "@your-org/ui-components",
      "description": "Design system components",
      "type": "npm",
      "repo": "your-org/ui-components",
      "registry": "npm",
      "workflow": "publish.yml",
      "dependent_repos": "auto"
    },
    {
      "name": "@your-org/shared-utils",
      "description": "Shared TypeScript utilities",
      "type": "npm",
      "repo": "your-org/shared-utils",
      "registry": "npm",
      "workflow": "publish.yml",
      "dependent_repos": "auto"
    }
  ]
}
```

### NuGet Packages (C#/.NET)

```json
{
  "packages": [
    {
      "name": "YourOrg.Core",
      "description": "Core .NET libraries",
      "type": "nuget",
      "repo": "your-org/dotnet-core",
      "registry": "nuget",
      "workflow": "publish.yml",
      "dependent_repos": "auto"
    },
    {
      "name": "YourOrg.Data",
      "description": "Data access layer",
      "type": "nuget",
      "repo": "your-org/dotnet-data",
      "registry": "nuget",
      "workflow": "publish.yml",
      "dependent_repos": "auto"
    },
    {
      "name": "YourOrg.Common",
      "description": "Common utilities and extensions",
      "type": "nuget",
      "repo": "your-org/dotnet-common",
      "registry": "nuget",
      "workflow": "publish.yml",
      "dependent_repos": "auto"
    }
  ]
}
```

## Package Detection

The package-version-manager identifies core packages by:

1. **Repository location**: Repos in `core/` directory
2. **Package prefix**: NPM scope `@your-org/`, NuGet prefix `YourOrg.`
3. **Publish workflow**: Has `.github/workflows/publish.yml`

## Dependency Scanning

### NPM
Scans for packages in:
- `dependencies`
- `devDependencies`
- `peerDependencies`

In files:
- `package.json`

### NuGet
Scans for packages in:
- `<PackageReference>` elements

In files:
- `*.csproj`
- `Directory.Packages.props`
- `packages.config` (legacy)

## Version Update Strategy

### NPM
- Preserves version prefix (`^`, `~`, `>=`)
- Default: `^` for dependencies, exact for dev
- Runs `npm install` after update

### NuGet
- Uses exact versions by default
- Runs `dotnet restore` after update
- Supports Central Package Management

## CI/CD Workflows

### Expected Workflow Structure

```yaml
# .github/workflows/publish.yml
name: Publish Package

on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'package.json'  # or *.csproj

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      # ... build steps ...
      - name: Publish
        run: npm publish  # or dotnet nuget push
```

### Workflow Detection

The package-version-manager looks for:
- Workflow file matching configured name
- `push` trigger on main/master
- Publish step in jobs

## Environment Variables

Required for package management:

```bash
# GitHub API access
export GITHUB_TOKEN="ghp_xxxx"

# NPM publishing (if using private registry)
export NPM_TOKEN="npm_xxxx"

# NuGet publishing (if using private feed)
export NUGET_API_KEY="xxxx"
```

## Update Policies

### Auto-Update Triggers

| Condition | Action |
|-----------|--------|
| Patch version (1.2.3 → 1.2.4) | Auto-update, auto-merge PR |
| Minor version (1.2.0 → 1.3.0) | Auto-update, require review |
| Major version (1.0.0 → 2.0.0) | Manual update, breaking change review |

### Excluded Repos

Repos that should NOT be auto-updated:

```json
{
  "excluded": [
    "legacy-app",
    "archived-service"
  ]
}
```
