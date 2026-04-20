#!/usr/bin/env python3
"""Stop hook: warn if autoresearch loop is active and goal not reached."""

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
    if status != "running":
        sys.exit(0)

    metric = state.get("metric_name", "?")
    current = state.get("current_metric", 0)
    baseline = state.get("baseline_metric", 0)
    iterations = state.get("iteration_count", 0)

    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
    scripts = f"{plugin_root}/scripts" if plugin_root else "scripts"
    sys.stderr.write(
        f"\n[autoresearch] Active run detected (iteration {iterations}).\n"
        f"[autoresearch] Current metric: {metric}={current} (baseline: {baseline}).\n"
        f"[autoresearch] To stop safely: PYTHONPATH={scripts} python3 {scripts}/autoresearch_state.py complete\n"
        f"[autoresearch] To pause: PYTHONPATH={scripts} python3 {scripts}/autoresearch_state.py pause\n"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
