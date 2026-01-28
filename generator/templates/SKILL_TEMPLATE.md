# Skill Template - Unified Format

## Format Specification

```markdown
---
name: skill-name
description: |
  What this skill provides.
  Trigger conditions: when to load this skill.
---

# Purpose
<!-- 1-2 sentences: What capability this skill adds -->

# Knowledge References

Load patterns from BOTH base knowledge (MD) and learned knowledge (YAML):
```
knowledge/[category]/[topic].md              → Base patterns (user-defined)
knowledge/[category]/[topic].learned.yaml    → Learned patterns (auto-discovered)
```

**Load order**: Base MD first, then YAML. YAML extends MD with discovered patterns.

# Resources
<!-- What's bundled with this skill -->
- references/: Documentation to load as needed
- assets/: Templates, configs to copy/use

# Usage

## Knowledge Files
- `knowledge/[category]/[topic].md`: Base patterns to reference
- `knowledge/[category]/[topic].learned.yaml`: Learned patterns (auto-updated)

## References
- `references/guide.md`: When to read this

# Workflow
<!-- If skill has a multi-step process -->
1. Load knowledge (base + learned)
2. Step two
3. Step three
4. Record learnings (if applicable)

# Output
<!-- What this skill produces -->
```

## Structure

```
skill-name/
├── SKILL.md               # This file - instructions
├── references/            # Documentation loaded as needed
│   └── detailed-guide.md
└── assets/                # Templates, configs
    └── template.json
```

**Note**: Skills should NOT contain Python scripts. Use built-in tools instead.

## Design Principles

### Progressive Disclosure
- SKILL.md: Core workflow (<500 lines)
- references/: Detailed docs (loaded when needed)
- Knowledge files: Pattern definitions (shared across skills/agents)

### Token Efficiency
- References loaded only when explicitly needed
- Assets copied/used, never loaded into context
- Knowledge files are focused and categorized

### Knowledge-Driven
- All patterns/rules in knowledge files, NOT embedded in skill
- Reference both MD (base) and YAML (learned) files
- Skill is a workflow guide, knowledge files are the rules

### Use Built-in Tools
- **Read** - Read file contents
- **Grep** - Search for patterns in files
- **Glob** - Find files by pattern
- **Task** - Spawn agents for complex work
- **Bash** - ONLY for git commands, build tools, or native CLI

**NEVER** use Python scripts for:
- File reading (use Read)
- Pattern matching (use Grep)
- File discovery (use Glob)
- Any analysis that built-in tools can do

## Example: Documentation Skill

```markdown
---
name: documentation
description: |
  Generate and maintain documentation for microservices.
  Trigger: When creating/updating service documentation.
---

# Purpose
Generate consistent API and service documentation.

# Knowledge References
```
knowledge/architecture/system-architecture.md
knowledge/architecture/system-architecture.learned.yaml
knowledge/architecture/tech-stack.md
knowledge/architecture/tech-stack.learned.yaml
```

# Resources
- references/doc-standards.md: Documentation format standards
- assets/templates/: Documentation templates

# Workflow

## 1. Load Knowledge
```
Read: knowledge/architecture/system-architecture.md
Read: knowledge/architecture/system-architecture.learned.yaml
```

## 2. Analyze Service
```
Glob: $SERVICE_PATH/src/**/*        → Find source files
Grep: "/// <summary>" in [files]    → Find XML docs
Grep: "\[Route\(" in [files]        → Find API endpoints
```

## 3. Generate Documentation
Using assets/templates/service-doc.md as template, generate docs.

## 4. Record Learnings
If new patterns discovered, spawn knowledge-updater:
```
Task: spawn knowledge-updater
Prompt: |
  $KNOWLEDGE_TYPE = system-architecture
  $SOURCE_AGENT = documentation-skill
  $LEARNING = { "documentation_patterns": [...] }
```

# Output
Generated documentation in Markdown format.
```

## Example: Code Review Skill

```markdown
---
name: code-review
description: |
  Perform architectural code review on changes.
  Trigger: Before committing or merging changes.
---

# Purpose
Review code changes against architectural patterns and standards.

# Knowledge References
```
knowledge/validation/backend-patterns.md
knowledge/validation/backend-patterns.learned.yaml
knowledge/validation/frontend-patterns.md
knowledge/validation/frontend-patterns.learned.yaml
knowledge/architecture/design-patterns.md
knowledge/architecture/design-patterns.learned.yaml
```

# Workflow

## 1. Load Knowledge (Base + Learned)
```
Read: knowledge/validation/backend-patterns.md
Read: knowledge/validation/backend-patterns.learned.yaml
Read: knowledge/architecture/design-patterns.md
Read: knowledge/architecture/design-patterns.learned.yaml
```

## 2. Identify Changed Files
```
Bash: git diff --name-only HEAD~1
```

## 3. Analyze Changes
For each changed file:
```
Read: [changed-file]
Grep: [patterns from knowledge] in [changed-file]
```

## 4. Validate Against Patterns
Check for:
- Pattern compliance (from knowledge files)
- Anti-pattern violations (from knowledge files)
- Convention adherence (from knowledge files)

## 5. Record Learnings
```
Task: spawn knowledge-updater
Prompt: |
  $KNOWLEDGE_TYPE = backend-patterns
  $SOURCE_AGENT = code-review-skill
  $LEARNING = {
    "patterns": [newly observed patterns],
    "anti_patterns": [newly observed anti-patterns]
  }
```

# Output
Review report with findings categorized by severity.
```

## Knowledge Integration

Skills should integrate with the knowledge system:

### Loading Knowledge
```
## 1. Load Knowledge (Base + Learned)
Read: knowledge/[category]/[topic].md
Read: knowledge/[category]/[topic].learned.yaml

Merge patterns - learned YAML extends base MD.
```

### Recording Learnings
```
## N. Record Learnings (If Applicable)
Task: spawn knowledge-updater
Prompt: |
  $KNOWLEDGE_TYPE = [topic]
  $SOURCE_AGENT = [skill-name]
  $LEARNING = { ... }
```

### Knowledge File Paths
```
knowledge/
├── validation/           → Pattern validation rules
│   ├── backend-patterns.md / .learned.yaml
│   └── frontend-patterns.md / .learned.yaml
├── architecture/         → System design rules
│   ├── system-architecture.md / .learned.yaml
│   ├── service-boundaries.md / .learned.yaml
│   ├── design-patterns.md / .learned.yaml
│   └── tech-stack.md / .learned.yaml
├── packages/             → Package/repo config
│   ├── core-packages.md / .learned.yaml
│   └── package-config.md / .learned.yaml
└── commit-conventions.md / .learned.yaml
```

## Tool Selection Guide

| Task | Tool | Example |
|------|------|---------|
| Find files | Glob | `Glob: $PATH/**/*.cs` |
| Search content | Grep | `Grep: "pattern" in $PATH/` |
| Read file | Read | `Read: $PATH/file.json` |
| Spawn agent | Task | `Task: spawn validator` |
| Git commands | Bash | `Bash: git diff` |
| Build/test | Bash | `Bash: npm build` |

## Skill vs Agent Decision

| Criteria | Skill | Agent |
|----------|-------|-------|
| Invocation | Loaded into context | Spawned as subagent |
| Context | Shares main context | Isolated context |
| Use for | Workflows, guides | Heavy processing |
| Token impact | Higher (loaded) | Lower (isolated) |
| Coordination | Direct | Via Task results |

Skills are best for:
- Multi-step workflows that need guidance
- Reference documentation
- Templates and assets

Agents are best for:
- Heavy validation work
- Parallel processing
- Work that needs isolation
