# Learned Knowledge System

## Overview

Each `.md` knowledge file has a companion `.learned.yaml` file:
- **`.md` files** = Base knowledge (user-defined, manually updated)
- **`.learned.yaml` files** = Learned knowledge (auto-updated by agents after implementations)

## Structure

```
knowledge/
├── validation/
│   ├── backend-patterns.md           # Base: User-defined patterns
│   ├── backend-patterns.learned.yaml # Learned: Discovered patterns
│   ├── frontend-patterns.md
│   ├── frontend-patterns.learned.yaml
│   └── ...
├── architecture/
│   ├── system-architecture.md
│   ├── system-architecture.learned.yaml
│   └── ...
```

## YAML Schema

```yaml
# [filename].learned.yaml
version: 1
last_updated: "2024-01-27T10:30:00Z"
updated_by: "agent-name"

# Learned patterns that extend base knowledge
patterns:
  - id: "pat-001"                      # Unique ID for dedup
    type: "api|database|security|component|..."
    category: "pattern|anti-pattern|convention"
    discovered_in: "services/user-api"  # Where it was found
    discovered_at: "2024-01-27T10:30:00Z"
    description: "Short description"
    grep_pattern: "actual regex pattern"  # If applicable
    example:
      file: "path/to/example.cs"
      snippet: |
        // code snippet showing the pattern
    confidence: "high|medium|low"       # How certain we are
    occurrences: 5                      # How many times seen
    tags: ["auth", "middleware"]

# Learned anti-patterns (things that caused issues)
anti_patterns:
  - id: "anti-001"
    type: "performance|security|maintainability"
    discovered_in: "services/order-api"
    discovered_at: "2024-01-27T10:30:00Z"
    description: "What the problem was"
    grep_pattern: "pattern to detect it"
    fix_suggestion: "How to fix it"
    severity: "error|warning|info"
    occurrences: 2

# Learned conventions (naming, structure)
conventions:
  - id: "conv-001"
    type: "naming|structure|config"
    discovered_in: "services/*"
    description: "Convention description"
    examples:
      - "UserController, OrderController"
    counter_examples:
      - "usersCtrl"  # What NOT to do
    occurrences: 10

# Learned service boundaries
boundaries:
  - id: "bound-001"
    from_service: "order-api"
    to_service: "user-api"
    communication: "http|grpc|event"
    discovered_at: "2024-01-27T10:30:00Z"
    contract: "GET /api/users/{id}"

# Statistics
stats:
  total_patterns: 5
  total_anti_patterns: 2
  total_conventions: 3
  last_scan: "2024-01-27T10:30:00Z"
```

## How Agents Use This

1. **Load base knowledge** (MD file) - User-defined rules
2. **Load learned knowledge** (YAML file) - Auto-discovered patterns
3. **Merge and deduplicate** - YAML extends MD, not replaces
4. **After implementation** - Call knowledge-updater to record learnings

## Deduplication Rules

Before adding to YAML, check:
1. Same `grep_pattern` already exists → Increment `occurrences`
2. Similar `description` (fuzzy match) → Update existing entry
3. Truly new → Add with new unique ID

## Who Updates YAML Files

The `knowledge-updater` agent is called by:
- `commit-manager` - After successful commits
- `service-validator` - After validation discoveries
- `design-pattern-advisor` - After pattern analysis
- `feature-planner` - After implementation completes
