#!/usr/bin/env python3
"""Record an iteration result to results.tsv and update state.json."""

import argparse
import sys
from autoresearch_core import (
    results_path, state_path, lessons_path,
    load_state, save_state, improvement, fmt_metric, iso_now,
    STATUS_KEEP, STATUS_DISCARD, STATUS_CRASH, STATUS_NOOP,
    STATUS_REFINE, STATUS_PIVOT, KEEP_STATUSES,
    REFINE_THRESHOLD, PIVOT_THRESHOLD, STOP_PIVOT_COUNT,
)


def main():
    parser = argparse.ArgumentParser(description="Record autoresearch iteration")
    parser.add_argument("--repo", default=".", help="Repository root path")
    parser.add_argument("--status", required=True,
                        choices=[STATUS_KEEP, STATUS_DISCARD, STATUS_CRASH,
                                 STATUS_NOOP, STATUS_REFINE, STATUS_PIVOT])
    parser.add_argument("--metric", type=float, required=True)
    parser.add_argument("--commit", default="", help="Commit SHA")
    parser.add_argument("--guard", default="true", help="Guard result (true/false)")
    parser.add_argument("--description", default="", help="Iteration description")
    args = parser.parse_args()

    state = load_state(args.repo)
    if not state:
        print("ERROR: No active run found", file=sys.stderr)
        sys.exit(1)

    now = iso_now()
    iteration = state["iteration_count"] + 1
    imp = improvement(state["baseline_metric"], args.metric, state["direction"])

    row = "\t".join([
        str(iteration),
        now,
        args.status,
        fmt_metric(args.metric),
        fmt_metric(imp),
        args.commit,
        args.guard,
        args.description,
    ])

    with open(results_path(args.repo), "a") as f:
        f.write(row + "\n")

    state["iteration_count"] = iteration
    state["current_metric"] = args.metric
    state["last_updated"] = now

    if args.status in KEEP_STATUSES:
        state["consecutive_discards"] = 0
    else:
        state["consecutive_discards"] = state.get("consecutive_discards", 0) + 1

    if args.status == STATUS_PIVOT:
        state["pivot_count"] = state.get("pivot_count", 0) + 1

    escalation = None
    cd = state["consecutive_discards"]
    pc = state["pivot_count"]

    if pc >= STOP_PIVOT_COUNT:
        escalation = "stop"
        state["status"] = "stopped"
    elif cd >= PIVOT_THRESHOLD:
        escalation = "pivot"
    elif cd >= REFINE_THRESHOLD:
        escalation = "refine"

    save_state(state, args.repo)

    output = {
        "iteration": iteration,
        "status": args.status,
        "metric": args.metric,
        "improvement_pct": round(imp, 2),
        "consecutive_discards": state["consecutive_discards"],
        "pivot_count": state["pivot_count"],
    }
    if escalation:
        output["escalation"] = escalation

    import json
    print(json.dumps(output))


if __name__ == "__main__":
    main()
