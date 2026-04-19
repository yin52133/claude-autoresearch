# Plan Mode

Convert a vague goal into a launch-ready configuration without editing code.

## When to Use

Use plan mode when:
- The user has a fuzzy goal ("make it faster", "clean this up")
- The user wants to review the proposed approach before committing
- The user wants to understand the scope and metric before starting

## Workflow

1. Scan the repo thoroughly
2. Ask clarifying questions about scope, metric, and constraints
3. Generate a detailed configuration proposal:
   - Goal (refined from vague input)
   - Scope (files/directories)
   - Metric (specific, measurable)
   - Direction (lower/higher)
   - Verify command
   - Guard command (if needed)
   - Estimated iteration count or unbounded
   - Rollback strategy
4. Present the plan in structured format
5. Ask if the user wants to proceed (launch) or modify the plan

## Output

- Structured text plan with all config fields
- No code changes made
- No artifacts created
- User can approve to launch or request changes

## Example

```
/autoresearch plan make the API faster
```

Claude produces a full launch config, user reviews and approves, then the loop starts.
