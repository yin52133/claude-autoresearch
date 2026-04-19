# Debug Mode Workflow

Evidence-based hypothesis testing for bugs.

## When to Use

Use debug mode when the goal involves finding and fixing a specific bug or investigating unexpected behavior.

## Before Starting

1. Run the interaction wizard with the bug description as goal
2. Initialize in debug mode: add `--mode debug` flag conceptually (same init script, different mental model)
3. Confirm with user

## Core Protocol

### Each Iteration

```
Hypothesis → Test → Observe → Decide → Log → Repeat
```

### Step 1: Observe

Read the bug report or symptom description from state.json (goal field).

Gather evidence:
- Read relevant source files
- Run the failing code and capture the error
- Check logs, stack traces, or debugging output
- Identify the failure mode (crash, wrong output, hang, etc.)

### Step 2: Form Hypothesis

Based on evidence, form a specific, falsifiable hypothesis:
- "The bug is caused by X because Y"
- "The null check at line N is missing"
- "The cache returns stale data when TTL expires"

Make one hypothesis per iteration.

### Step 3: Test

Design a test that would fail if the hypothesis is wrong, and pass if the hypothesis is correct.

Run the test:
```bash
# Either modify existing test or write a new one
python3 -c "assert <hypothesis condition>"
```

### Step 4: Observe Result

- **Confirmed**: Hypothesis explains the bug → proceed to fix
- **Rejected**: Hypothesis is wrong → form new hypothesis
- **Partial**: Hypothesis is partially correct → refine

### Step 5: Fix (if confirmed)

Make the minimal change to fix the bug.

### Step 6: Verify

Run the verification command (the test suite or specific test for this bug).

### Step 7: Log

Record the iteration:
```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/autoresearch_record_iteration.py \
  --status keep|discard \
  --metric <1 if confirmed, 0 if not> \
  --commit <sha> \
  --description "<hypothesis>"
```

### Step 8: Repeat

If bug is fixed, run `autoresearch_state.py complete`.
If not, continue with next hypothesis.

## Escalation

Same ladder as loop mode, but with debug-specific meaning:
- 3 consecutive rejected hypotheses → refine (narrow scope, get more evidence)
- 5 non-confirmed → pivot (try different debugging strategy: binary search, rubber duck, etc.)
- 3 pivots → stop and report

## Termination

- Bug confirmed and fixed (verification passes)
- 3 pivots without resolution
- User interrupts
