# Commit Conventions

<!--
TODO: Customize these conventions for your organization.
This file is loaded by commit-manager for message generation.
-->

## Conventional Commits Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Types

| Type | When to Use | Example |
|------|-------------|---------|
| `feat` | New feature for users | `feat(auth): add OAuth2 login` |
| `fix` | Bug fix for users | `fix(api): handle null response` |
| `refactor` | Code change (no feature/fix) | `refactor(utils): simplify date parsing` |
| `perf` | Performance improvement | `perf(query): add index for user lookup` |
| `test` | Adding/updating tests | `test(auth): add OAuth flow tests` |
| `docs` | Documentation only | `docs(readme): update setup instructions` |
| `style` | Formatting, whitespace | `style(lint): fix eslint warnings` |
| `chore` | Maintenance, deps | `chore(deps): update lodash to 4.17.21` |
| `ci` | CI/CD changes | `ci(actions): add caching step` |
| `build` | Build system changes | `build(webpack): optimize bundle size` |

## Scope

Scope should indicate the component/module affected:

- Use the directory name if changes are isolated: `feat(auth):`
- Use the feature name for cross-cutting: `feat(user-management):`
- Omit scope if truly global: `chore: update dependencies`

## Subject Line Rules

1. **Imperative mood**: "add feature" not "added feature"
2. **Lowercase**: "add feature" not "Add feature"
3. **No period**: "add feature" not "add feature."
4. **Max 50 characters**: Keep it concise
5. **What, not how**: Describe the change, not the implementation

Good:
- `add user authentication`
- `fix memory leak in image processor`
- `remove deprecated API endpoints`

Bad:
- `Added authentication` (past tense)
- `Fixed bug` (vague)
- `Changes to support new auth system.` (period, vague)

## Body

- Wrap at 72 characters
- Explain **what** and **why**, not **how**
- Use bullet points for multiple changes
- Reference issues/tickets if applicable

## Footer

### Breaking Changes

```
BREAKING CHANGE: <description>

<migration instructions>
```

### Issue References

```
Refs: JIRA-123
Closes: #456
```

## Examples

### Simple Feature
```
feat(cart): add quantity selector

Allow users to change item quantity directly in cart
without removing and re-adding items.
```

### Bug Fix with Ticket
```
fix(checkout): prevent double submission

Add loading state to prevent users from clicking
submit multiple times during payment processing.

Refs: JIRA-456
```

### Breaking Change
```
feat(api)!: change user endpoint response format

BREAKING CHANGE: User endpoint now returns nested
address object instead of flat fields.

Migration:
- Update clients to access user.address.street
  instead of user.street
```

### Dependency Update
```
chore(deps): update react to 18.2.0

- Enables concurrent features
- Improves hydration performance
- Required for new streaming SSR
```

## Auto-Detection Rules

The commit-manager uses these patterns to determine type:

| Files Changed | Detected Type |
|--------------|---------------|
| `src/**/*.{ts,js,cs,py}` (new) | `feat` |
| `test/**/*`, `*.test.*` | `test` |
| `docs/**/*`, `*.md` | `docs` |
| `package.json`, `*.csproj` | `chore` |
| `.github/**/*` | `ci` |
| `webpack.*`, `tsconfig.*` | `build` |

Keywords in diff also influence detection:
- "fix", "bug", "issue" → `fix`
- "refactor", "rename" → `refactor`
- "perf", "optimize" → `perf`
