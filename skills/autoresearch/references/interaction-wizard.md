# Interaction Wizard

Structured setup flow before launching the autonomous loop.

## Purpose

The wizard ensures the goal is clear, measurable, and achievable before any autonomous action begins. This is the only phase that asks questions — everything after "go" is fully autonomous.

## Wizard Flow

### Step 1: Goal Confirmation

Ask: "What would you like to improve?"

Accept natural language. Parse the intent and classify into mode:
- Metric improvement → loop
- Bug investigation → debug
- Error elimination → fix

### Step 2: Scope Discovery

Scan the repository to understand the codebase:
- Language(s) and framework(s)
- Testing setup
- Linting/formatting configuration
- Key directories and files

### Step 3: Metric Definition

Confirm the metric:
- "What metric should I track to measure progress?"
- If not specified, suggest one based on the goal (e.g., test coverage for quality goals)

For the metric, determine:
- **Name**: human-readable identifier
- **Direction**: maximize or minimize
- **Current value**: measure the baseline
- **Verification command**: shell command that returns a numeric value
- **Guard command**: optional, a command that must always pass (e.g., existing test suite)

### Step 4: Baseline Measurement

Run the verification command to establish baseline:
```
<verify_command>
```
Baseline: `<value>`

Run the guard command if defined:
```
<guard_command>
```
Result: passed / failed (if failed, set baseline anyway but note the warning)

### Step 5: Strategy Preview

Briefly describe the approach:
- "I'll target `<metric>` by making small, verifiable changes"
- "Each iteration will: modify → verify → keep or discard → log"
- "I'll escalate if progress stalls (refine → pivot → stop)"

### Step 6: Confirmation

```
Ready to launch autonomous loop:
  Goal: <goal>
  Mode: <mode>
  Metric: <metric_name> (<direction>)
  Baseline: <baseline_value>
  Verify: <verify_command>
  Guard: <guard_command|not set>

Type "go" to start, or describe changes to the goal.
```

## After "Go"

1. Initialize the run with `autoresearch_init_run.py`
2. Read `references/loop-workflow.md` (or debug/fix)
3. Enter the autonomous loop — **never ask for approval again**
