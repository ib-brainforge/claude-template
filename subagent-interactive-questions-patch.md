# Patch: Add Interactive User Questions to Subagents

## Problem

When subagents encounter blockers (like HTTP 400 errors, validation failures, or decision points), they currently:
- Output text describing the problem
- Stop silently
- Don't ask the user interactively

The user is left wondering what to do next.

## Solution

Add `AskUserQuestion` to the tools list for orchestrating agents, and add explicit instructions for when/how to use it.

---

## Patch 1: Update feature-implementor.md

**File:** `.claude/agents/feature-implementor.md`

**Add to tools list:**
```yaml
tools: [Task, Read, Grep, Glob, Bash, Edit, Write, AskUserQuestion]
```

**Add new section after "When to STOP":**

```markdown
## Interactive User Questions

When you hit a VALID BLOCKER that requires user decision, use `AskUserQuestion` to ask interactively:

### When to Ask (not just output text)

| Blocker Type | Example | Question to Ask |
|--------------|---------|-----------------|
| HTTP 4xx error | `400: Quiz must have at least one question` | "The API returned an error. Should I: (A) Create test data, (B) Skip this step, (C) Let you investigate?" |
| Multiple valid approaches | "Feature could use polling or WebSockets" | "Which approach should I use?" |
| Missing dependency | "Package X is not installed" | "Should I install package X? It adds 500KB to bundle." |
| Breaking change detected | "This changes the API signature" | "This may break existing clients. Proceed anyway?" |
| Ambiguous requirement | "Not clear if user wants X or Y" | "The requirement mentions '...' - should I implement X or Y?" |

### How to Ask

Use the `AskUserQuestion` tool with clear options:

```
AskUserQuestion:
  questions:
    - question: "The API returned '400: Quiz must have at least one question'. How should I proceed?"
      header: "API Error"
      options:
        - label: "Create test quiz data"
          description: "I'll add a quiz with sample questions so the endpoint works"
        - label: "Skip this step"
          description: "Continue with implementation, test this manually later"
        - label: "Show me the code"
          description: "I'll show you the relevant code so you can investigate"
        - label: "Abort workflow"
          description: "Stop the entire feature implementation"
      multiSelect: false
```

### What NOT to Ask

Don't ask about:
- "Should I continue to the next phase?" → Just continue
- "Is this the right file?" → Make reasonable decision
- "Which variable name?" → Follow conventions
- Internal implementation details → Just decide

**Rule: Only ask when the decision significantly impacts the outcome or requires user judgment about business requirements.**
```

---

## Patch 2: Update bug-fixer.md

**File:** `.claude/agents/bug-fixer.md`

**Add to tools list:**
```yaml
tools: [Read, Grep, Glob, Edit, Bash, AskUserQuestion]
```

**Add new section after "Error Handling":**

```markdown
## Interactive User Questions

When you can't proceed without user input, use `AskUserQuestion`:

### Trigger Conditions

| Situation | Action |
|-----------|--------|
| Multiple possible root causes | Ask which to investigate first |
| Fix would change behavior | Ask if behavior change is acceptable |
| Can't reproduce issue | Ask for more details |
| Fix requires structural change | Ask if refactoring is OK |

### Example

```
AskUserQuestion:
  questions:
    - question: "I found two possible causes for this bug. Which should I fix?"
      header: "Root cause"
      options:
        - label: "Option A: Null check missing"
          description: "Add defensive null check in processData()"
        - label: "Option B: Race condition"
          description: "Add synchronization in async handler"
        - label: "Fix both"
          description: "Apply both fixes to be safe"
      multiSelect: false
```
```

---

## Patch 3: Update bug-fix-orchestrator.md

**File:** `.claude/agents/bug-fix-orchestrator.md` (if it exists, otherwise create based on bug-triage)

**Add to tools list:**
```yaml
tools: [Task, Read, Grep, Glob, Bash, Edit, Write, AskUserQuestion]
```

**Add instruction:**

```markdown
## Interactive Questions

If any spawned `bug-fixer` agent returns `status: needs_review`, use `AskUserQuestion` to present options to the user before continuing.

Example flow:
1. bug-fixer returns: `status: needs_review, reason: "Multiple possible fixes"`
2. Orchestrator asks user: "Bug #2 has multiple fixes. Which approach?"
3. User selects option
4. Re-spawn bug-fixer with user decision
```

---

## Patch 4: Update feature-planner.md

**File:** `.claude/agents/feature-planner.md`

**Add to tools list:**
```yaml
tools: [Read, Grep, Glob, Bash, AskUserQuestion]
```

**Add section:**

```markdown
## Clarifying Requirements

If the feature request is ambiguous, use `AskUserQuestion` BEFORE generating the plan:

```
AskUserQuestion:
  questions:
    - question: "The feature 'add chat' could mean several things. Which do you want?"
      header: "Clarify scope"
      options:
        - label: "Real-time chat between users"
          description: "WebSocket-based messaging between participants"
        - label: "AI chatbot assistant"
          description: "LLM-powered Q&A for users"
        - label: "Support chat widget"
          description: "Customer service chat integration"
      multiSelect: false
```
```

---

## Patch 5: Update CLAUDE.md

**File:** `.claude/CLAUDE.md`

**Add new section after "Never Break Orchestration":**

```markdown
## Interactive Questions for Blockers

Subagents should use `AskUserQuestion` (not just output text) when they hit blockers that require user decisions.

### Required Behavior

When a subagent encounters:
- HTTP 4xx/5xx errors that block progress
- Multiple valid implementation approaches
- Ambiguous requirements
- Breaking changes that need approval
- Missing dependencies or resources

**They MUST use `AskUserQuestion` with clear options**, not just output text.

### After User Answers

After user answers an interactive question:
1. The orchestrating agent continues with the user's decision
2. If the subagent already exited, main conversation re-spawns it with context

### Example - WRONG:
```
[bug-fixer] Found multiple root causes:
1. Null check missing
2. Race condition
Which should I fix?
```
(User sees this as text output, agent stops, no interaction)

### Example - CORRECT:
```
[bug-fixer] Found multiple root causes.
AskUserQuestion:
  questions:
    - question: "I found multiple root causes. Which should I fix?"
      header: "Bug fix"
      options:
        - label: "Fix null check"
          description: "..."
        - label: "Fix race condition"
          description: "..."
        - label: "Fix both"
          description: "..."
```
(User sees interactive buttons, can click to respond)
```

---

## Implementation Steps

1. **Add `AskUserQuestion` to these agent tool lists:**
   - `feature-implementor.md`
   - `bug-fixer.md`
   - `bug-triage.md` / `bug-fix-orchestrator.md`
   - `feature-planner.md`
   - `planning-council.md`

2. **Add the "Interactive User Questions" section to each agent** with:
   - When to ask (trigger conditions)
   - How to ask (example AskUserQuestion call)
   - What NOT to ask

3. **Update CLAUDE.md** with the global rules for interactive questions

4. **Test with a scenario** that would previously fail silently:
   ```
   /implement-feature "Add quiz chat endpoint"
   ```
   When it hits `400: Quiz must have at least one question`, it should now ask you what to do.

---

## Why This Works

The `AskUserQuestion` tool:
- Is available to subagents (it's a Claude Code capability)
- Renders as interactive buttons in the UI
- Pauses execution until user responds
- Returns the user's selection to the agent

This gives you control at decision points without needing to manually intervene.
