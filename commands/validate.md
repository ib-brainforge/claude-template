---
name: /validate
description: Run architecture validation across services
allowed_tools: [Task, Bash, Read]
---

# Purpose
Quick entry point for architecture validation. Delegates to validation-orchestrator subagent.

# Arguments
- `--scope`: all|changed|service (default: all)
- `--service`: Service name if scope=service
- `--level`: quick|standard|thorough (default: standard)
- `--output`: json|text (default: text)

# Workflow

1. Parse arguments from user input
2. Spawn validation-orchestrator agent:
   ```
   Task: validation-orchestrator
   Variables:
     $REPOS_ROOT = <configured repos root>
     $SCOPE = <from args>
     $SERVICE_NAME = <from args if applicable>
     $VALIDATION_LEVEL = <from args>
   ```
3. Wait for orchestrator to complete
4. Format and display results based on --output

# Examples

```
/validate
→ Full validation, standard level, text output

/validate --scope=changed
→ Only validate services with changes since last commit

/validate --service=user-api --level=thorough
→ Deep validation of specific service

/validate --output=json
→ Full validation with JSON output for CI integration
```

# Output

**Text format:**
```
Architecture Validation Report
==============================
Status: PASS/WARN/FAIL

Services validated: 5
  ✅ user-api
  ✅ auth-service
  ⚠️  frontend-app (2 warnings)
  ✅ core-utils
  ✅ infrastructure

Issues: 0 errors, 2 warnings

Warnings:
  - [frontend-app] Missing ARCHITECTURE.md
  - [frontend-app] Recommended: Add tests directory
```

**JSON format:**
Raw output from validation-orchestrator
