#!/usr/bin/env python3
"""PostToolUse hook: monitor iteration progress and detect stalls."""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

SCRIPT_DIR = Path(__file__).parent
PLUGIN_ROOT = SCRIPT_DIR.parent
STATE_PATH = PLUGIN_ROOT.parent / "autoresearch-results" / "state.json"
CONTEXT_PATH = PLUGIN_ROOT.parent / "autoresearch-results" / "context.json"


def main():
    # Read state
    if not STATE_PATH.exists():
        sys.exit(0)

    try:
        with open(STATE_PATH) as f:
            state = json.load(f)
    except (json.JSONDecodeError, IOError):
        sys.exit(0)

    if state.get("status") != "running":
        sys.exit(0)

    # Update last activity time in context
    try:
        with open(CONTEXT_PATH) as f:
            context = json.load(f)
    except (json.JSONDecodeError, IOError):
        context = {}

    context["last_activity"] = datetime.now().isoformat()
    context["iteration_count"] = state.get("iteration_count", 0)

    # Write back
    tmp = CONTEXT_PATH.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(context, f, indent=2)
        f.write("\n")
    tmp.rename(CONTEXT_PATH)

    sys.exit(0)


if __name__ == "__main__":
    main()
