# Agent Telemetry System

## Purpose

Track agent execution to understand:
- **Call hierarchy** - Who spawned who
- **Context usage** - Tokens used per agent
- **Parallelism** - How many agents ran concurrently
- **Work distribution** - What each agent did
- **Bottlenecks** - Which agents use too much context

## Telemetry File

Location: `.claude/telemetry/session-{timestamp}.json`

Each agent writes its telemetry when it starts and completes.

## Data Structure

```json
{
  "session_id": "2026-01-27T10:30:00Z",
  "root_command": "/plan-council 'Add inline-edit'",
  "total_agents_spawned": 12,
  "total_context_tokens": 245000,
  "max_parallel_agents": 5,
  "duration_seconds": 180,
  "agents": [
    {
      "id": "agent-001",
      "name": "planning-council",
      "parent_id": null,
      "depth": 0,
      "started_at": "2026-01-27T10:30:00Z",
      "completed_at": "2026-01-27T10:32:30Z",
      "duration_seconds": 150,
      "status": "PASS",
      "context": {
        "input_tokens": 8500,
        "output_tokens": 3200,
        "total_tokens": 11700,
        "knowledge_files_loaded": [
          "knowledge/architecture/system-architecture.md",
          "knowledge/architecture/service-boundaries.md"
        ],
        "tools_used": ["Read", "Grep", "Task"]
      },
      "children_spawned": ["agent-002", "agent-003", "agent-004", "agent-005", "agent-006"],
      "work_summary": "Spawned 5 plan-analysts, aggregated results"
    },
    {
      "id": "agent-002",
      "name": "plan-analyst",
      "perspective": "Pragmatic",
      "parent_id": "agent-001",
      "depth": 1,
      "started_at": "2026-01-27T10:30:05Z",
      "completed_at": "2026-01-27T10:31:15Z",
      "duration_seconds": 70,
      "status": "PASS",
      "context": {
        "input_tokens": 12000,
        "output_tokens": 2500,
        "total_tokens": 14500,
        "knowledge_files_loaded": ["..."],
        "tools_used": ["Read", "Grep", "Glob"]
      },
      "children_spawned": [],
      "work_summary": "Analyzed feature from Pragmatic perspective"
    }
  ],
  "call_tree": {
    "planning-council": {
      "plan-analyst:Pragmatic": {},
      "plan-analyst:Architectural": {},
      "plan-analyst:Risk-Aware": {},
      "plan-analyst:User-Centric": {},
      "plan-analyst:Performance": {}
    }
  },
  "context_breakdown": {
    "by_agent": {
      "planning-council": 11700,
      "plan-analyst:Pragmatic": 14500,
      "plan-analyst:Architectural": 15200,
      "plan-analyst:Risk-Aware": 13800,
      "plan-analyst:User-Centric": 14100,
      "plan-analyst:Performance": 13500
    },
    "by_depth": {
      "0": 11700,
      "1": 71100
    },
    "total": 82800
  },
  "warnings": [
    {
      "type": "HIGH_CONTEXT",
      "agent": "plan-analyst:Architectural",
      "message": "Used 15200 tokens (threshold: 15000)",
      "recommendation": "Consider splitting analysis into smaller chunks"
    }
  ]
}
```

## Environment Variables

```bash
# Enable telemetry (default: true)
AGENT_TELEMETRY_ENABLED=true

# Context warning threshold (tokens)
AGENT_CONTEXT_WARN_THRESHOLD=15000

# Context error threshold (tokens) - agent should split
AGENT_CONTEXT_ERROR_THRESHOLD=30000

# Telemetry output directory
AGENT_TELEMETRY_DIR=.claude/telemetry
```

## Bash Commands for Telemetry

### Initialize Session
```bash
# At start of orchestrator
SESSION_ID=$(date -Iseconds)
TELEMETRY_FILE=".claude/telemetry/session-${SESSION_ID//:/}.json"
mkdir -p .claude/telemetry
echo '{"session_id":"'$SESSION_ID'","agents":[],"call_tree":{}}' > "$TELEMETRY_FILE"
```

### Record Agent Start
```bash
# When agent starts
AGENT_ID="agent-$(date +%s%N | cut -c1-13)"
START_TIME=$(date -Iseconds)

# Append to activity log
echo "[${START_TIME}] [START] [$AGENT_NAME] id=$AGENT_ID parent=$PARENT_ID" >> .claude/agent-activity.log
```

### Record Agent Complete
```bash
# When agent completes
END_TIME=$(date -Iseconds)
echo "[${END_TIME}] [COMPLETE] [$AGENT_NAME] id=$AGENT_ID status=$STATUS tokens=$TOTAL_TOKENS" >> .claude/agent-activity.log
```

### Record Context Usage
```bash
# Estimate context from tool uses (rough approximation)
# Real token counts come from Claude's response metadata
echo "[$(date -Iseconds)] [CONTEXT] [$AGENT_NAME] input=$INPUT_TOKENS output=$OUTPUT_TOKENS" >> .claude/agent-activity.log
```

## Activity Log Format

Simple line-based log at `.claude/agent-activity.log`:

```
[2026-01-27T10:30:00+00:00] [START] [planning-council] id=agent-001 parent=main depth=0
[2026-01-27T10:30:05+00:00] [SPAWN] [planning-council] spawning=plan-analyst perspective=Pragmatic
[2026-01-27T10:30:05+00:00] [START] [plan-analyst:Pragmatic] id=agent-002 parent=agent-001 depth=1
[2026-01-27T10:30:05+00:00] [START] [plan-analyst:Architectural] id=agent-003 parent=agent-001 depth=1
[2026-01-27T10:30:05+00:00] [START] [plan-analyst:Risk-Aware] id=agent-004 parent=agent-001 depth=1
[2026-01-27T10:30:05+00:00] [START] [plan-analyst:User-Centric] id=agent-005 parent=agent-001 depth=1
[2026-01-27T10:30:05+00:00] [START] [plan-analyst:Performance] id=agent-006 parent=agent-001 depth=1
[2026-01-27T10:30:10+00:00] [LOAD] [plan-analyst:Pragmatic] file=knowledge/architecture/system-architecture.md
[2026-01-27T10:31:15+00:00] [COMPLETE] [plan-analyst:Pragmatic] id=agent-002 status=PASS tokens=14500 duration=70s
[2026-01-27T10:31:20+00:00] [COMPLETE] [plan-analyst:Performance] id=agent-006 status=PASS tokens=13500 duration=75s
[2026-01-27T10:31:25+00:00] [COMPLETE] [plan-analyst:Risk-Aware] id=agent-004 status=PASS tokens=13800 duration=80s
[2026-01-27T10:31:30+00:00] [COMPLETE] [plan-analyst:User-Centric] id=agent-005 status=PASS tokens=14100 duration=85s
[2026-01-27T10:31:35+00:00] [COMPLETE] [plan-analyst:Architectural] id=agent-003 status=PASS tokens=15200 duration=90s
[2026-01-27T10:31:35+00:00] [WARN] [plan-analyst:Architectural] HIGH_CONTEXT tokens=15200 threshold=15000
[2026-01-27T10:32:30+00:00] [COMPLETE] [planning-council] id=agent-001 status=PASS tokens=11700 duration=150s
[2026-01-27T10:32:30+00:00] [SESSION] total_agents=6 total_tokens=82800 max_parallel=5
```

## Viewing Telemetry

### Quick Summary
```bash
# Show last session summary
tail -20 .claude/agent-activity.log | grep -E "\[SESSION\]|\[WARN\]"
```

### Call Hierarchy
```bash
# Show agent tree
grep -E "\[START\]|\[COMPLETE\]" .claude/agent-activity.log | tail -50
```

### Context Usage
```bash
# Show tokens per agent
grep "\[COMPLETE\]" .claude/agent-activity.log | awk -F'tokens=' '{print $2}' | awk '{sum+=$1; print} END {print "TOTAL: "sum}'
```

### Warnings Only
```bash
# Show high context warnings
grep "\[WARN\]" .claude/agent-activity.log
```
