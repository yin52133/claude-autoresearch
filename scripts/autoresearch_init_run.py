#!/usr/bin/env python3
"""Initialize an autoresearch run with baseline measurement."""

import argparse
import json
import uuid
from autoresearch_core import (
    artifact_dir, results_path, state_path, lessons_path, context_path,
    fmt_metric, iso_now, save_state,
)


def main():
    parser = argparse.ArgumentParser(description="Initialize autoresearch run")
    parser.add_argument("--repo", default=".", help="Repository root path")
    parser.add_argument("--goal", required=True, help="Improvement goal description")
    parser.add_argument("--scope", default="", help="Files/directories in scope")
    parser.add_argument("--metric-name", required=True, help="Name of the metric")
    parser.add_argument("--direction", choices=["lower", "higher"], required=True)
    parser.add_argument("--verify", required=True, help="Verification command")
    parser.add_argument("--guard", default="", help="Guard command (must pass)")
    parser.add_argument("--baseline-metric", type=float, required=True)
    parser.add_argument("--baseline-commit", default="", help="Baseline commit SHA")
    parser.add_argument("--run-tag", default="", help="Optional run tag")
    parser.add_argument("--session-mode", default="foreground", help="foreground or background")
    parser.add_argument("--iterations", type=int, default=0, help="Max iterations (0=unlimited)")
    args = parser.parse_args()

    adir = artifact_dir(args.repo)
    adir.mkdir(parents=True, exist_ok=True)

    run_id = uuid.uuid4().hex[:12]
    now = iso_now()

    with open(results_path(args.repo), "w") as f:
        f.write(f"# claude-autoresearch iteration log\n")
        f.write(f"# metric_direction: {args.direction}\n")
        f.write("\t".join(["iteration", "commit", "metric", "delta", "guard", "status", "description"]) + "\n")
        row = "\t".join([
            "0",
            args.baseline_commit or "-",
            fmt_metric(args.baseline_metric),
            "0",
            "-",
            "baseline",
            f"Initial baseline ({args.metric_name})",
        ])
        f.write(row + "\n")

    state = {
        "run_id": run_id,
        "mode": "loop",
        "run_tag": args.run_tag or None,
        "config": {
            "session_mode": args.session_mode,
            "workspace_root": str(adir.parent),
            "goal": args.goal,
            "scope": args.scope,
            "metric": args.metric_name,
            "direction": args.direction,
            "verify": args.verify,
            "guard": args.guard or None,
            "iterations": args.iterations,
            "verify_format": "scalar",
            "primary_metric_key": args.metric_name,
            "acceptance_criteria": [],
            "required_keep_criteria": [],
        },
        "state": {
            "iteration": 0,
            "baseline_metric": args.baseline_metric,
            "best_metric": args.baseline_metric,
            "best_iteration": 0,
            "current_metric": args.baseline_metric,
            "last_commit": args.baseline_commit or "-",
            "last_trial_commit": "-",
            "last_trial_metric": args.baseline_metric,
            "keeps": 0,
            "discards": 0,
            "crashes": 0,
            "no_ops": 0,
            "blocked": 0,
            "consecutive_discards": 0,
            "pivot_count": 0,
            "last_status": "baseline",
        },
        "updated_at": now,
    }
    save_state(state, args.repo)

    lp = lessons_path(args.repo)
    if not lp.exists():
        with open(lp, "w") as f:
            f.write(f"# Lessons — run {run_id}\n\n")

    cp = context_path(args.repo)
    with open(cp, "w") as f:
        json.dump({
            "run_id": run_id,
            "artifact_dir": str(adir),
        }, f, indent=2)
        f.write("\n")

    print(f"Initialized run {run_id} — baseline {args.metric_name}={fmt_metric(args.baseline_metric)} ({args.direction})")


if __name__ == "__main__":
    main()
