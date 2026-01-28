# Claude Subagent Workflow Simulations

Generated: 2026-01-28

This document shows the EXPECTED agent call sequences for common workflows based on your `.claude/` configuration.

---

## Scenario 1: New Feature via `/implement-feature`

**User Command:**
```
/implement-feature "Add AI chatbot for LMS quiz system"
```

### Expected Agent Sequence

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    EXPECTED EXECUTION TREE                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  T+0s   ├── [main] Detected feature implementation request                       │
│         ├── [main] Spawning feature-implementor...                               │
│                                                                                  │
│  T+5s   ├── 🔀 git-workflow-manager [STEP 0 - HARD GATE]                        │
│         │      └── ACTION: start-feature                                         │
│         │      └── Pull latest develop                                           │
│         │      └── Create feature/ai-chatbot-lms-quiz branch                     │
│         │      └── Status: READY ✓                                               │
│                                                                                  │
│  T+15s  ├── 📋 feature-planner [STEP 1]                                         │
│         │      └── Analyze and identify work streams                             │
│         │      └── Output: backend work + frontend work (can_parallelize: true)  │
│                                                                                  │
│  T+30s  ├── ▶ PARALLEL IMPLEMENTATION [STEP 2]                                  │
│         │   ┌────────────────────┬────────────────────┐                          │
│         │   │ backend-implementor │ frontend-implementor│                         │
│         │   │ (.cs files)         │ (.tsx files)         │                        │
│         │   └─────────┬───────────┴─────────┬───────────┘                        │
│         │             └─────────────────────┘                                    │
│         │                   WAIT FOR ALL                                         │
│                                                                                  │
│  T+180s ├── 🔍 PARALLEL VALIDATION [STEP 3]                                     │
│         │   ┌─────────────────────────┬───────────────────────────┐              │
│         │   │ backend-pattern-validator │ frontend-pattern-validator│             │
│         │   │ • API design validation   │ • Component patterns       │            │
│         │   │ • Database patterns       │ • State management         │            │
│         │   │ • Security patterns       │ • Accessibility           │            │
│         │   │ • Error handling          │ • Performance             │            │
│         │   └────────────┬──────────────┴────────────┬──────────────┘            │
│         │                └───────────────────────────┘                           │
│         │                     WAIT FOR ALL                                       │
│         │      └── If fails: Fix issues, re-validate                             │
│                                                                                  │
│  T+210s ├── 📦 Dependency updates [STEP 4]                                      │
│         │      └── If core package changed: update consumers                     │
│         │      └── npm install --package-lock-only                               │
│                                                                                  │
│  T+220s ├── 💾 commit-manager [STEP 5]                                          │
│         │      └── Commit to feature branch (NOT develop!)                       │
│         │      └── Conventional commit message                                   │
│                                                                                  │
│  T+240s ├── 🔀 git-workflow-manager [STEP 6 - HARD GATE]                        │
│         │      └── ACTION: finish-feature                                        │
│         │      └── Push feature branch                                           │
│         │      └── Create PR to develop                                          │
│         │      └── Output: PR URL                                                │
│                                                                                  │
│  T+250s └── 📊 REPORT [STEP 7]                                                  │
│              └── Summary with PR links                                           │
│              └── Assumptions made (REVIEW comments)                              │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Agents That SHOULD Be Called:
| Agent | Purpose | When |
|-------|---------|------|
| `git-workflow-manager` | Create feature branch | Step 0 (BEFORE any code changes) |
| `feature-planner` | Analyze and split work | Step 1 |
| `backend-implementor` | Implement C# code | Step 2 (parallel) |
| `frontend-implementor` | Implement React code | Step 2 (parallel) |
| `backend-pattern-validator` | Validate C# patterns | Step 3 (parallel) |
| `frontend-pattern-validator` | Validate React patterns | Step 3 (parallel) |
| `commit-manager` | Commit changes | Step 5 |
| `git-workflow-manager` | Create PR | Step 6 (AFTER commit) |

### Your Actual Trace (for comparison):
```
✓ planning-council (with plan-analyst x5) - Step 1 OK
✓ feature-implementor x2 - Step 2 OK
⚠️ NO validators spawned - Step 3 MISSING
✓ commit-manager - Step 5 OK
❌ NO git-workflow-manager - Steps 0 & 6 MISSING
❌ Committed directly to develop instead of feature branch
```

---

## Scenario 2: Jira Bug Fix via `/fix-bugs`

**User Command:**
```
/fix-bugs BF-123
```

### Expected Agent Sequence

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    EXPECTED EXECUTION TREE                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  T+0s   ├── [main] Detected Jira bug fix request                                │
│         ├── [main] Spawning bug-triage agent for BF-123...                       │
│                                                                                  │
│  T+5s   ├── 🎫 jira-integration                                                 │
│         │      └── Fetch ticket BF-123                                           │
│         │      └── Parse bugs from description                                   │
│         │      └── Output: [bug1, bug2, bug3...]                                 │
│                                                                                  │
│  T+15s  ├── 🔀 git-workflow-manager [HARD GATE]                                 │
│         │      └── ACTION: start-feature                                         │
│         │      └── Create fix/BF-123-description branch                          │
│                                                                                  │
│  T+30s  ├── 🐛 bug-fixer x N (one per bug, PARALLEL)                           │
│         │   ┌──────────┬──────────┬──────────┐                                   │
│         │   │ bug-1    │ bug-2    │ bug-3    │                                   │
│         │   └────┬─────┴────┬─────┴────┬─────┘                                   │
│         │        └──────────┴──────────┘                                         │
│         │              WAIT FOR ALL                                              │
│                                                                                  │
│  T+120s ├── 🔍 VALIDATION                                                       │
│         │   ┌─────────────────────────┬───────────────────────────┐              │
│         │   │ backend-pattern-validator │ frontend-pattern-validator│             │
│         │   └────────────┬──────────────┴────────────┬──────────────┘            │
│         │                └───────────────────────────┘                           │
│                                                                                  │
│  T+150s ├── 💾 commit-manager                                                   │
│         │      └── Commit to fix branch                                          │
│                                                                                  │
│  T+160s ├── 🎫 jira-integration                                                 │
│         │      └── Add business-focused comment with fix table                   │
│         │      └── Link commit to ticket                                         │
│                                                                                  │
│  T+170s ├── 🔀 git-workflow-manager [HARD GATE]                                 │
│         │      └── ACTION: finish-feature                                        │
│         │      └── Create PR to develop                                          │
│                                                                                  │
│  T+180s └── 📊 REPORT                                                           │
│              └── PR URL                                                          │
│              └── Bugs fixed summary                                              │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Scenario 3: Plan-Only via `/plan-council`

**User Command:**
```
/plan-council "Add real-time notifications"
```

### Expected Agent Sequence

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    EXPECTED EXECUTION TREE                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  T+0s   ├── [main] Detected multi-perspective planning request                  │
│         ├── [main] Spawning planning-council...                                  │
│                                                                                  │
│  T+5s   ├── 📋 planning-council [opus]                                          │
│         │      └── Load knowledge files                                          │
│         │      └── Prepare perspectives                                          │
│                                                                                  │
│  T+15s  ├── 🔍 PARALLEL ANALYSIS (5 plan-analyst agents)                        │
│         │   ┌─────────────┬─────────────┬─────────────┬─────────────┬───────────┐│
│         │   │ Pragmatic   │Architectural│ Risk-Aware  │User-Centric │Performance││
│         │   │ (sonnet)    │ (sonnet)    │ (sonnet)    │ (sonnet)    │ (sonnet)  ││
│         │   └──────┬──────┴──────┬──────┴──────┬──────┴──────┬──────┴─────┬─────┘│
│         │          └─────────────┴─────────────┴─────────────┴────────────┘      │
│         │                              WAIT FOR ALL                              │
│                                                                                  │
│  T+120s ├── 📊 SYNTHESIS                                                        │
│         │      └── Compare all perspectives                                      │
│         │      └── Identify consensus vs. conflicts                              │
│         │      └── Generate recommendation                                       │
│                                                                                  │
│  T+150s └── 📋 PLAN OUTPUT                                                      │
│              └── Comprehensive plan with all perspectives                        │
│              └── Risk analysis                                                   │
│              └── Recommended approach                                            │
│              └── Work stream breakdown                                           │
│                                                                                  │
│  NOTE: No git-workflow-manager because this is PLANNING ONLY (no code changes)  │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Scenario 4: Architecture Validation via `/validate`

**User Command:**
```
/validate
```

### Expected Agent Sequence

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    EXPECTED EXECUTION TREE                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  T+0s   ├── [main] Detected validation request                                  │
│         ├── [main] Invoking validation skill...                                  │
│                                                                                  │
│  T+5s   ├── 🔍 validation-orchestrator [sonnet]                                 │
│         │      └── Load knowledge files                                          │
│         │      └── Discover services                                             │
│                                                                                  │
│  T+20s  ├── 🔍 PHASE 2: SERVICE VALIDATION (parallel)                           │
│         │   ┌─────────────────────┬─────────────────────┐                        │
│         │   │ service-validator   │ service-validator   │                        │
│         │   │ (lms-backend)       │ (lms-mf)            │                        │
│         │   └──────────┬──────────┴──────────┬──────────┘                        │
│         │              └─────────────────────┘                                   │
│                                                                                  │
│  T+60s  ├── 🔍 PHASE 3: CROSS-CUTTING (parallel)                                │
│         │   ┌─────────────────────────┬───────────────────────────┐              │
│         │   │ master-architect        │ infrastructure-validator  │              │
│         │   │ (system-wide)           │ (terraform/k8s)           │              │
│         │   └────────────┬────────────┴────────────┬──────────────┘              │
│         │                └─────────────────────────┘                             │
│                                                                                  │
│  T+120s ├── 📊 PHASE 4: AGGREGATION                                             │
│         │      └── Collect all results                                           │
│         │      └── Merge and determine status                                    │
│                                                                                  │
│  T+130s └── 📋 REPORT                                                           │
│              └── PASS/WARN/FAIL status                                           │
│              └── Critical issues                                                 │
│              └── Recommendations                                                 │
│                                                                                  │
│  NOTE: No git-workflow-manager because validation is READ-ONLY                   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Why Validators Weren't Called in Your Session

Based on your trace, here's why the dedicated validators were skipped:

### Root Cause Analysis

1. **Feature-implementor did "inline validation"**
   - Your trace shows: `feature-implementor did inline validation`
   - But per your config, it SHOULD spawn `backend-pattern-validator` and `frontend-pattern-validator` as separate Task agents

2. **git-workflow-manager was never called**
   - Commits went directly to `develop`
   - No feature branch was created
   - No PR was created
   - This violated the "HARD GATE" rule in your config

### Possible Causes

| Issue | Why It May Have Happened |
|-------|-------------------------|
| User bypassed the workflow | You may have asked to "just implement" without using `/implement-feature` |
| Context window pressure | Long conversation may have caused the agent to take shortcuts |
| Ambiguous instruction | The agent may have interpreted "implement" as "do it directly" |
| Knowledge not loaded | Agent may not have loaded `feature-implementor.md` properly |

---

## Recommendations

### 1. Strengthen CLAUDE.md Routing

Add explicit enforcement in your `CLAUDE.md`:

```markdown
## ENFORCEMENT: Mandatory Agent Calls

For ANY implementation request:
1. **git-workflow-manager** (start-feature) - BEFORE any code changes
2. **[implementors]** - Do the work
3. **backend-pattern-validator + frontend-pattern-validator** - MUST be spawned, not inline
4. **commit-manager** - Commit to feature branch
5. **git-workflow-manager** (finish-feature) - Create PR

**NEVER commit directly to develop or main.**
**NEVER do inline validation - always spawn validator agents.**
```

### 2. Add Validation Checkpoint to feature-implementor

Update `feature-implementor.md` Step 3 to be more explicit:

```markdown
### Step 3: Integration & Validation

**MANDATORY**: Spawn validators as separate agents. Do NOT validate inline.

```
Task: spawn backend-pattern-validator
Prompt: |
  Validate all .cs changes from this feature.
  $REPOS_ROOT = $REPOS_ROOT
  Files changed: [list files]

Task: spawn frontend-pattern-validator
Prompt: |
  Validate all .tsx/.ts changes from this feature.
  $REPOS_ROOT = $REPOS_ROOT
  Files changed: [list files]
```

**If you skip this step, the workflow is INVALID.**
```

### 3. Use /agent-trace After Every Workflow

Your `/agent-trace` command can detect missing calls. Add a post-workflow check:

```
After completion, verify:
- [ ] git-workflow-manager was called TWICE (start + finish)
- [ ] validators were spawned (not inline)
- [ ] All work was done on feature branch
- [ ] PR was created
```

---

## Expected Token/Time Estimates

| Workflow | Agents | Est. Tokens | Est. Duration |
|----------|--------|-------------|---------------|
| `/implement-feature` (full) | 8-10 | 150-250k | 15-30 min |
| `/fix-bugs` (multi-bug) | 6-12 | 100-200k | 10-25 min |
| `/plan-council` | 6-7 | 50-100k | 5-10 min |
| `/validate` | 4-8 | 30-80k | 3-8 min |

---

## Summary

Your subagent system is well-designed, but the execution bypassed:
1. **git-workflow-manager** (branch management)
2. **Dedicated validators** (replaced with inline checks)

This likely happened because the conversation didn't strictly follow the `/implement-feature` command pathway, or the feature-implementor took shortcuts under context pressure.

To fix: Re-run with explicit `/implement-feature` command and verify with `/agent-trace` that all expected agents were spawned.
