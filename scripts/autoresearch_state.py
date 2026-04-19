#!/usr/bin/env python3
"""State management for autoresearch runs."""

import argparse
import json
import sys
from pathlib import Path
from autoresearch_core import (
    load_state, save_state, improvement,
    fmt_metric, iso_now, state_path,
)


def main():
    parser = argparse.ArgumentParser(description="Autoresearch state management")
    parser.add_argument("--repo", default=".", help="Repository root path")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("check", help="Check if an active run exists")
    p = sub.add_parser("summary", help="JSON summary of current state")
    p.add_argument("--json", action="store_true", help="Raw JSON output")
    sub.add_parser("pause", help="Pause the current run")
    sub.add_parser("resume", help="Resume a paused run")
    sub.add_parser("complete", help="Mark run as completed")
    sub.add_parser("stop", help="Stop the current run")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    state = load_state(args.repo)

    if args.command == "check":
        if state and state.get("state", {}).get("iteration", 0) >= 0:
            last_status = state.get("state", {}).get("last_status", "")
            if last_status in ("baseline", "running", "keep", "discard", "crash", "refine", "pivot"):
                print("active")
                sys.exit(0)
            print("inactive")
            sys.exit(1)
        print("inactive")
        sys.exit(1)

    elif args.command == "summary":
        if not state:
            print("{}")
            sys.exit(0)
        st = state.get("state", {})
        cfg = state.get("config", {})
        baseline = st.get("baseline_metric", 0)
        current = st.get("current_metric", 0)
        best = st.get("best_metric", 0)
        direction = cfg.get("direction", "higher")
        delta = current - baseline
        imp = ((current - baseline) / abs(baseline) * 100) if baseline else 0

        summary = {
            "run_id": state.get("run_id"),
            "goal": cfg.get("goal"),
            "metric": cfg.get("metric"),
            "direction": direction,
            "baseline_metric": baseline,
            "current_metric": current,
            "best_metric": best,
            "best_iteration": st.get("best_iteration", 0),
            "improvement": f"{imp:.2f}%" if baseline else "N/A",
            "delta": f"{delta:+.4f}".rstrip("0").rstrip("."),
            "iteration": st.get("iteration", 0),
            "keeps": st.get("keeps", 0),
            "discards": st.get("discards", 0),
            "crashes": st.get("crashes", 0),
            "consecutive_discards": st.get("consecutive_discards", 0),
            "pivot_count": st.get("pivot_count", 0),
            "last_status": st.get("last_status"),
            "session_mode": cfg.get("session_mode"),
            "status": state.get("state", {}).get("last_status", "unknown"),
        }
        if hasattr(args, "json") and args.json:
            print(json.dumps(state, indent=2))
        else:
            print(json.dumps(summary, indent=2))

    elif args.command == "pause":
        if not state:
            print("ERROR: No active run", file=sys.stderr)
            sys.exit(1)
        state["state"]["last_status"] = "paused"
        state["updated_at"] = iso_now()
        save_state(state, args.repo)
        print("Run paused")

    elif args.command == "resume":
        if not state:
            print("ERROR: No run found", file=sys.stderr)
            sys.exit(1)
        state["state"]["last_status"] = "running"
        state["updated_at"] = iso_now()
        save_state(state, args.repo)
        print("Run resumed")

    elif args.command in ("complete", "stop"):
        if not state:
            print("ERROR: No run found", file=sys.stderr)
            sys.exit(1)
        st = state.get("state", {})
        cfg = state.get("config", {})
        baseline = st.get("baseline_metric", 0)
        current = st.get("current_metric", 0)
        best = st.get("best_metric", 0)
        direction = cfg.get("direction", "higher")
        improved = improvement(current, baseline, direction)
        st["last_status"] = "completed"
        state["updated_at"] = iso_now()
        save_state(state, args.repo)
        reason = "goal reached" if improved else "no improvement"
        print(f"Run {args.command} — {cfg.get('metric', 'metric')}: "
              f"{fmt_metric(baseline)} → {fmt_metric(best)} "
              f"({'+' if improved else ''}{fmt_metric(current - baseline)}, improved={improved})")
        print(f"Result: {reason}")
        print(f"Total: {st.get('iteration', 0)} iterations, "
              f"{st.get('keeps', 0)} keeps, {st.get('discards', 0)} discards, "
              f"{st.get('crashes', 0)} crashes")


if __name__ == "__main__":
    main()
