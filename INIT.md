# Claude Code Setup - Deployment Guide

## Deployment Steps

### 1. Copy the Setup to Your Repository

```bash
# From your multi-repo root directory
cp -r claude-code-setup/.claude .
cp -r claude-code-setup/knowledge .
cp -r claude-code-setup/agents .
cp -r claude-code-setup/skills .
cp -r claude-code-setup/commands .
```

### 2. Configure Your Base Knowledge Files

Edit each MD file in `knowledge/` with your actual system details:

**knowledge/architecture/system-architecture.md**
- List your actual ~40 microservices
- Document your real ADRs (architectural decisions)
- Define your service categories

**knowledge/architecture/service-boundaries.md**
- Define which services can communicate
- Document your event bus topics
- List forbidden dependencies

**knowledge/architecture/tech-stack.md**
- Your .NET versions, React versions
- Your actual NuGet/npm packages
- Your cloud provider specifics (Azure/AWS/GCP)

**knowledge/architecture/design-patterns.md**
- Your required patterns (CQRS, Repository, etc.)
- Your naming conventions
- Your folder structure standards

**knowledge/validation/backend-patterns.md**
- Your C# grep patterns for validation
- Your anti-patterns to catch
- Your required attributes/decorators

**knowledge/validation/frontend-patterns.md**
- Your React/TypeScript patterns
- Your component conventions
- Your state management rules

**knowledge/packages/core-packages.md**
- Your shared library exports
- Cross-cutting concerns
- Required package usages

**knowledge/commit-conventions.md**
- Your commit message format
- Your scopes (service names)
- Your ticket/issue format

### 3. Initialize YAML Learned Files

The `.learned.yaml` files start empty - they'll populate as agents run. Verify they exist:

```bash
ls knowledge/**/*.learned.yaml
```

### 4. Test the Setup Locally

```bash
# Navigate to your repos root
cd /path/to/your/repos

# Run Claude Code
claude

# Test a validation
> validate the auth-service against our patterns

# Test commit generation
> analyze changes and suggest commits
```

### 5. Customize Agents for Your Stack

Review and adjust agents if needed:

- **backend-pattern-validator.md** - Adjust if not using C#/.NET
- **frontend-pattern-validator.md** - Adjust if not using React/TypeScript
- **infrastructure-validator.md** - Adjust for your IaC tool (Terraform/Pulumi/etc.)

### 6. Add to .gitignore (Optional)

If you don't want learned knowledge committed:

```gitignore
# Claude Code learned knowledge (auto-generated)
knowledge/**/*.learned.yaml
```

Or if you DO want to track learnings (recommended for team sharing):

```gitignore
# Don't ignore - we want to share learnings
# knowledge/**/*.learned.yaml
```

### 7. Team Onboarding

Share with your team:

```markdown
## Using Claude Code for Architecture Validation

1. Run `claude` from the repos root
2. Available commands:
   - `/validate` - Check architecture patterns
   - `/commit` - Generate conventional commits
   - `/plan <feature>` - Plan implementation

3. Knowledge files in `knowledge/` define our standards
4. Agents auto-update `*.learned.yaml` with discovered patterns
```

### 8. Ongoing Maintenance

**Weekly/Monthly:**
- Review `.learned.yaml` files for useful discoveries
- Promote valuable learned patterns to base MD files
- Remove outdated patterns from YAML files

**When Adding New Services:**
- Update `system-architecture.md` with new service
- Update `service-boundaries.md` with allowed communications
- Run validation to populate learned patterns

**When Changing Standards:**
- Update base MD knowledge files
- Clear relevant sections in `.learned.yaml` if needed

---

## Quick Checklist

- [ ] Copy setup folders to repo
- [ ] Fill in `system-architecture.md` with your services
- [ ] Fill in `service-boundaries.md` with communication rules
- [ ] Fill in `tech-stack.md` with your versions/tools
- [ ] Fill in `design-patterns.md` with your patterns
- [ ] Fill in `backend-patterns.md` with C# grep patterns
- [ ] Fill in `frontend-patterns.md` with React grep patterns
- [ ] Fill in `core-packages.md` with shared library exports
- [ ] Fill in `commit-conventions.md` with your format
- [ ] Test with `claude` command
- [ ] Decide git tracking for `.learned.yaml` files
