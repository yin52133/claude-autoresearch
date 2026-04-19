#!/usr/bin/env python3
"""SessionStart hook: detect active run and emit resume context."""

import json
import os
import sys
from pathlib import Path

ARTIFACT_DIR = Path(os.environ.get("PWD", ".")) / "autoresearch-results"
STATE_PATH = ARTIFACT_DIR / "state.json"


def main():
    if not STATE_PATH.exists():
        sys.exit(0)

    try:
        with open(STATE_PATH) as f:
            state = json.load(f)
    except (json.JSONDecodeError, IOError):
        sys.exit(0)

    status = state.get("status", "")
    if status not in ("running", "paused"):
        sys.exit(0)

    baseline = state.get("baseline_metric", 0)
    current = state.get("current_metric", 0)
    direction = state.get("direction", "maximize")

    if baseline == 0:
        imp = "N/A"
    else:
        if direction == "maximize":
            imp_pct = ((current - baseline) / abs(baseline)) * 100
        else:
            imp_pct = ((baseline - current) / abs(baseline)) * 100
        imp = f"{imp_pct:.2f}%"

    lines = [
        "",
        "=== Autoresearch Active Run Detected ===",
        f"  Run ID: {state.get('run_id', '?')}",
        f"  Goal: {state.get('goal', '?')}",
        f"  Metric: {state.get('metric_name', '?')} = {current} (baseline: {baseline}, {imp})",
        f"  Iterations: {state.get('iteration_count', 0)}",
        f"  Status: {status}",
        f"  Consecutive discards: {state.get('consecutive_discards', 0)}",
        f"  Pivot count: {state.get('pivot_count', 0)}",
        "",
        "Use /autoresearch to continue the loop, or check with:",
        "  python3 ${CLAUDE_PLUGIN_ROOT}/scripts/autoresearch_state.py summary",
        "",
    ]

    print("\n".join(lines))
    sys.exit(0)


if __name__ == "__main__":
    main()
