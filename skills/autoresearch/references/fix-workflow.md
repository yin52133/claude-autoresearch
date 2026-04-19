# Fix Mode Workflow

Iteratively reduce error count to zero.

## When to Use

Use fix mode when the goal is to eliminate a class of errors: TypeScript errors, lint warnings, test failures, compiler errors.

## Core Protocol

```
Scan Errors → Prioritize → Fix One → Verify → Log → Repeat
```

## Each Iteration

### Step 1: Scan Errors

Run the verification command to get current error list. Note total count and specific errors.

### Step 2: Prioritize

Choose one error to fix. Priority:
1. Errors causing cascading failures
2. Errors in frequently-modified files
3. Errors quick to fix
4. Errors that unlock fixes for others

### Step 3: Fix

Make the minimal change to fix the chosen error.

### Step 4: Verify

Re-run the verification command. Capture the new error count.

### Step 5: Decide

- **Keep**: Error count decreased → commit the fix
- **Discard**: Error count unchanged or increased → revert, try different fix

### Step 6: Log

Record iteration. Metric = current error count (minimize).

### Step 7: Repeat

Continue until error count is 0.

## Escalation

Same ladder:
- 3 discards → refine
- 5 non-keeps → pivot
- 3 pivots → stop

## Termination

- Error count reaches 0
- 3 pivots without reaching 0
- User interrupts
