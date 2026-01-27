# Agent Template - Unified Format

## Format Specification

```markdown
---
name: agent-name
description: |
  Brief description of what this agent does.
  Include trigger conditions (when to use).
tools: [Read, Grep, Glob]  # Only tools this agent needs - add Task if spawning subagents
model: sonnet              # haiku|sonnet|opus based on complexity
---

# Purpose
<!-- 1-2 sentences: What this agent does and why it exists -->

# Variables
<!-- Input variables this agent expects -->
- `$REPO_PATH (path)`: Path to repository being validated
- `$SERVICE_NAME (string, optional)`: Name of the microservice

# Knowledge References

Load patterns from BOTH base knowledge (MD) and learned knowledge (YAML):
```
knowledge/[category]/[topic].md              → Base patterns (user-defined)
knowledge/[category]/[topic].learned.yaml    → Learned patterns (auto-discovered)
```

**Load order**: Base MD first, then YAML. YAML extends MD with discovered patterns.

# Instructions

## 1. Load Knowledge (Base + Learned)
```
Read: knowledge/[category]/[topic].md
Read: knowledge/[category]/[topic].learned.yaml
```

Merge patterns from both - learned YAML patterns extend base MD.

## 2. [Analysis Steps]
<!-- Use built-in tools for all analysis -->
```
Glob: [pattern]           → Find files
Grep: [pattern] in [path] → Search content
Read: [file]              → Read specific files
```

## 3. [Validation/Processing]
<!-- Numbered steps for sequential logic -->

## N. Record Learnings (REQUIRED)

After completing work, record any NEW discoveries to learned knowledge:

```
Task: spawn knowledge-updater
Prompt: |
  Update learned knowledge with discoveries:
  $KNOWLEDGE_TYPE = [topic]
  $SOURCE_AGENT = [this-agent-name]
  $SOURCE_FILE = [file that was analyzed]
  $LEARNING = {
    "patterns": [newly discovered patterns],
    "anti_patterns": [newly discovered anti-patterns],
    "conventions": [newly discovered conventions]
  }
```

Only record if:
- New pattern not in base knowledge
- New anti-pattern discovered
- Higher occurrence count than previously recorded

# Validation Rules
<!-- Specific rules to check - reference knowledge files -->
- Pattern category 1: See knowledge/validation/[topic].md
- Pattern category 2: See knowledge/architecture/[topic].md

# Report Format
<!-- Exact output structure -->
```json
{
  "agent": "agent-name",
  "status": "PASS|WARN|FAIL",
  "issues": [],
  "learnings_recorded": {
    "new_patterns": 0,
    "new_anti_patterns": 0,
    "new_conventions": 0
  },
  "summary": ""
}
```
```

## Design Principles

### Keep It Minimal
- Each section should justify its token cost
- Link to knowledge files instead of embedding patterns
- Agent prompt itself should be <100 lines

### Use Built-in Tools for Analysis
- **Read** - Read file contents
- **Grep** - Search for patterns in files
- **Glob** - Find files by pattern
- **Task** - Spawn subagents (add when needed)
- **Bash** - ONLY for git commands, build tools, or native CLI tools

**NEVER** use Python scripts for:
- File reading (use Read)
- Pattern matching (use Grep)
- File discovery (use Glob)
- Any analysis that built-in tools can do

### Knowledge-Driven Patterns
- All patterns/rules in knowledge files, NOT hardcoded in agents
- Reference both MD (base) and YAML (learned) files
- Agent is a reasoning engine, knowledge files are the rules

### Self-Improving System
- Load both base (MD) and learned (YAML) knowledge
- After work completes, spawn knowledge-updater to record discoveries
- YAML files accumulate patterns over time

## Section Guidelines

### Purpose
- One sentence: what it does
- One sentence: when to use it
- No "this agent" preamble

### Variables
- Only list variables the agent actually uses
- Include type hints: `$VAR (string)`, `$VAR (path)`, `$VAR (bool)`
- Mark optional with `(optional)`
- Include defaults where applicable

### Knowledge References
- List both MD and YAML files for each topic
- Explain load order (MD first, YAML extends)
- Group by category (validation/, architecture/, packages/)

### Instructions
- Start with "Load Knowledge" section
- Use tool syntax: `Glob:`, `Grep:`, `Read:`
- End with "Record Learnings" section
- Keep to 5-10 steps max

### Report Format
- Consistent JSON structure across all agents
- Include `agent` field for identification
- Status: PASS (all good), WARN (non-blocking), FAIL (blocking issues)
- Include `learnings_recorded` for tracking self-improvement

## Tool Selection Guide

| Task | Tool | Example |
|------|------|---------|
| Find files | Glob | `Glob: $REPO/**/*.cs` |
| Search content | Grep | `Grep: "pattern" in $REPO/src/` |
| Read file | Read | `Read: $REPO/package.json` |
| Spawn subagent | Task | `Task: spawn validator-agent` |
| Git commands | Bash | `Bash: git status` |
| Build/test | Bash | `Bash: npm test` |

## Knowledge File Paths

```
knowledge/
├── validation/           → Pattern validation rules
│   ├── backend-patterns.md
│   ├── backend-patterns.learned.yaml
│   ├── frontend-patterns.md
│   └── frontend-patterns.learned.yaml
├── architecture/         → System design rules
│   ├── system-architecture.md
│   ├── system-architecture.learned.yaml
│   ├── service-boundaries.md
│   ├── service-boundaries.learned.yaml
│   ├── design-patterns.md
│   ├── design-patterns.learned.yaml
│   ├── tech-stack.md
│   └── tech-stack.learned.yaml
├── packages/             → Package/repo config
│   ├── core-packages.md
│   ├── core-packages.learned.yaml
│   ├── package-config.md
│   ├── package-config.learned.yaml
│   └── repo-config.md
└── commit-conventions.md
```
