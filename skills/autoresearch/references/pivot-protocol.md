# PIVOT / REFINE Decision Framework

Smart stuck recovery with a graduated escalation system.

## Definitions

- **REFINE:** Adjust within the current strategy. Change parameters, scope, or approach details without abandoning the overall direction.
- **PIVOT:** Abandon the current strategy entirely. Try a fundamentally different approach to the same goal.

## Escalation Ladder

### Level 1: REFINE (3 consecutive discards)

Trigger: 3 consecutive iterations with status `discard`, `crash`, or `no-op`.

Actions:
1. Re-read the last 10 results log entries.
2. Identify what is common across failed attempts.
3. Consult `autoresearch-results/lessons.md` for insights.
4. Generate a hypothesis that differs in at least one concrete dimension:
   - Different file within scope
   - Different technique
   - Different granularity
5. Log the decision as status `refine` in the results TSV.

### Level 2: PIVOT (5 consecutive non-keeps)

Trigger: 5 consecutive non-keep iterations since the last keep (refines count toward this).

Actions:
1. Re-read all in-scope files from scratch.
2. Re-read the original goal.
3. Review the entire results log for patterns.
4. Explicitly name the strategy being abandoned and why.
5. Choose a fundamentally different approach:
   - If previous attempts were incremental, try a structural change.
   - If previous attempts targeted one file, try a cross-file approach.
   - If previous attempts added code, try removing or simplifying.
   - If previous attempts were conservative, try a bolder change.
6. Consult lessons for successful strategies in different contexts.
7. Log the decision as status `pivot` in the results TSV.

### Level 3: Web Search (2 PIVOTs without improvement)

Trigger: 2 PIVOT decisions have been made since the last keep, with no improvement.

Actions:
1. Formulate a targeted search query based on the current blocker.
2. Follow `references/web-search-protocol.md` for search execution.
3. Treat search results as hypotheses — still verify mechanically.
4. Log as status `search` in the results TSV.

### Level 4: Soft Blocker (3 PIVOTs without improvement)

Trigger: 3 PIVOT decisions without any keep since the first pivot.

Actions:
1. Print a warning:
   ```
   [WARNING] 3 strategy pivots without improvement. The goal may require
   manual intervention, broader scope, or a different metric.
   Stopping and reporting a soft blocker.
   ```
2. Stop the current run.
3. Report that the next step likely needs human input.

## Counting Rules

| Status | Counts toward REFINE (3)? | Counts toward PIVOT (5)? | Resets counters? |
|--------|--------------------------|--------------------------|-----------------|
| `keep` | no | no | **yes — resets all** |
| `discard` | yes | yes | no |
| `crash` | yes | yes | no |
| `no-op` | yes | yes | no |
| `refine` | no (it IS the refine) | yes (counts as non-keep) | no |
| `pivot` | no (it IS the pivot) | no (it IS the pivot) | no |
| `search` | no (action, not outcome) | no | no |
| `drift` | no (environmental) | no | no |
| `baseline` | no | no | no |
| `blocked` | hard stop | hard stop | n/a |

## Integration with Lessons

After every PIVOT:
- Extract a lesson per `references/lessons-protocol.md`.
- Record which strategy family was abandoned and the iteration cost.

## Example

```
iteration	commit	metric	delta	guard	status	description
0	a1b2c3d	47	0	-	baseline	initial any count
1	b2c3d4e	41	-6	pass	keep	type-narrow auth module
2	c3d4e5f	43	+2	-	discard	generic wrapper attempt
3	d4e5f6a	45	+4	-	discard	broader type union
4	-	41	0	-	refine	[REFINE] shifting from auth to api layer
5	c3d4e5f	38	-3	pass	keep	narrow api response handlers
```
