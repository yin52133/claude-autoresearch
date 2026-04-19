#!/usr/bin/env python3
"""Stop hook: prevent premature exit if autoresearch loop is active."""

import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PLUGIN_ROOT = SCRIPT_DIR.parent
STATE_PATH = PLUGIN_ROOT.parent / "autoresearch-results" / "state.json"


def main():
    if not STATE_PATH.exists():
        sys.exit(0)

    try:
        with open(STATE_PATH) as f:
            state = json.load(f)
    except (json.JSONDecodeError, IOError):
        sys.exit(0)

    status = state.get("status", "")
    if status != "running":
        sys.exit(0)

    metric = state.get("metric_name", "?")
    current = state.get("current_metric", 0)
    baseline = state.get("baseline_metric", 0)
    iterations = state.get("iteration_count", 0)

    sys.stderr.write(
        f"\n[autoresearch] Active run detected (iteration {iterations}).\n"
        f"[autoresearch] Current metric: {metric}={current} (baseline: {baseline}).\n"
        f"[autoresearch] To stop safely: run 'python3 {SCRIPT_DIR}/autoresearch_state.py complete'\n"
        f"[autoresearch] To pause: run 'python3 {SCRIPT_DIR}/autoresearch_state.py pause'\n"
    )
    # Return non-zero to block the stop, but let Claude decide
    sys.exit(0)


if __name__ == "__main__":
    main()
