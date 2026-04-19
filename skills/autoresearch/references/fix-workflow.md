# Fix Mode Workflow

Iteratively reduce error count to zero.

## When to Use

Use fix mode when the goal is to eliminate a class of errors: TypeScript errors, lint warnings, test failures, compiler errors, etc.

## Before Starting

1. Run the interaction wizard with error elimination as goal
2. Define the metric: error count (minimize to 0)
3. Define the verification command: returns the current error count
4. Confirm baseline error count
5. Confirm "go"

## Core Protocol

### Each Iteration

```
Scan Errors → Prioritize → Fix One → Verify → Log → Repeat
```

### Step 1: Scan Errors

Run the verification command to get current error list:
```
<verify_command>
```

Note the total count and the specific errors.

### Step 2: Prioritize

Choose one error to fix. Priority order:
1. Errors that cause cascading failures
2. Errors in frequently-modified files
3. Errors that are quick to fix
4. Errors that, once fixed, unlock fixes for others

### Step 3: Fix

Make the minimal change to fix the chosen error.

### Step 4: Verify

Re-run the verification command:
```
<verify_command>
```

Capture the new error count.

### Step 5: Decide

- **Keep**: Error count decreased → commit the fix
- **Discard**: Error count unchanged or increased → revert, try a different fix

### Step 6: Log

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/autoresearch_record_iteration.py \
  --status keep|discard \
  --metric <new_error_count> \
  --commit <sha> \
  --description "<fixed error type>"
```

### Step 7: Repeat

Continue until error count is 0.

## Escalation

Same ladder:
- 3 discards in a row → refine (find easier errors to start with)
- 5 non-keeps → pivot (try different error-fixing strategy)
- 3 pivots → stop

## Termination

- Error count reaches 0
- 3 pivots without reaching 0
- User interrupts
