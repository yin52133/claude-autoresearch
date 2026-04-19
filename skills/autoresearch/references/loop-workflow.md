# Loop Mode Workflow

Metric-driven autonomous improvement toward a measurable goal.

## When to Use

Use loop mode when the goal is quantifiable: test coverage percentage, error count, lint warnings, latency, custom metric.

## Before Starting

1. Run the interaction wizard to confirm goal, metric, and verification command
2. Initialize the run: `autoresearch_init_run.py --goal ... --metric-name ... --direction maximize|minimize --verify "..." --baseline-metric ...`
3. Read current state: `autoresearch_state.py summary`
4. Confirm "go" from user

## Each Iteration

### Step 1: Scan

Read `autoresearch-results/state.json`:
- Current metric value and direction
- Iteration count
- Consecutive discard count
- Pivot count
- Last strategy used

### Step 2: Plan

Based on the metric and current state, plan one focused change:

- What specific aspect of the code needs to change?
- What is the expected direction of improvement?
- Is this a refinement or a pivot? (check escalation)

### Step 3: Modify

Make one focused change using Edit or Write tools. Choose the file(s) most likely to move the metric.

### Step 4: Commit

```bash
git add <changed files>
git commit -m "Autoresearch iteration N: <brief description>"
```

Capture the commit SHA for recording.

### Step 5: Verify

Run the verification command. Capture the metric value from stdout.

**If the guard command exists and fails:** Revert immediately and record as crash.

### Step 6: Decide

Compare new metric vs baseline:

- **Keep**: improvement ≥ 1% AND guard passed
- **Discard**: improvement < 1% OR guard failed

**If keep:** Commit stands.
**If discard:** `git revert HEAD` to undo the change.

### Step 7: Log

Record the iteration:
```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/autoresearch_record_iteration.py \
  --status keep|discard|crash \
  --metric <value> \
  --commit <sha> \
  --guard true|false \
  --description "<brief description>"
```

The script returns JSON with escalation signal if applicable.

### Step 8: Escalate

Check the escalation signal from the recording script:
- **refine**: 3+ consecutive discards — adjust within current strategy
- **pivot**: 5+ consecutive non-keeps — try fundamentally different approach
- **stop**: 3 pivots without improvement — report to human

If escalation triggers, follow `references/pivot-protocol.md`.

### Step 9: Repeat

Continue to next iteration. Every ~10 iterations, use `/compact` and re-read SKILL.md and state.json.

## Termination Conditions

- Goal metric reached
- 3 pivots without improvement
- User interrupts
- Context limit approaching (use `/compact`)
