# Exec Mode

Non-interactive CI/CD mode with JSON-only output.

## When to Use

Use exec mode for:
- CI/CD pipeline integration
- Automated quality gates
- Batch processing without human interaction

## Differences from Interactive Modes

- No wizard — all config must be provided at invocation
- JSON-only output — no human-readable text
- No session resume — always starts fresh
- No lessons extraction
- Strict exit codes

## Invocation

All fields provided in the prompt or environment:

```
Goal: eliminate TypeScript any types
Scope: src/**/*.ts
Metric: any_count
Direction: lower
Verify: grep -r ":\s*any" src/ --include="*.ts" | wc -l
Guard: tsc --noEmit
Iterations: 50
```

## Output Format

Per-iteration line (stdout):
```json
{"iteration": 1, "commit": "abc1234", "metric": 41, "delta": -6, "guard": "pass", "status": "keep", "description": "narrowed auth types"}
```

Completion summary (stdout, last line):
```json
{"status": "completed", "baseline": 47, "best": 38, "best_iteration": 5, "total_iterations": 10, "keeps": 4, "discards": 5, "crashes": 1, "improved": true, "exit_code": 0}
```

Error output (stderr):
```json
{"error": "missing required field: Verify", "exit_code": 2}
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Run completed with improvement |
| 1 | Run completed, no improvement |
| 2 | Hard blocker (missing/invalid config) |

## State Management

Exec mode uses scratch state under `/tmp/claude-autoresearch-exec/`. State must be cleaned up before exit.
