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

TSV_HEADER_COMMENT = (
    "# claude-autoresearch iteration log\n"
    "# Each row records one experiment iteration\n"
)
TSV_COLUMNS = [
    "iteration",
    "timestamp",
    "status",
    "metric_value",
    "improvement_pct",
    "commit_sha",
    "guard_passed",
    "description",
]
TSV_HEADER = "\t".join(TSV_COLUMNS)

STATUS_KEEP = "keep"
STATUS_DISCARD = "discard"
STATUS_CRASH = "crash"
STATUS_NOOP = "no-op"
STATUS_REFINE = "refine"
STATUS_PIVOT = "pivot"
STATUS_BASELINE = "baseline"

KEEP_STATUSES = {STATUS_KEEP, STATUS_BASELINE}

REFINE_THRESHOLD = 3
PIVOT_THRESHOLD = 5
STOP_PIVOT_COUNT = 3
MIN_IMPROVEMENT_PCT = 1.0


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


def improvement(baseline: float, current: float, direction: str) -> float:
    if baseline == 0:
        return 0.0 if current == 0 else 100.0
    if direction == "maximize":
        return ((current - baseline) / abs(baseline)) * 100
    else:
        return ((baseline - current) / abs(baseline)) * 100


def fmt_metric(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return f"{value:.4f}".rstrip("0").rstrip(".")


def iso_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())


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
