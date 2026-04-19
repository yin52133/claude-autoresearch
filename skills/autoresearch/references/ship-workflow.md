# Ship Workflow

Gate and execute pre-launch readiness workflows.

## When to Use

Use ship mode for:
- Pre-deployment checklist validation
- Release readiness checks
- CI/CD gate automation

## Workflow

### Phase 1: Define Checklist

Identify what needs to pass:
- All tests green
- Lint/formatting passes
- Security scan passes
- Documentation updated
- Version bumped

### Phase 2: Measure Readiness

Run verification command that emits a readiness score:
```
<check_script> --format=score
```

### Phase 3: Iterate

For each failing checklist item:
1. Fix the item
2. Re-run verification
3. Log the result
4. Continue until readiness score reaches 1.0 (100%)

### Phase 4: Ship

Once all checks pass:
- Dry run: show what would happen
- Direct: execute the deployment/release
- Monitor: watch for issues post-launch

## Verification

The verify command returns a score between 0 and 1:
- 1.0 = all checks passed, ready to ship
- 0.75 = mostly ready, X items pending
- 0.0 = far from ready

## Stop Conditions

- Readiness score reaches 1.0
- User interrupts
- Hard blocker (security issue, data integrity risk)
