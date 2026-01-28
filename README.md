# Claude Code Multi-Agent Setup

Multi-agent system for architectural validation, feature planning, and CI/CD management across microservices.

## Repository Structure

```
claude-code-setup/
│
├── copy-to-repo/               ← COPY THIS TO YOUR PROJECTS
│   └── .claude/                # Everything goes in .claude folder
│       ├── CLAUDE.md           # Main instructions
│       ├── settings.json       # Hooks configuration
│       ├── hooks/              # Auto-telemetry scripts
│       ├── agents/             # Agent definitions
│       ├── commands/           # Slash command definitions
│       ├── skills/             # Reusable skills
│       └── knowledge/          # Knowledge files (customize these!)
│
├── generator/                  ← USED BY CLAUDE TO CREATE NEW CONTENT
│   └── templates/
│
├── README.md
└── INIT.md
```

## Quick Start

### 1. Copy to Your Repository

```bash
# Copy .claude folder to your project
cp -r copy-to-repo/.claude /path/to/your/repo/
```

Your repo will then have:
```
your-repo/
├── .claude/
│   ├── CLAUDE.md
│   ├── agents/
│   ├── commands/
│   ├── skills/
│   ├── knowledge/      # ← Customize these!
│   └── hooks/
└── ... your code
```

### 2. Customize Knowledge Files

Edit the knowledge files to match your project:
- `.claude/knowledge/architecture/` - Your system architecture, service boundaries
- `.claude/knowledge/packages/` - Your NPM/NuGet package structure
- `.claude/knowledge/validation/` - Your pattern rules

### 3. Use Commands

| Command | Purpose |
|---------|---------|
| `/validate` | Run architectural validation |
| `/plan-feature "description"` | Plan a feature implementation |
| `/plan-council "description"` | Multi-perspective feature planning |
| `/implement-feature "description"` | Implement feature end-to-end |
| `/fix-bug "description"` | Fix a bug |
| `/commit` | Generate intelligent commit |

## Key Features

- **Autonomous Execution** - Agents run end-to-end without stopping between phases
- **Parallel Implementation** - Backend and frontend work runs simultaneously
- **GitFlow Hard Gate** - All code changes go through feature branches and PRs
- **Automatic Telemetry** - Agent activity logged via hooks (no manual logging)

## Creating New Content

Ask Claude to create new agents, commands, or skills:
- "Create a new agent for [purpose]"
- "Add a command for [action]"

Claude uses templates from `generator/templates/`.
