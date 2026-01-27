---
name: docs-sync
description: |
  Documentation synchronization between code repositories and Confluence.
  Trigger: documentation updates, ADR changes, architecture docs sync,
  keeping Confluence in sync with code-level documentation.
triggers:
  - /sync-docs
  - sync documentation
  - update confluence
---

# Purpose

Synchronizes architecture documentation between code repositories and Confluence,
ensuring single source of truth with bi-directional awareness.

# Knowledge References

This skill loads domain knowledge from:

```
knowledge/architecture/system-architecture.md        → ADR templates, system structure
```

# Cookbook

| Recipe | Purpose |
|--------|---------|
| `extract-docs.md` | How to extract docs from repos |
| `compare-confluence.md` | Compare local vs Confluence |
| `sync-workflow.md` | Push/pull sync workflow |

# Tools

| Tool | Purpose |
|------|---------|
| `confluence-api.py` | Confluence REST API wrapper |
| `extract-docs.py` | Extract docs from repositories |
| `diff-docs.py` | Compare local and Confluence |
| `sync-docs.py` | Orchestrate sync operations |

# Assets

- `assets/confluence-template.html` - Standard page template

# Configuration
<!-- TODO: Set your Confluence details -->
```yaml
confluence:
  base_url: "https://your-domain.atlassian.net/wiki"
  space_key: "ARCH"  # Your architecture space
  # API token set via environment: CONFLUENCE_API_TOKEN

doc_sources:
  - type: adr
    repo_pattern: "**/docs/adr/*.md"
    confluence_parent: "Architecture Decision Records"
  - type: service-docs
    repo_pattern: "**/ARCHITECTURE.md"
    confluence_parent: "Service Architecture"
  - type: runbooks
    repo_pattern: "**/docs/runbooks/*.md"
    confluence_parent: "Runbooks"
```

# Workflow

## Extract Documentation
```bash
# Extract all docs from repositories
python tools/extract-docs.py \
  --repos-root $REPOS_ROOT \
  --output docs-manifest.json

# Output: docs-manifest.json with all discovered docs
```

## Compare with Confluence
```bash
# Diff local docs against Confluence
python tools/diff-docs.py \
  --manifest docs-manifest.json \
  --confluence-space ARCH \
  --output diff-report.json

# Output: diff-report.json with changes
```

## Sync to Confluence
```bash
# Preview changes (dry-run)
python tools/sync-docs.py \
  --diff diff-report.json \
  --dry-run

# Apply changes
python tools/sync-docs.py \
  --diff diff-report.json \
  --apply
```

## Pull from Confluence
```bash
# For docs that are Confluence-primary
python tools/sync-docs.py \
  --direction pull \
  --pages "Architecture Overview,System Diagram" \
  --output-dir ./docs/from-confluence
```

# Output
Sync report with:
- Pages created
- Pages updated
- Pages unchanged
- Conflicts detected (manual resolution needed)
