# Autoresearch Skill

An autonomous goal-driven experimentation framework for Claude Code. Port of [codex-autoresearch](https://github.com/leo-lilinxiao/codex-autoresearch).

## Activation

Invoke via `/autoresearch` or when the user asks to improve code autonomously.

## What It Does

Given a measurable improvement goal, this skill drives an autonomous feedback loop:

```
Scan → Modify → Commit → Verify → Decide → Log → Escalate? → Repeat
```

Each iteration makes one focused change, verifies it, keeps or discards based on measurable results, and repeats.

## Modes

Choose the appropriate mode based on the goal type:

| Mode | Trigger | Example |
|---|---|---|
| **loop** | Metric improvement | "increase test coverage to 80%" |
| **debug** | Bug investigation | "fix the memory leak in the cache" |
| **fix** | Error elimination | "eliminate all TypeScript errors" |

## Hard Rules

1. **Ask before act, never ask after "go"** — The interactive wizard confirms the goal before launch. After launch, never prompt for approval.
2. **One change per iteration** — High signal-to-noise; makes verification clean.
3. **Mechanical verification only** — Run the verification command; interpret results objectively. No subjective judgment.
4. **Keep improvements ≥1%, discard smaller ones** — Small gains that add complexity are not worth it.
5. **Guard commands must always pass** — Existing tests or lint must continue to pass.
6. **Escalate when stuck** — Refine after 3 discards, pivot after 5, stop after 3 pivots.
7. **Log every iteration** — Use `autoresearch_record_iteration.py` after each iteration.
8. **Compact context periodically** — Use `/compact` every ~10 iterations to prevent context exhaustion.
9. **After compaction, re-read protocol** — Read SKILL.md and state.json to restore context.

## Interaction Wizard

When first activated, run the interaction wizard:

1. Scan the repository to understand structure
2. Confirm the improvement goal
3. Identify or define the measurable metric
4. Define the verification command (must return a numeric value)
5. Define the guard command (optional, must pass for all iterations)
6. Confirm baseline measurement
7. Confirm launch

See `references/interaction-wizard.md` for the full wizard protocol.

## Core Loop Protocol

For **loop mode**, follow `references/loop-workflow.md`.
For **debug mode**, follow `references/debug-workflow.md`.
For **fix mode**, follow `references/fix-workflow.md`.

## Escalation

See `references/pivot-protocol.md` for the full escalation ladder.

## State Management

Helper scripts (use `${CLAUDE_PLUGIN_ROOT}/scripts/`):

- `autoresearch_init_run.py --goal ... --metric-name ... --direction ... --verify ... --baseline-metric ...` — Initialize run
- `autoresearch_record_iteration.py --status keep|discard|crash|no-op|refine|pivot --metric ... --commit ... --description ...` — Record iteration
- `autoresearch_state.py check|summary|pause|resume|complete` — Manage state

## Results

All artifacts are stored in `autoresearch-results/` (gitignored):

- `results.tsv` — Iteration log
- `state.json` — Current state snapshot
- `lessons.md` — Cross-run learnings
- `context.json` — Hook context

## Runtime Invariants

Before every iteration, verify the invariants in `references/runtime-invariants.md`.
