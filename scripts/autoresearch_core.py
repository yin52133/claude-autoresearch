#!/usr/bin/env python3
"""Core constants, types, and utilities for claude-autoresearch."""

import os
import json
import time
from pathlib import Path
from typing import Optional

ARTIFACT_DIR_NAME = "autoresearch-results"
RESULTS_FILE_NAME = "results.tsv"
STATE_FILE_NAME = "state.json"
LESSONS_FILE_NAME = "lessons.md"
CONTEXT_FILE_NAME = "context.json"

TSV_COLUMNS = [
    "iteration",
    "commit",
    "metric",
    "delta",
    "guard",
    "status",
    "description",
]

STATUS_BASELINE = "baseline"
STATUS_KEEP = "keep"
STATUS_DISCARD = "discard"
STATUS_CRASH = "crash"
STATUS_NOOP = "no-op"
STATUS_REFINE = "refine"
STATUS_PIVOT = "pivot"
STATUS_SEARCH = "search"
STATUS_BLOCKED = "blocked"
STATUS_DRIFT = "drift"

KEEP_STATUSES = {STATUS_KEEP, STATUS_BASELINE}
NON_KEEP_STATUSES = {STATUS_DISCARD, STATUS_CRASH, STATUS_NOOP, STATUS_REFINE}

REFINE_THRESHOLD = 3
PIVOT_THRESHOLD = 5
STOP_PIVOT_COUNT = 3
MIN_IMPROVEMENT_PCT = 1.0
COMPACTION_INTERVAL = 10


def artifact_dir(repo_root: Optional[str] = None) -> Path:
    base = Path(repo_root) if repo_root else Path.cwd()
    return base / ARTIFACT_DIR_NAME


def results_path(repo_root: Optional[str] = None) -> Path:
    return artifact_dir(repo_root) / RESULTS_FILE_NAME


def state_path(repo_root: Optional[str] = None) -> Path:
    return artifact_dir(repo_root) / STATE_FILE_NAME


def lessons_path(repo_root: Optional[str] = None) -> Path:
    return artifact_dir(repo_root) / LESSONS_FILE_NAME


def context_path(repo_root: Optional[str] = None) -> Path:
    return artifact_dir(repo_root) / CONTEXT_FILE_NAME


def improvement(current: float, baseline: float, direction: str) -> bool:
    """Return True if current is an improvement over baseline per direction."""
    if direction == "higher":
        return current > baseline
    elif direction == "lower":
        return current < baseline
    else:
        raise ValueError(f"direction must be 'lower' or 'higher', got: {direction}")


def delta_value(current: float, previous: float) -> float:
    """Return delta (current - previous)."""
    return current - previous


def improvement_pct(baseline: float, current: float) -> float:
    if baseline == 0:
        return 0.0 if current == 0 else 100.0
    return ((current - baseline) / abs(baseline)) * 100


def fmt_delta(delta: float) -> str:
    text = f"{delta:.4f}".rstrip("0").rstrip(".")
    if delta > 0 and not text.startswith("+"):
        return f"+{text}"
    return text


def fmt_metric(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return f"{value:.4f}".rstrip("0").rstrip(".")


def iso_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())


def utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S+0000", time.gmtime())


def load_state(repo_root: Optional[str] = None) -> Optional[dict]:
    sp = state_path(repo_root)
    if not sp.exists():
        return None
    with open(sp) as f:
        return json.load(f)


def save_state(state: dict, repo_root: Optional[str] = None) -> None:
    sp = state_path(repo_root)
    sp.parent.mkdir(parents=True, exist_ok=True)
    tmp = sp.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
        f.write("\n")
    tmp.rename(sp)
