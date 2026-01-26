# Agent Template - Unified Format

## Format Specification

```markdown
---
name: agent-name
description: |
  Brief description of what this agent does.
  Include trigger conditions (when to use).
tools: [Read, Grep, Glob]  # Only tools this agent needs
model: sonnet              # haiku|sonnet|opus based on complexity
---

# Purpose
<!-- 1-2 sentences: What this agent does and why it exists -->

# Variables
<!-- Input variables this agent expects -->
- `$REPO_PATH`: Path to repository being validated
- `$SERVICE_NAME`: Name of the microservice (optional)

# Context Requirements
<!-- What context/files this agent needs access to -->
- references/architecture-decisions.md
- references/patterns/{domain}.md

# Instructions
<!-- Step-by-step execution logic -->
1. First action
2. Second action
3. ...

# Validation Rules
<!-- Specific rules to check - link to references for details -->
- Rule category 1: See references/rules/category1.md
- Rule category 2: See references/rules/category2.md

# Report Format
<!-- Exact output structure - keep minimal -->
```json
{
  "agent": "agent-name",
  "status": "PASS|WARN|FAIL",
  "issues": [],
  "summary": ""
}
```
```

## Design Principles

### Keep It Minimal
- Each section should justify its token cost
- Link to references instead of embedding large content
- Agent prompt itself should be <100 lines

### Be Specific
- Clear trigger conditions in description
- Explicit tool restrictions
- Structured output format

### Enable Determinism
- Use Python scripts for repeatable checks
- Reference scripts by path, not inline code
- Scripts return structured JSON

## Section Guidelines

### Purpose
- One sentence: what it does
- One sentence: when to use it
- No "this agent" preamble

### Variables
- Only list variables the agent actually uses
- Include type hints: `$VAR (string)`, `$VAR (path)`, `$VAR (json)`
- Mark optional with `(optional)`

### Context Requirements
- List files agent needs to read
- Use relative paths from project root
- Group by category if many

### Instructions
- Numbered steps for sequential logic
- Bullet points for parallel/conditional
- Reference scripts: `Run scripts/validate-x.py`
- Keep to 5-10 steps max

### Validation Rules
- Don't embed rules in agent file
- Link to references/rules/*.md files
- Group by category

### Report Format
- Consistent JSON structure across all agents
- Include `agent` field for identification
- Status: PASS (all good), WARN (non-blocking), FAIL (blocking issues)
- Keep `issues` array items brief
