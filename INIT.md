# Claude Code Setup - Deployment Guide

## Required Configuration

Before deploying, you'll need to configure the following variables and files.

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `JIRA_URL` | Optional | Your Jira instance URL | `https://mycompany.atlassian.net` |
| `JIRA_USER` | Optional | Jira account email | `dev@mycompany.com` |
| `JIRA_API_TOKEN` | Optional | Jira API token ([get here](https://id.atlassian.com/manage-profile/security/api-tokens)) | `ATATT3x...` |
| `CONFLUENCE_URL` | Optional | Confluence instance URL | `https://mycompany.atlassian.net/wiki` |
| `CONFLUENCE_USER` | Optional | Confluence account email | `dev@mycompany.com` |
| `CONFLUENCE_API_TOKEN` | Optional | Confluence API token | `ATATT3x...` |
| `GITHUB_TOKEN` | Optional | GitHub token for PR operations | `ghp_...` |

Set these in your shell profile or `.env` file:
```bash
# ~/.bashrc or ~/.zshrc
export JIRA_URL="https://mycompany.atlassian.net"
export JIRA_USER="dev@mycompany.com"
export JIRA_API_TOKEN="your-token-here"
```

### Knowledge Files to Configure

| File | Required | What to Fill In |
|------|----------|-----------------|
| `knowledge/architecture/system-architecture.md` | **Yes** | Your ~40 microservices, ADRs, service categories |
| `knowledge/architecture/service-boundaries.md` | **Yes** | Allowed communications, event topics, forbidden deps |
| `knowledge/architecture/tech-stack.md` | **Yes** | .NET/React versions, packages, cloud provider |
| `knowledge/architecture/design-patterns.md` | **Yes** | Required patterns, naming conventions, folder structure |
| `knowledge/validation/backend-patterns.md` | **Yes** | C# grep patterns, anti-patterns, required attributes |
| `knowledge/validation/frontend-patterns.md` | **Yes** | React/TS patterns, component conventions |
| `knowledge/packages/core-packages.md` | **Yes** | Shared library exports, cross-cutting concerns |
| `knowledge/packages/package-config.md` | **Yes** | Package names, npm/NuGet registries, CI workflows |
| `knowledge/commit-conventions.md` | **Yes** | Commit format, scopes, ticket format |
| `knowledge/jira/jira-config.md` | Optional | Jira projects, workflows, bug patterns |

### Values to Replace in Knowledge Files

Search for these placeholders and replace with your actual values:

| Placeholder | Replace With | Found In |
|-------------|--------------|----------|
| `your-domain` | Your company domain | jira-config.md, docs-sync skill |
| `@org/` | Your npm scope | core-packages.md, package-config.md |
| `Org.` | Your NuGet namespace | core-packages.md, package-config.md |
| `PROJ` | Your Jira project key | jira-config.md |
| `ARCH` | Your Confluence space key | docs-sync skill |
| `your-org` | Your GitHub org | jira-config.md |
| Service names | Your actual service names | system-architecture.md, service-boundaries.md |

---

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

**knowledge/jira/jira-config.md** (Optional - for Jira integration)
- Your Jira URL and project keys
- Workflow status mappings
- Bug parsing patterns
- Auto-transition rules

### 2.5. Configure Jira Integration (Optional)

If you want to use Jira integration for bug tickets:

1. **Get Jira API Token**:
   - Go to https://id.atlassian.com/manage-profile/security/api-tokens
   - Create a new API token
   - Save it securely

2. **Set Environment Variables**:
   ```bash
   export JIRA_URL="https://your-domain.atlassian.net"
   export JIRA_USER="your-email@domain.com"
   export JIRA_API_TOKEN="your-api-token"
   ```

3. **Update jira-config.md**:
   - Set your project keys
   - Configure workflow statuses
   - Map components to repositories

4. **Test Connection**:
   ```bash
   curl -s -u "$JIRA_USER:$JIRA_API_TOKEN" \
     "$JIRA_URL/rest/api/3/myself" | jq '.displayName'
   ```

### 3. Initialize YAML Learned Files

The `.learned.yaml` files start empty - they'll populate as agents run. Verify they exist:

```bash
ls knowledge/**/*.learned.yaml
```

### 4. Test the Setup

#### Dry-Run Mode (Recommended First)

All commands support dry-run to preview without making changes:

```bash
# Navigate to your repos root
cd /path/to/your/repos

# Run Claude Code
claude

# Test 1: Validate a service (read-only, always safe)
> validate the auth-service against our patterns

# Test 2: Preview commits without executing (DRY_RUN=true is default)
> analyze changes and suggest commits

# Test 3: Plan a feature (creates plan file, no code changes)
> plan adding a new property to user profile
```

#### Sample Test Scenario

Run this end-to-end test to verify the setup works:

```
Step 1: Make a small change
  - Edit a file in one of your services (e.g., add a comment)

Step 2: Run validation
  > validate [service-name]
  - Should load knowledge files
  - Should return PASS/WARN/FAIL

Step 3: Preview commit
  > commit changes (dry-run)
  - Should detect changed repo
  - Should generate commit message
  - Should NOT actually commit (dry-run)

Step 4: Execute commit (when ready)
  > commit changes --execute
  - Should stage, validate, commit
  - Should record learnings (if significant)

Step 5: Verify learned knowledge
  > cat knowledge/architecture/system-architecture.learned.yaml
  - If multi-service feat, should see new entry
  - If single fix, should be empty (not significant)
```

#### Verifying Agent Flow

To see the full agent flow:

```
> plan adding lease_end_date to tenancy feature

Expected flow:
1. feature-planner loads knowledge
2. Spawns validators in parallel
3. Synthesizes plan
4. Spawns plan-validator
5. Outputs plan document

Watch for:
- Knowledge files being loaded
- Subagents being spawned
- Validation results returned
```

#### Troubleshooting

| Issue | Check |
|-------|-------|
| "Knowledge file not found" | Verify paths in agent match actual file locations |
| "No patterns loaded" | Check knowledge MD files have content |
| Validation always passes | Add actual grep patterns to knowledge files |
| Commits not recording | Only multi-service `feat` commits record learnings |

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
   - `/jira <ticket-id>` - Fetch and work on Jira tickets

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

### Required Setup
- [ ] Copy setup folders to repo (`agents/`, `skills/`, `knowledge/`, `commands/`)
- [ ] Fill in `system-architecture.md` with your services
- [ ] Fill in `service-boundaries.md` with communication rules
- [ ] Fill in `tech-stack.md` with your versions/tools
- [ ] Fill in `design-patterns.md` with your patterns
- [ ] Fill in `backend-patterns.md` with C# grep patterns
- [ ] Fill in `frontend-patterns.md` with React grep patterns
- [ ] Fill in `core-packages.md` with shared library exports
- [ ] Fill in `package-config.md` with registries and package names
- [ ] Fill in `commit-conventions.md` with your format
- [ ] Test with `claude` command

### Optional: Jira Integration
- [ ] Get Jira API token from Atlassian
- [ ] Set `JIRA_URL` environment variable
- [ ] Set `JIRA_USER` environment variable
- [ ] Set `JIRA_API_TOKEN` environment variable
- [ ] Configure `jira-config.md` with project keys and workflows
- [ ] Test with: `curl -s -u "$JIRA_USER:$JIRA_API_TOKEN" "$JIRA_URL/rest/api/3/myself"`

### Optional: Confluence Integration
- [ ] Set `CONFLUENCE_URL` environment variable
- [ ] Set `CONFLUENCE_USER` environment variable
- [ ] Set `CONFLUENCE_API_TOKEN` environment variable
- [ ] Configure space key in docs-sync skill

### Optional: GitHub Integration
- [ ] Set `GITHUB_TOKEN` environment variable (for PR operations)

### Final Steps
- [ ] Decide git tracking for `.learned.yaml` files
- [ ] Share team onboarding docs

---

## Jira Bug Fixing Workflow

If you've configured Jira integration, you can fix bugs from tickets:

```
> Fix bugs from Jira ticket PROJ-123

Expected flow:
1. bug-triage fetches ticket from Jira
2. Parses bug list from description
3. Prioritizes and orders bugs
4. Spawns bug-fixer for each bug
5. Validates all fixes
6. commit-manager commits with Jira linking
7. Updates Jira ticket with results
```

---

## Quick Reference: All Environment Variables

Copy and customize this block for your shell profile:

```bash
# ============================================
# Claude Code Multi-Agent Setup - Environment
# ============================================

# Jira Integration (Optional)
export JIRA_URL="https://YOUR-DOMAIN.atlassian.net"
export JIRA_USER="your-email@company.com"
export JIRA_API_TOKEN="your-jira-api-token"

# Confluence Integration (Optional)
export CONFLUENCE_URL="https://YOUR-DOMAIN.atlassian.net/wiki"
export CONFLUENCE_USER="your-email@company.com"
export CONFLUENCE_API_TOKEN="your-confluence-api-token"

# GitHub Integration (Optional)
export GITHUB_TOKEN="ghp_your-github-token"

# Azure DevOps Integration (Optional, if using instead of GitHub)
# export AZURE_DEVOPS_PAT="your-azure-devops-pat"
# export AZURE_DEVOPS_ORG="your-org-name"
```

---

## Quick Reference: All Knowledge Files

```
knowledge/
├── architecture/
│   ├── system-architecture.md          # Your services, ADRs
│   ├── system-architecture.learned.yaml # Auto-populated features
│   ├── service-boundaries.md           # Communication rules
│   ├── service-boundaries.learned.yaml # Auto-populated communications
│   ├── design-patterns.md              # Required patterns
│   ├── tech-stack.md                   # Versions, frameworks
│   └── tech-stack.learned.yaml         # Auto-populated dependencies
├── validation/
│   ├── backend-patterns.md             # C#/.NET grep patterns
│   └── frontend-patterns.md            # React/TS grep patterns
├── packages/
│   ├── core-packages.md                # Shared library exports
│   └── package-config.md               # Registries, package names
├── jira/
│   └── jira-config.md                  # Jira projects, workflows
└── commit-conventions.md               # Commit message format
```

---

## Quick Reference: All Agents

| Agent | Purpose | Tools |
|-------|---------|-------|
| `master-architect` | Architectural oversight, cross-service analysis | Read, Grep, Glob, Task |
| `feature-planner` | Plan features across services | Read, Grep, Glob, Task |
| `backend-pattern-validator` | Validate C#/.NET patterns | Read, Grep, Glob |
| `frontend-pattern-validator` | Validate React/TS patterns | Read, Grep, Glob |
| `core-validator` | Validate shared libraries | Read, Grep, Glob |
| `infrastructure-validator` | Validate IaC (Terraform, etc.) | Read, Grep, Glob |
| `plan-validator` | Validate implementation plans | Read, Grep, Glob |
| `commit-manager` | Git commits + record learnings (single writer) | Read, Grep, Glob, Bash, Task |
| `knowledge-updater` | Write to learned YAML files | Read, Write |
| `bug-triage` | Orchestrate bug fixing from Jira | Read, Grep, Glob, Task |
| `bug-fixer` | Apply individual bug fixes | Read, Grep, Glob, Edit, Bash |

---

## Quick Reference: All Skills

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `validation` | `/validate` | Run architectural validation |
| `feature-planning` | `/plan-feature` | Plan feature implementation |
| `design-patterns` | `/patterns` | Validate/suggest patterns |
| `commit-manager` | `/commit` | Generate commits across repos |
| `docs-sync` | `/sync-docs` | Sync docs with Confluence |
| `package-release` | `/update-packages` | Propagate package versions |
| `jira-integration` | `/jira` | Fetch tickets, update status |
