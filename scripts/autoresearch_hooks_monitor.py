#!/usr/bin/env python3
"""PostToolUse hook: monitor iteration progress."""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

ARTIFACT_DIR = Path(os.environ.get("PWD", ".")) / "autoresearch-results"
STATE_PATH = ARTIFACT_DIR / "state.json"
CONTEXT_PATH = ARTIFACT_DIR / "context.json"


def main():
    if not STATE_PATH.exists():
        sys.exit(0)

    try:
        with open(STATE_PATH) as f:
            state = json.load(f)
    except (json.JSONDecodeError, IOError):
        sys.exit(0)

    if state.get("status") != "running":
        sys.exit(0)

    try:
        with open(CONTEXT_PATH) as f:
            context = json.load(f)
    except (json.JSONDecodeError, IOError):
        context = {}

    context["last_activity"] = datetime.now().isoformat()
    context["iteration_count"] = state.get("iteration_count", 0)

    tmp = CONTEXT_PATH.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(context, f, indent=2)
        f.write("\n")
    tmp.rename(CONTEXT_PATH)

    sys.exit(0)


if __name__ == "__main__":
    main()
