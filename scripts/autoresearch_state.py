#!/usr/bin/env python3
"""State management for autoresearch runs."""

import argparse
import json
import sys
from autoresearch_core import load_state, save_state, improvement, fmt_metric


def main():
    parser = argparse.ArgumentParser(description="Autoresearch state management")
    parser.add_argument("--repo", default=".", help="Repository root path")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("check", help="Check if an active run exists")
    sub.add_parser("summary", help="JSON summary of current state")
    sub.add_parser("pause", help="Pause the current run")
    sub.add_parser("resume", help="Resume a paused run")
    sub.add_parser("complete", help="Mark run as completed")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    state = load_state(args.repo)

    if args.command == "check":
        if state and state.get("status") in ("running", "paused"):
            print("active")
            sys.exit(0)
        else:
            print("inactive")
            sys.exit(1)

    elif args.command == "summary":
        if not state:
            print("{}")
            sys.exit(0)
        imp = improvement(
            state["baseline_metric"],
            state["current_metric"],
            state["direction"],
        )
        summary = {
            "run_id": state["run_id"],
            "goal": state["goal"],
            "metric_name": state["metric_name"],
            "direction": state["direction"],
            "baseline": state["baseline_metric"],
            "current": state["current_metric"],
            "improvement_pct": round(imp, 2),
            "iteration_count": state["iteration_count"],
            "consecutive_discards": state["consecutive_discards"],
            "pivot_count": state["pivot_count"],
            "status": state["status"],
        }
        print(json.dumps(summary, indent=2))

    elif args.command == "pause":
        if not state:
            print("ERROR: No active run", file=sys.stderr)
            sys.exit(1)
        state["status"] = "paused"
        save_state(state, args.repo)
        print("Run paused")

    elif args.command == "resume":
        if not state:
            print("ERROR: No run found", file=sys.stderr)
            sys.exit(1)
        state["status"] = "running"
        save_state(state, args.repo)
        print("Run resumed")

    elif args.command == "complete":
        if not state:
            print("ERROR: No run found", file=sys.stderr)
            sys.exit(1)
        state["status"] = "completed"
        save_state(state, args.repo)
        imp = improvement(
            state["baseline_metric"],
            state["current_metric"],
            state["direction"],
        )
        print(f"Run completed — {state['metric_name']}: "
              f"{fmt_metric(state['baseline_metric'])} → "
              f"{fmt_metric(state['current_metric'])} "
              f"({fmt_metric(imp)}% improvement)")


if __name__ == "__main__":
    main()
