#!/usr/bin/env python3
"""Append or list lessons from autoresearch runs."""

import argparse
import json
import re
from pathlib import Path
from datetime import datetime


LESSONS_OUTCOMES = ("keep", "discard", "crash", "pivot", "summary")
REQUIRED_FIELDS = ("strategy", "outcome", "insight", "context", "iteration", "timestamp")


def lessons_path(repo_root=None):
    base = Path(repo_root) if repo_root else Path.cwd()
    return base / "autoresearch-results" / "lessons.md"


def utc_now():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def compact_text(value):
    return " ".join(str(value).split()).strip() or "-"


def append_lesson(lessons_path, title, strategy, outcome, insight, context, iteration):
    """Append a lesson entry to the lessons file."""
    lessons_path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = utc_now()

    entry = f"### L-?: {compact_text(title)}\n"
    entry += f"- **Strategy:** {compact_text(strategy)}\n"
    entry += f"- **Outcome:** {outcome}\n"
    entry += f"- **Insight:** {compact_text(insight)}\n"
    entry += f"- **Context:** {compact_text(context)}\n"
    entry += f"- **Iteration:** {compact_text(iteration)}\n"
    entry += f"- **Timestamp:** {timestamp}\n\n"

    with open(lessons_path, "a") as f:
        f.write(entry)

    return {
        "lessons_path": str(lessons_path),
        "title": compact_text(title),
        "outcome": outcome,
        "timestamp": timestamp,
    }


def list_lessons(lessons_path):
    """List all lesson entries."""
    if not lessons_path.exists():
        return []

    entries = []
    current = None

    header_re = re.compile(r"^### L-(\d+):\s*(.+)$")
    field_re = re.compile(r"^- \*\*(Strategy|Outcome|Insight|Context|Iteration|Timestamp):\*\* (.+)$")
    field_map = {
        "Strategy": "strategy",
        "Outcome": "outcome",
        "Insight": "insight",
        "Context": "context",
        "Iteration": "iteration",
        "Timestamp": "timestamp",
    }

    for line in lessons_path.read_text(encoding="utf-8").splitlines():
        line = line.rstrip()
        if not line:
            continue
        m = header_re.match(line)
        if m:
            if current:
                entries.append(current)
            current = {"id": f"L-{m.group(1)}", "title": m.group(2).strip()}
            continue
        m = field_re.match(line)
        if m and current:
            current[field_map[m.group(1)]] = m.group(2).strip()

    if current:
        entries.append(current)

    return entries


def main():
    parser = argparse.ArgumentParser(description="Manage autoresearch lessons")
    sub = parser.add_subparsers(dest="command", required=True)

    append_p = sub.add_parser("append")
    append_p.add_argument("--repo", default=".")
    append_p.add_argument("--title", required=True)
    append_p.add_argument("--strategy", required=True)
    append_p.add_argument("--outcome", required=True, choices=LESSONS_OUTCOMES)
    append_p.add_argument("--insight", required=True)
    append_p.add_argument("--context", default="-")
    append_p.add_argument("--iteration", default="-")

    list_p = sub.add_parser("list")
    list_p.add_argument("--repo", default=".")

    args = parser.parse_args()

    lp = lessons_path(args.repo)

    if args.command == "append":
        if args.outcome not in LESSONS_OUTCOMES:
            print(f"ERROR: outcome must be one of {LESSONS_OUTCOMES}", file=__import__('sys').stderr)
            return 1
        result = append_lesson(
            lessons_path=lp,
            title=args.title,
            strategy=args.strategy,
            outcome=args.outcome,
            insight=args.insight,
            context=args.context,
            iteration=args.iteration,
        )
        print(json.dumps(result, indent=2))

    elif args.command == "list":
        entries = list_lessons(lp)
        print(json.dumps(entries, indent=2))

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
