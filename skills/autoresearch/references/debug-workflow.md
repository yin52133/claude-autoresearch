# Debug Mode Workflow

Evidence-based hypothesis testing for bugs.

## When to Use

Use debug mode when the goal involves finding and fixing a specific bug or investigating unexpected behavior.

## Core Protocol

```
Observe → Form Hypothesis → Test → Observe Result → Fix (if confirmed) → Verify → Log → Repeat
```

## Each Iteration

### Step 1: Observe

Gather evidence:
- Read relevant source files
- Run the failing code and capture the error
- Check logs, stack traces
- Identify the failure mode (crash, wrong output, hang)

### Step 2: Form Hypothesis

Form a specific, falsifiable hypothesis:
- "The bug is caused by X because Y"
- "The null check at line N is missing"
- "The cache returns stale data when TTL expires"

Make one hypothesis per iteration.

### Step 3: Test

Design a test that would fail if the hypothesis is wrong and pass if correct.

### Step 4: Observe Result

- **Confirmed**: Hypothesis explains the bug → proceed to fix
- **Rejected**: Hypothesis is wrong → form new hypothesis
- **Partial**: Hypothesis partially correct → refine

### Step 5: Fix (if confirmed)

Make the minimal change to fix the bug.

### Step 6: Verify

Run the verification command.

### Step 7: Log

Record the iteration. Metric is binary: 1 if confirmed and fixed, 0 if not.

### Step 8: Repeat

If bug is fixed, complete. If not, continue with next hypothesis.

## Escalation

Same ladder:
- 3 consecutive rejected hypotheses → refine
- 5 non-confirmed → pivot (try different debugging strategy)
- 3 pivots → stop and report

## Termination

- Bug confirmed and fixed
- 3 pivots without resolution
- User interrupts
