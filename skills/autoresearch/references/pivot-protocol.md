# Pivot Protocol — Escalation Ladder

What to do when the autonomous loop stalls.

## The Problem

The loop will sometimes hit a plateau where the current strategy stops producing improvements. This is expected — not every approach works. The escalation ladder provides a structured response.

## Escalation Levels

### Level 1: Continue (default)

Current strategy is working. No intervention needed.

- Metric is improving → keep iterating
- Consecutive discards < 3 → stay the course

### Level 2: Refine (3 consecutive discards)

Adjust within the current strategy.

**Trigger:** 3 consecutive discard iterations.

**What to do:**
1. Analyze what has been tried so far (read lessons.md)
2. Identify patterns that didn't work
3. Narrow the focus or try a more targeted approach
4. Explicitly log the refinement decision

**Examples:**
- "Too broad — targeting specific files instead of whole codebase"
- "Pattern not matching — trying regex approach instead"
- "Too aggressive — smaller incremental changes"

### Level 3: Pivot (5 consecutive non-keeps)

Fundamentally change strategy.

**Trigger:** 5 consecutive non-keep iterations (discard + refine + crash).

**What to do:**
1. Acknowledge the current approach has failed
2. Read lessons.md for patterns across all attempts
3. Propose a fundamentally different approach
4. Explicitly log the pivot with a clear rationale
5. Reset consecutive discard counter to 0

**Examples:**
- "Adding tests from scratch didn't work — try test-driven refactoring instead"
- "Inline changes too risky — try extraction and replacement"
- "Type annotations causing issues — try strict mode off approach"

### Level 4: Web Search (2 pivots without improvement)

Look for external solutions.

**Trigger:** 2 pivot cycles with no improvement recorded.

**What to do:**
1. Use web search to find solutions others have used for similar goals
2. Adapt known patterns to this codebase
3. Log the web search results

### Level 5: Stop (3 pivots without improvement)

Report to human.

**Trigger:** 3 pivot cycles with no improvement.

**What to do:**
1. Stop the autonomous loop
2. Generate a summary report:
   - Original goal
   - Total iterations attempted
   - Strategies tried (refine + pivot cycles)
   - Best metric achieved
   - Remaining gap
   - Suggested next steps for human
3. Save final state with `autoresearch_state.py complete`
4. Present the report to the user

## Pivot Count Tracking

The `state.json` tracks `pivot_count` and `consecutive_discards`:
- `consecutive_discards` resets on keep
- `pivot_count` increments on pivot and does not reset
- Stop is triggered when `pivot_count >= 3` and no net improvement

## Logging

Every escalation decision should be logged to `lessons.md`:
```
## Iteration N — ESCALATION: refine|pivot|stop
Reason: <why this escalation was triggered>
Decision: <what will change>
Previous approaches: <summary of what was tried>
```
