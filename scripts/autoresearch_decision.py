#!/usr/bin/env python3
"""Evaluate mechanical keep/discard/trial decisions for autoresearch."""

import argparse
import json


def derive_trial_status(direction, current_metric, trial_metric, guard="pass", crashed=False):
    """Determine status based on trial metric, direction, and guard."""
    if crashed:
        return {
            "status": "crash",
            "trial_metric": float(trial_metric),
            "retained_metric": float(current_metric),
            "improved": False,
            "guard": guard,
        }
    if guard == "fail":
        status = "discard"
    else:
        if direction == "lower":
            improved = float(trial_metric) < float(current_metric)
        elif direction == "higher":
            improved = float(trial_metric) > float(current_metric)
        else:
            improved = False
        status = "keep" if improved else "discard"
    retained = trial_metric if status == "keep" else current_metric
    return {
        "status": status,
        "trial_metric": float(trial_metric),
        "retained_metric": float(retained),
        "improved": status == "keep",
        "guard": guard,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate mechanical keep/discard/crash decisions."
    )
    parser.add_argument("--direction", required=True, choices=["lower", "higher"])
    parser.add_argument("--current-metric", required=True, type=float)
    parser.add_argument("--trial-metric", required=True, type=float)
    parser.add_argument("--guard", default="pass",
                        help="Guard result: pass (default), fail, or - (no guard)")
    parser.add_argument("--crashed", action="store_true",
                        help="Treat as crash regardless of metric")
    args = parser.parse_args()

    result = derive_trial_status(
        direction=args.direction,
        current_metric=args.current_metric,
        trial_metric=args.trial_metric,
        guard=args.guard,
        crashed=args.crashed,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
