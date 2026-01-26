---
name: docs-sync
description: |
  Documentation synchronization between code repositories and Confluence.
  Trigger: documentation updates, ADR changes, architecture docs sync,
  keeping Confluence in sync with code-level documentation.
---

# Purpose
Synchronizes architecture documentation between code repositories and Confluence, ensuring single source of truth with bi-directional awareness.

# Resources

## Scripts
- `scripts/confluence-api.py`: Confluence REST API wrapper
- `scripts/extract-docs.py`: Extract documentation from repositories
- `scripts/diff-docs.py`: Compare local and Confluence versions
- `scripts/sync-docs.py`: Orchestrate sync operations

## References
- `references/confluence-structure.md`: Your Confluence space organization
- `references/doc-mapping.md`: Mapping between repo docs and Confluence pages

## Assets
- `assets/confluence-template.html`: Standard page template

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
python scripts/extract-docs.py \
  --repos-root $REPOS_ROOT \
  --output docs-manifest.json

# Output: docs-manifest.json with all discovered docs
```

## Compare with Confluence
```bash
# Diff local docs against Confluence
python scripts/diff-docs.py \
  --manifest docs-manifest.json \
  --confluence-space ARCH \
  --output diff-report.json

# Output: diff-report.json with changes
```

## Sync to Confluence
```bash
# Preview changes (dry-run)
python scripts/sync-docs.py \
  --diff diff-report.json \
  --dry-run

# Apply changes
python scripts/sync-docs.py \
  --diff diff-report.json \
  --apply
```

## Pull from Confluence
```bash
# For docs that are Confluence-primary
python scripts/sync-docs.py \
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
