#!/usr/bin/env python3
"""Record an iteration result to results.tsv and update state.json."""

import argparse
import json
import sys
from autoresearch_core import (
    results_path, state_path,
    load_state, save_state,
    improvement, delta_value,
    fmt_delta, fmt_metric, iso_now,
    STATUS_KEEP, STATUS_DISCARD, STATUS_CRASH, STATUS_NOOP,
    STATUS_REFINE, STATUS_PIVOT, STATUS_SEARCH, STATUS_BLOCKED, STATUS_DRIFT,
    KEEP_STATUSES,
    REFINE_THRESHOLD, PIVOT_THRESHOLD, STOP_PIVOT_COUNT,
)


def main():
    parser = argparse.ArgumentParser(description="Record autoresearch iteration")
    parser.add_argument("--repo", default=".", help="Repository root path")
    parser.add_argument("--status", required=True,
                        choices=[STATUS_KEEP, STATUS_DISCARD, STATUS_CRASH,
                                 STATUS_NOOP, STATUS_REFINE, STATUS_PIVOT,
                                 STATUS_SEARCH, STATUS_BLOCKED, STATUS_DRIFT])
    parser.add_argument("--metric", type=float, required=True)
    parser.add_argument("--commit", default="-", help="Commit SHA")
    parser.add_argument("--guard", default="pass", help="Guard result (pass/fail/-)")
    parser.add_argument("--description", default="", help="Iteration description")
    args = parser.parse_args()

    state = load_state(args.repo)
    if not state:
        print("ERROR: No active run found", file=sys.stderr)
        sys.exit(1)

    cfg = state.get("config", {})
    st = state.get("state", {})
    direction = cfg.get("direction", "higher")
    baseline_metric = st.get("baseline_metric", 0)
    current_metric = st.get("current_metric", baseline_metric)

    now = iso_now()
    iteration = st.get("iteration", 0) + 1
    delta = delta_value(args.metric, current_metric)
    improved = improvement(args.metric, current_metric, direction)
    is_keep = args.status == STATUS_KEEP

    # Determine retained metric and update state
    if is_keep:
        retained_metric = args.metric
    else:
        retained_metric = current_metric

    # Update state
    st["iteration"] = iteration
    st["last_status"] = args.status
    st["last_trial_metric"] = args.metric
    st["last_trial_commit"] = args.commit

    if is_keep:
        st["keeps"] = st.get("keeps", 0) + 1
        st["current_metric"] = retained_metric
        st["last_commit"] = args.commit
        st["consecutive_discards"] = 0
        st["pivot_count"] = 0
        # Update best if improved over best
        best_metric = st.get("best_metric", baseline_metric)
        if improvement(args.metric, best_metric, direction):
            st["best_metric"] = args.metric
            st["best_iteration"] = iteration
    elif args.status == STATUS_DISCARD:
        st["discards"] = st.get("discards", 0) + 1
        st["consecutive_discards"] = st.get("consecutive_discards", 0) + 1
    elif args.status == STATUS_CRASH:
        st["crashes"] = st.get("crashes", 0) + 1
        st["consecutive_discards"] = st.get("consecutive_discards", 0) + 1
    elif args.status == STATUS_NOOP:
        st["no_ops"] = st.get("no_ops", 0) + 1
        st["consecutive_discards"] = st.get("consecutive_discards", 0) + 1
    elif args.status == STATUS_REFINE:
        st["consecutive_discards"] = st.get("consecutive_discards", 0) + 1
    elif args.status == STATUS_PIVOT:
        st["pivot_count"] = st.get("pivot_count", 0) + 1
    elif args.status == STATUS_BLOCKED:
        st["blocked"] = st.get("blocked", 0) + 1

    # Write TSV row
    row = "\t".join([
        str(iteration),
        args.commit,
        fmt_metric(args.metric),
        fmt_delta(delta),
        args.guard,
        args.status,
        args.description,
    ])
    with open(results_path(args.repo), "a") as f:
        f.write(row + "\n")

    st["updated_at"] = now
    save_state(state, args.repo)

    # Determine escalation
    escalation = None
    cd = st["consecutive_discards"]
    pc = st["pivot_count"]

    if args.status == STATUS_BLOCKED:
        escalation = "blocked"
    elif pc >= STOP_PIVOT_COUNT:
        escalation = "stop"
        st["status"] = "stopped"
        save_state(state, args.repo)
    elif cd >= PIVOT_THRESHOLD:
        escalation = "pivot"
    elif cd >= REFINE_THRESHOLD:
        escalation = "refine"

    output = {
        "iteration": iteration,
        "status": args.status,
        "metric": args.metric,
        "delta": round(delta, 4),
        "improved": improved,
        "retained_metric": retained_metric,
        "guard": args.guard,
        "keeps": st.get("keeps", 0),
        "discards": st.get("discards", 0),
        "crashes": st.get("crashes", 0),
        "consecutive_discards": cd,
        "pivot_count": pc,
        "best_metric": st.get("best_metric"),
        "best_iteration": st.get("best_iteration"),
    }
    if escalation:
        output["escalation"] = escalation

    print(json.dumps(output))


if __name__ == "__main__":
    main()
