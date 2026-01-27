# Package Configuration

<!--
PROJECT-SPECIFIC: Update with your package registry settings.
This is referenced by: package-release skill, npm/nuget package managers
-->

## NPM Packages

### Registry

```yaml
registry: https://npm.pkg.github.com
scope: "@your-org"
```

### Core Packages

| Package | Description | Current Version |
|---------|-------------|-----------------|
| @your-org/ui | UI components | 2.3.0 |
| @your-org/hooks | React hooks | 1.5.0 |
| @your-org/api-client | API client | 1.2.0 |
| @your-org/utils | Utilities | 1.0.0 |

### Version Prefix Policy

| Prefix | Meaning | Auto-Update |
|--------|---------|-------------|
| `^` | Minor updates | Yes |
| `~` | Patch updates | Yes |
| (none) | Exact version | No |

### CI/CD

```yaml
workflow: .github/workflows/npm-publish.yml
trigger: tag v*
registry_secret: NPM_TOKEN
```

---

## NuGet Packages

### Feed

```yaml
feed: https://nuget.pkg.github.com/your-org/index.json
prefix: "YourOrg."
```

### Core Packages

| Package | Description | Current Version |
|---------|-------------|-----------------|
| YourOrg.Common | Common utilities | 3.1.0 |
| YourOrg.Data | Data access | 3.1.0 |
| YourOrg.Security | Auth/security | 2.0.0 |
| YourOrg.Validation | Validation | 2.0.0 |

### Central Package Management

Using `Directory.Packages.props`:

```xml
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>
  <ItemGroup>
    <PackageVersion Include="YourOrg.Common" Version="3.1.0" />
    <PackageVersion Include="YourOrg.Data" Version="3.1.0" />
  </ItemGroup>
</Project>
```

### CI/CD

```yaml
workflow: .github/workflows/nuget-publish.yml
trigger: tag v*
feed_secret: NUGET_TOKEN
```

---

## GitHub Configuration

```yaml
owner: your-org
repositories:
  npm_packages: core-frontend
  nuget_packages: core-backend
```

## Update Policy

| Change Type | Version Bump | Auto-Update |
|-------------|--------------|-------------|
| Bug fix | Patch (0.0.x) | Yes |
| New feature | Minor (0.x.0) | Yes (with ^) |
| Breaking change | Major (x.0.0) | No |

## Dependency Update Workflow

```
1. Core package CI builds new version
2. package-release skill detects new version
3. Scans dependent repos
4. Creates PRs with updated versions
5. CI runs tests on PRs
6. Auto-merge if tests pass (optional)
```

## References

- NPM registry docs: `docs/npm-setup.md`
- NuGet feed docs: `docs/nuget-setup.md`
