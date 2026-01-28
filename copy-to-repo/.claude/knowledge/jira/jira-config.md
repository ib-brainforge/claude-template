# Jira Configuration

This file contains Jira project configuration for the multi-agent system.

## Connection Settings

<!-- TODO: Update with your Jira details -->

```yaml
jira:
  base_url: "https://your-domain.atlassian.net"
  # Authentication via environment variables:
  # JIRA_USER: your-email@domain.com
  # JIRA_API_TOKEN: your-api-token
```

## Projects

<!-- TODO: Add your project keys -->

```yaml
projects:
  - key: "PROJ"
    name: "Main Project"
    default: true
  # - key: "INFRA"
  #   name: "Infrastructure"
```

## Workflows & Status Mappings

Define how ticket statuses map to your workflow:

```yaml
workflows:
  default:
    statuses:
      - name: "To Do"
        category: "todo"
      - name: "In Progress"
        category: "in_progress"
      - name: "In Review"
        category: "review"
      - name: "Done"
        category: "done"

    transitions:
      start_work: "To Do" → "In Progress"
      submit_review: "In Progress" → "In Review"
      complete: "In Review" → "Done"
      reopen: "Done" → "To Do"
```

## Ticket Types

```yaml
ticket_types:
  - name: "Bug"
    prefix: "fix"
    commit_type: "fix"
  - name: "Story"
    prefix: "feat"
    commit_type: "feat"
  - name: "Task"
    prefix: "chore"
    commit_type: "chore"
  - name: "Improvement"
    prefix: "feat"
    commit_type: "feat"
```

## Bug List Patterns

Patterns to recognize bug lists in ticket descriptions:

```yaml
bug_patterns:
  # Numbered list
  numbered: "^\\d+\\.\\s+(.+)$"

  # Bullet list (-, *, •)
  bullet: "^[-*•]\\s+(.+)$"

  # Checkbox list
  checkbox: "^\\[[ x]\\]\\s+(.+)$"

  # Header-based sections
  section_headers:
    - "Bugs:"
    - "Issues:"
    - "Problems:"
    - "To Fix:"
    - "Bug List:"
```

## Severity Mappings

Map Jira priority to severity:

```yaml
severity_mapping:
  "Highest": "critical"
  "High": "high"
  "Medium": "medium"
  "Low": "low"
  "Lowest": "low"
```

## Commit Message Format

How to include Jira ticket in commits:

```yaml
commit_format:
  # Include ticket in footer
  footer_format: "Refs: {ticket_id}"

  # Or in subject (alternative)
  # subject_format: "[{ticket_id}] {subject}"

  # Smart commit format (for Jira integration)
  smart_commit: "{ticket_id} #comment {message}"
```

## Auto-Transition Rules

When to automatically transition tickets:

```yaml
auto_transitions:
  # When first commit is pushed
  on_first_commit:
    from: "To Do"
    to: "In Progress"
    enabled: false  # Set to true to enable

  # When PR is created
  on_pr_created:
    from: "In Progress"
    to: "In Review"
    enabled: false

  # When PR is merged
  on_pr_merged:
    from: "In Review"
    to: "Done"
    enabled: false
```

## Labels & Components

Map code locations to Jira labels/components:

```yaml
component_mapping:
  # Repo name → Jira component
  "auth-service": "Authentication"
  "user-service": "User Management"
  "user-frontend": "Web UI"
  # Add more as needed
```

## Repository Links

Configure how commits link to repos:

```yaml
repository_links:
  base_url: "https://github.com/your-org"
  # Or for Azure DevOps:
  # base_url: "https://dev.azure.com/your-org/project/_git"

  commit_url_pattern: "{base_url}/{repo}/commit/{sha}"
  pr_url_pattern: "{base_url}/{repo}/pull/{pr_number}"
```

---

## Setup Instructions

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

3. **Update This File**:
   - Replace placeholder values with your actual project keys
   - Configure workflows to match your Jira setup
   - Map components to your repositories

4. **Test Connection**:
   ```bash
   curl -s -u "$JIRA_USER:$JIRA_API_TOKEN" \
     "$JIRA_URL/rest/api/3/myself" | jq '.displayName'
   ```
