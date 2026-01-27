# Learned Knowledge System

## Overview

Each `.md` knowledge file has a companion `.learned.yaml` file:
- **`.md` files** = Base knowledge (user-defined, manually updated)
- **`.learned.yaml` files** = Learned knowledge (significant changes auto-recorded)

## What Gets Recorded

**ONLY record significant architectural knowledge:**

| Record | Don't Record |
|--------|--------------|
| New feature added to system | Individual file patterns found |
| New service communication discovered | Grep match counts |
| Breaking change made | Minor code style observations |
| New shared contract/event created | File structure discoveries |
| Architectural decision made | Routine validations |
| New integration point | Existing pattern confirmations |

### Good Examples (Record These)
```yaml
- "Added lease_end_date property to Tenancy - affects asset-backend, asset-mf, common-backend"
- "New event TenancyLeaseExpiring added to common-backend for notification triggers"
- "asset-backend now calls notification-backend via event bus for lease reminders"
- "Breaking: TenancyDto changed - all consumers need update"
```

### Bad Examples (Don't Record)
```yaml
- "Found Tenancy entity in asset-backend"  # Obvious, not useful
- "TenancyForm uses React.FC"              # Too granular
- "Grep pattern matched 5 times"           # Noise
- "Convention followed correctly"          # Not a change
```

## YAML Schema

```yaml
# [topic].learned.yaml
version: 1
last_updated: "2024-01-27T10:30:00Z"
updated_by: "feature-planner"

# Significant feature additions
features:
  - id: "feat-20240127-001"
    date: "2024-01-27"
    description: "Added lease_end_date to tenancy feature"
    ticket: "FEAT-123"
    affected_services:
      - name: "asset-backend"
        changes: ["Tenancy entity", "TenancyDto", "migration"]
      - name: "asset-mf"
        changes: ["TenancyForm", "TenancyDetails", "types"]
      - name: "common-backend"
        changes: ["TenancyEvents"]
    breaking: false
    notes: "Optional field, nullable DateTime"

# New service communications discovered
communications:
  - id: "comm-20240127-001"
    date: "2024-01-27"
    from: "asset-backend"
    to: "notification-backend"
    type: "event"
    event: "TenancyLeaseExpiring"
    purpose: "Trigger lease expiry notifications"
    discovered_in: "FEAT-123"

# New shared contracts/events
contracts:
  - id: "contract-20240127-001"
    date: "2024-01-27"
    name: "TenancyLeaseExpiring"
    location: "common-backend/src/Contracts/Events/"
    consumers: ["notification-backend", "asset-mf"]
    publisher: "asset-backend"
    added_in: "FEAT-123"

# Breaking changes log
breaking_changes:
  - id: "break-20240127-001"
    date: "2024-01-27"
    description: "TenancyDto added required LeaseEndDate field"
    affected_services: ["asset-mf", "onboard-mf"]
    migration_notes: "Update all TenancyDto consumers"
    ticket: "FEAT-123"

# Architectural decisions made during implementation
decisions:
  - id: "adr-20240127-001"
    date: "2024-01-27"
    context: "Needed to track lease expiration for tenancies"
    decision: "Add nullable LeaseEndDate to Tenancy entity"
    alternatives_considered:
      - "Separate LeaseTerms table - rejected (overkill for single field)"
      - "Store in metadata JSON - rejected (need query capability)"
    consequences: "Simple approach, can extend later if needed"
    ticket: "FEAT-123"

# Statistics (auto-updated)
stats:
  total_features: 1
  total_communications: 1
  total_contracts: 1
  total_breaking_changes: 1
  last_update: "2024-01-27T10:30:00Z"
```

## Recording Triggers

Record learned knowledge ONLY when:

1. **Feature Implementation Completes**
   - New property/field added to domain
   - New API endpoint created
   - New UI component added

2. **Service Communication Changes**
   - New service-to-service call
   - New event published/consumed
   - New API integration

3. **Shared Contract Changes**
   - New event type in common-backend
   - New shared DTO
   - Contract modification

4. **Breaking Changes**
   - DTO field changes
   - API signature changes
   - Event schema changes

5. **Architectural Decisions**
   - Why a specific approach was chosen
   - Trade-offs considered
   - Future implications

## How Agents Use This

### Reading (All Agents)
```
Read: knowledge/architecture/system-architecture.md        # Base
Read: knowledge/architecture/system-architecture.learned.yaml  # Recent changes

Check recent features to understand:
- What was recently added to affected services?
- Any recent breaking changes to consider?
- Recent communications added?
```

### Writing (ONLY commit-manager)

**Single Writer Pattern**: Only `commit-manager` writes to learned YAML files.
This prevents concurrent write conflicts when multiple agents run in parallel.

```
commit-manager (after commits complete)
    │
    └──► Task: spawn knowledge-updater
         Prompt: |
           $KNOWLEDGE_TYPE = system-architecture
           $LEARNING = {
             "type": "feature",
             "description": "[from commit messages]",
             "ticket": "FEAT-123",
             "affected_services": [...],
             "breaking": false
           }
```

**Why single writer?**
- Parallel validation agents can't conflict
- Learnings based on actual committed changes (not planned changes)
- Clear ownership and responsibility

## Deduplication Rules

1. **Same ticket ID** → Update existing entry, don't duplicate
2. **Same feature description** → Merge into existing
3. **Same date + same services** → Likely same change, merge

## Maintenance

### Weekly Review
- Review recent entries for accuracy
- Promote important decisions to base MD files
- Archive old entries (>6 months) if no longer relevant

### Cleanup Criteria
- Remove entries older than 1 year
- Remove entries superseded by newer changes
- Consolidate related entries
