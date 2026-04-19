# Lessons Protocol

Cross-run learning system. Extracts structured insights from completed iterations.

## When to Extract Lessons

### After Every Kept Iteration

Extract a positive lesson:
- What strategy worked?
- Why did it work?
- Is this generalizable?

### After Every PIVOT Decision

Extract a strategic lesson:
- What strategy family was abandoned?
- How many iterations were spent before pivoting?
- What signal triggered the pivot?

### At Run Completion

Extract a summary lesson:
- Best overall strategy family for this goal type
- Most common failure patterns
- Effective verify/guard combinations observed

## Lesson Structure

```markdown
### L-{N}: {title}
- **Strategy:** what was attempted
- **Outcome:** keep / discard / crash / pivot / summary
- **Insight:** what to do differently next time
- **Context:** goal, scope, metric at the time
- **Iteration:** {iteration-number}
- **Timestamp:** {ISO-8601 UTC}
```

## Reading Lessons

At run start (Phase 1: Read):
1. Check if `autoresearch-results/lessons.md` exists.
2. If it exists, read all entries.
3. During hypothesis generation, consult lessons:
   - Prefer strategies that succeeded in similar contexts
   - Avoid strategies that consistently failed
   - Adapt successful strategies from related goals

## Capacity Management

### Target: 50 Entries Maximum

1. Preserve every lesson from the current run verbatim.
2. Group 30+ day-old entries by normalized strategy family.
3. For families with 5+ eligible entries, replace with one consolidated `summary` lesson.
4. If older archive is still above 50 entries, roll up oldest entries into one historical summary.

## Writing Rules

- Create the lessons file at the end of the first iteration that produces a keep or pivot.
- Append after each qualifying event.
- Never commit the lessons file.
- If corrupted, rename with `.bak` suffix and start fresh.
