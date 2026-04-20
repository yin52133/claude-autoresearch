#!/usr/bin/env python3
"""SessionStart hook: detect active run and emit resume context."""

import json
import os
import sys
from pathlib import Path


def _resolve_cwd_from_stdin() -> str | None:
    raw = sys.stdin.read().strip()
    if raw:
        try:
            payload = json.loads(raw)
            cwd = payload.get("cwd")
            if isinstance(cwd, str) and cwd:
                return cwd
        except (json.JSONDecodeError, TypeError):
            pass
    return None


def main():
    cwd = _resolve_cwd_from_stdin() or os.environ.get("PWD", ".")
    artifact_dir = Path(cwd) / "autoresearch-results"
    state_path = artifact_dir / "state.json"

    if not state_path.exists():
        sys.exit(0)

    try:
        with open(state_path) as f:
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

    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
    scripts = f"{plugin_root}/scripts" if plugin_root else "scripts"

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
        f"  PYTHONPATH={scripts} python3 {scripts}/autoresearch_state.py summary",
        "",
    ]

    print("\n".join(lines))
    sys.exit(0)


if __name__ == "__main__":
    main()
