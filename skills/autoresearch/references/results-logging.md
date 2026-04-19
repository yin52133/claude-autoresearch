# Results Logging

The authoritative contract for `results.tsv` and `state.json`.

## TSV Schema

```
# claude-autoresearch iteration log
# metric_direction: lower|higher
iteration	commit	metric	delta	guard	status	description
```

Columns:
- `iteration` — integer (0 = baseline, 1+ = iterations)
- `commit` — git commit SHA, or `-` for baseline/refine/pivot
- `metric` — current metric value
- `delta` — change vs previous retained metric (with `+` prefix for positive)
- `guard` — `pass`, `fail`, or `-`
- `status` — baseline/keep/discard/crash/no-op/refine/pivot/search/blocked/drift
- `description` — one-line summary of what was tried

## Delta Calculation

- `delta = current_metric - previous_retained_metric` (higher = positive)
- For direction `lower`, smaller is better (negative delta = improvement)
- For direction `higher`, larger is better (positive delta = improvement)

## State Schema (state.json)

```json
{
  "run_id": "string",
  "mode": "loop|debug|fix|...",
  "run_tag": "string|null",
  "config": {
    "session_mode": "foreground|background",
    "workspace_root": "/path/to/workspace",
    "goal": "string",
    "scope": "string",
    "metric": "string",
    "direction": "lower|higher",
    "verify": "string",
    "guard": "string|null",
    "verify_format": "scalar|metrics_json",
    "primary_metric_key": "string",
    "acceptance_criteria": [],
    "required_keep_criteria": []
  },
  "state": {
    "iteration": 0,
    "baseline_metric": 47,
    "best_metric": 47,
    "best_iteration": 0,
    "current_metric": 47,
    "last_commit": "-",
    "last_trial_commit": "-",
    "last_trial_metric": 47,
    "keeps": 0,
    "discards": 0,
    "crashes": 0,
    "no_ops": 0,
    "blocked": 0,
    "consecutive_discards": 0,
    "pivot_count": 0,
    "last_status": "baseline"
  },
  "updated_at": "ISO8601"
}
```

## Context File (context.json)

```json
{
  "run_id": "string",
  "artifact_dir": "/path/to/workspace/autoresearch-results",
  "last_activity": "ISO8601",
  "iteration_count": 0
}
```

## Write Protocol

Write state to a uniquely named temporary file in the same directory, then rename to `state.json` (atomic). Never commit the Results directory.
