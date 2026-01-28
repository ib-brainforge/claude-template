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

Load patterns from base knowledge:
```
knowledge/[category]/[topic].md  → Pattern definitions, rules
```

For implementation agents (feature-planner, etc.), also load recent changes:
```
knowledge/architecture/system-architecture.learned.yaml  → Recent features
knowledge/architecture/service-boundaries.learned.yaml   → Recent communications
```

# Instructions

## 1. Load Knowledge
```
Read: knowledge/[category]/[topic].md
```

## 2. [Analysis Steps]
<!-- Use built-in tools for all analysis -->
```
Glob: [pattern]           → Find files
Grep: [pattern] in [path] → Search content
Read: [file]              → Read specific files
```

## 3. [Validation/Processing]
<!-- Numbered steps for sequential logic -->

# Validation Rules
<!-- Specific rules to check - reference knowledge files -->
- Pattern category 1: See knowledge/validation/[topic].md
- Pattern category 2: See knowledge/architecture/[topic].md

# Output Prefix (Observability)
<!-- ALWAYS prefix output with agent identifier -->
[agent-name] Starting analysis...
[agent-name] Loading knowledge files...
[agent-name] Found X issues...

# Report Format
<!-- Exact output structure -->
```json
{
  "agent": "agent-name",
  "status": "PASS|WARN|FAIL",
  "issues": [],
  "summary": ""
}
```
```

## Observability Requirements

Every agent MUST follow these observability patterns for tracking and debugging.

### 1. Output Prefix
Every message MUST start with agent name in brackets:
```
[backend-pattern-validator] Starting validation of auth-service...
[backend-pattern-validator] Found 2 warnings, 0 errors
```

### 2. Telemetry Logging (REQUIRED)

**On Agent Start:**
```bash
Bash: |
  AGENT_ID="$(date +%s%N | cut -c1-13)"
  echo "[$(date -Iseconds)] [START] [$AGENT_NAME] id=$AGENT_ID parent=$PARENT_ID depth=$DEPTH model=$MODEL" >> .claude/agent-activity.log
```

Note: `$MODEL` comes from the agent's YAML frontmatter (haiku/sonnet/opus).

**On Knowledge File Load:**
```bash
Bash: echo "[$(date -Iseconds)] [LOAD] [$AGENT_NAME] file=$KNOWLEDGE_FILE" >> .claude/agent-activity.log
```

**On Spawning Child Agent:**
```bash
Bash: echo "[$(date -Iseconds)] [SPAWN] [$AGENT_NAME] child=$CHILD_AGENT_NAME" >> .claude/agent-activity.log
```

**On Agent Complete:**
```bash
Bash: |
  # Estimate tokens (tool_uses * ~500 for input, output_lines * ~10 for output)
  echo "[$(date -Iseconds)] [COMPLETE] [$AGENT_NAME] id=$AGENT_ID status=$STATUS tokens=$ESTIMATED_TOKENS duration=${DURATION}s" >> .claude/agent-activity.log
```

**On High Context Warning:**
```bash
Bash: |
  if [ $ESTIMATED_TOKENS -gt ${AGENT_CONTEXT_WARN_THRESHOLD:-15000} ]; then
    echo "[$(date -Iseconds)] [WARN] [$AGENT_NAME] HIGH_CONTEXT tokens=$ESTIMATED_TOKENS threshold=15000" >> .claude/agent-activity.log
  fi
```

### 3. Report Format with Telemetry

```json
{
  "agent": "agent-name",
  "agent_id": "1706123456789",
  "parent_id": "1706123456000",
  "depth": 1,
  "model": "sonnet",
  "status": "PASS|WARN|FAIL",
  "telemetry": {
    "started_at": "2026-01-27T10:30:00Z",
    "completed_at": "2026-01-27T10:31:30Z",
    "duration_seconds": 90,
    "model": "sonnet",
    "estimated_tokens": {
      "input": 12000,
      "output": 2500,
      "total": 14500
    },
    "knowledge_files_loaded": [
      "knowledge/architecture/system-architecture.md"
    ],
    "tools_used": {
      "Read": 5,
      "Grep": 3,
      "Glob": 2,
      "Task": 0,
      "Bash": 2
    }
  },
  "children_spawned": [
    {
      "name": "backend-pattern-validator",
      "agent_id": "1706123456800",
      "model": "sonnet",
      "status": "PASS",
      "tokens": 8500,
      "duration_seconds": 45
    }
  ],
  "work_summary": "Brief description of what this agent did",
  "issues": [],
  "warnings": []
}
```

### 4. Context Estimation

Since exact token counts aren't available, estimate based on:
- **Input tokens**: ~500 per tool use + ~200 per knowledge file loaded
- **Output tokens**: ~10 per line of output generated

```
TOOL_USES=10
KNOWLEDGE_FILES=3
OUTPUT_LINES=50

INPUT_TOKENS=$((TOOL_USES * 500 + KNOWLEDGE_FILES * 200))   # 5600
OUTPUT_TOKENS=$((OUTPUT_LINES * 10))                         # 500
TOTAL_TOKENS=$((INPUT_TOKENS + OUTPUT_TOKENS))               # 6100
```

### 5. Environment Variables

Agents should respect these thresholds:
```bash
AGENT_CONTEXT_WARN_THRESHOLD=15000   # Warn if agent uses more
AGENT_CONTEXT_ERROR_THRESHOLD=30000  # Agent should split work
```

---

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
- Agent is a reasoning engine, knowledge files are the rules

### Recording Learned Knowledge

**WHO records:** Only implementation agents (feature-planner, commit-manager)
**WHO doesn't:** Validators don't record - they only validate

**WHAT to record:** Significant architectural changes only
- ✅ New feature implemented across services
- ✅ New service communication established
- ✅ Breaking change made
- ✅ Architectural decision with rationale
- ❌ Pattern found during grep (don't record)
- ❌ Validation passed (don't record)

**HOW to record (for implementation agents only):**
```
Task: spawn knowledge-updater
Prompt: |
  $KNOWLEDGE_TYPE = system-architecture
  $LEARNING = {
    "type": "feature",
    "description": "What was implemented",
    "ticket": "FEAT-123",
    "affected_services": [
      {"name": "service", "changes": ["what changed"]}
    ],
    "breaking": false
  }
```

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
- List MD knowledge files needed
- For implementation agents, also list learned YAML files to check recent changes
- Validators only need MD files (they don't record)

### Instructions
- Start with "Load Knowledge" section
- Use tool syntax: `Glob:`, `Grep:`, `Read:`
- Keep to 5-10 steps max
- Implementation agents add "Record to Learned Knowledge" at end

### Report Format
- Consistent JSON structure across all agents
- Include `agent` field for identification
- Status: PASS (all good), WARN (non-blocking), FAIL (blocking issues)

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
├── validation/           → Pattern validation rules (validators read these)
│   ├── backend-patterns.md
│   ├── frontend-patterns.md
│   └── security-standards.md
├── architecture/         → System design rules + learned changes
│   ├── system-architecture.md
│   ├── system-architecture.learned.yaml   ← Recent features, decisions
│   ├── service-boundaries.md
│   ├── service-boundaries.learned.yaml    ← Recent communications, contracts
│   ├── design-patterns.md
│   ├── tech-stack.md
│   └── tech-stack.learned.yaml            ← Recent dependency changes
├── packages/             → Package/repo config
│   ├── core-packages.md
│   ├── package-config.md
│   └── repo-config.md
└── commit-conventions.md
```

## Agent Types

### Validators (Don't Record)
- backend-pattern-validator
- frontend-pattern-validator
- infrastructure-validator
- service-validator
- core-validator
- plan-validator

These agents validate code against patterns. They read knowledge but don't modify it.

### Single Writer (Records Learnings)
- **commit-manager** - ONLY agent that writes to learned YAML files

This prevents concurrent write conflicts. commit-manager records after commits complete,
based on actual changes made (from git diff/commit messages).

### Readers of Learned Knowledge
- feature-planner - Reads learned YAML to check recent changes before planning
- master-architect - Reads to understand recent architectural decisions

These agents READ learned knowledge but do NOT write to it.
