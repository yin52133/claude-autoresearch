#!/usr/bin/env python3
"""PostToolUse hook: monitor iteration progress."""

import json
import os
import sys
from pathlib import Path
from datetime import datetime


def _resolve_artifact_dir() -> Path:
    raw = sys.stdin.read().strip()
    if raw:
        try:
            payload = json.loads(raw)
            cwd = payload.get("cwd")
            if isinstance(cwd, str) and cwd:
                return Path(cwd) / "autoresearch-results"
        except (json.JSONDecodeError, TypeError):
            pass
    return Path(os.environ.get("PWD", ".")) / "autoresearch-results"


def main():
    artifact_dir = _resolve_artifact_dir()
    state_path = artifact_dir / "state.json"
    context_path = artifact_dir / "context.json"

    if not state_path.exists():
        sys.exit(0)

    try:
        with open(state_path) as f:
            state = json.load(f)
    except (json.JSONDecodeError, IOError):
        sys.exit(0)

    if state.get("status") != "running":
        sys.exit(0)

    try:
        with open(context_path) as f:
            context = json.load(f)
    except (json.JSONDecodeError, IOError):
        context = {}

    context["last_activity"] = datetime.now().isoformat()
    context["iteration_count"] = state.get("iteration_count", 0)

    tmp = context_path.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(context, f, indent=2)
        f.write("\n")
    tmp.rename(context_path)

    sys.exit(0)


if __name__ == "__main__":
    main()
