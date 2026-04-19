#!/usr/bin/env python3
"""Initialize an autoresearch run with baseline measurement."""

import argparse
import sys
import uuid
from autoresearch_core import (
    artifact_dir, results_path, state_path, lessons_path, context_path,
    TSV_HEADER_COMMENT, TSV_HEADER, STATUS_BASELINE, fmt_metric, iso_now,
    save_state,
)


def main():
    parser = argparse.ArgumentParser(description="Initialize autoresearch run")
    parser.add_argument("--repo", default=".", help="Repository root path")
    parser.add_argument("--goal", required=True, help="Improvement goal description")
    parser.add_argument("--scope", default="", help="Files/directories in scope")
    parser.add_argument("--metric-name", required=True, help="Name of the metric")
    parser.add_argument("--direction", choices=["maximize", "minimize"], required=True)
    parser.add_argument("--verify", required=True, help="Verification command")
    parser.add_argument("--guard", default="", help="Guard command (must pass)")
    parser.add_argument("--baseline-metric", type=float, required=True)
    parser.add_argument("--baseline-commit", default="", help="Baseline commit SHA")
    parser.add_argument("--baseline-description", default="Initial baseline")
    args = parser.parse_args()

    adir = artifact_dir(args.repo)
    adir.mkdir(parents=True, exist_ok=True)

    run_id = uuid.uuid4().hex[:12]
    now = iso_now()

    with open(results_path(args.repo), "w") as f:
        f.write(TSV_HEADER_COMMENT)
        f.write(TSV_HEADER + "\n")
        row = "\t".join([
            "0",
            now,
            STATUS_BASELINE,
            fmt_metric(args.baseline_metric),
            "0",
            args.baseline_commit,
            "true",
            args.baseline_description,
        ])
        f.write(row + "\n")

    state = {
        "run_id": run_id,
        "goal": args.goal,
        "scope": args.scope,
        "metric_name": args.metric_name,
        "direction": args.direction,
        "verify_command": args.verify,
        "guard_command": args.guard,
        "current_metric": args.baseline_metric,
        "baseline_metric": args.baseline_metric,
        "iteration_count": 0,
        "consecutive_discards": 0,
        "pivot_count": 0,
        "status": "running",
        "last_updated": now,
    }
    save_state(state, args.repo)

    lp = lessons_path(args.repo)
    if not lp.exists():
        with open(lp, "w") as f:
            f.write(f"# Lessons — run {run_id}\n\n")

    cp = context_path(args.repo)
    with open(cp, "w") as f:
        import json
        json.dump({"run_id": run_id, "artifact_dir": str(adir)}, f, indent=2)
        f.write("\n")

    print(f"Initialized run {run_id} — baseline {args.metric_name}={fmt_metric(args.baseline_metric)}")


if __name__ == "__main__":
    main()
