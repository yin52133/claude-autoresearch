# Runtime Invariants

Checklist to verify before every iteration.

## Pre-Iteration Checklist

Run through this checklist before starting each iteration:

### State

- [ ] `autoresearch-results/state.json` exists
- [ ] Run status is "running"
- [ ] Current metric is recorded
- [ ] Iteration count is correct

### Context

- [ ] Goal is clear and measurable
- [ ] Verification command is known and runnable
- [ ] Baseline metric is established

### Strategy

- [ ] One focused change planned
- [ ] Expected metric direction is understood
- [ ] This is a continue / refine / pivot based on escalation

### Safety

- [ ] Guard command will be run after the change
- [ ] Revert plan exists if the change breaks things
- [ ] Change is scoped to minimize blast radius

## Escalation Signals

Watch for these signals that escalation is near:

| Signal | Meaning | Action |
|---|---|---|
| 2 consecutive discards | Running low on current strategy | Prepare for refine |
| 3 consecutive discards | Must refine now | Adjust approach |
| 4 consecutive non-keeps | Prepare for pivot | Start thinking alternatives |
| 5 consecutive non-keeps | Must pivot now | New strategy required |

## Context Compaction

When to trigger `/compact`:

- Every 10 iterations
- When consecutive_discards reaches 2
- When context is more than 50% full
- Before a pivot

After compaction:
1. Re-read SKILL.md
2. Re-read `references/pivot-protocol.md` (if escalating)
3. Re-read `autoresearch-results/state.json`
4. Re-read `autoresearch-results/lessons.md`
5. Continue from step 1 of the appropriate workflow
