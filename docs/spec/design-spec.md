# Claude Autoresearch - Design Specification

## 1. Overview

Claude Autoresearch is an autonomous experimentation framework for Claude Code. It enables continuous, self-directed code improvement through a structured feedback loop: modify code → verify results → keep or discard → repeat.

Adapted from [codex-autoresearch](https://github.com/leo-lilinxiao/codex-autoresearch) for Claude Code's plugin architecture.

## 2. Goals

- Automate measurable code improvements (test coverage, type strictness, lint warnings, security findings, latency, custom metrics)
- Provide structured escalation when progress stalls
- Maintain full audit trail of every experiment
- Support session resume after interruption
- Require zero human intervention after launch

## 3. Architecture

### 3.1 Plugin Structure

Implemented as a Claude Code plugin with four subsystems:

| Subsystem | Purpose |
|---|---|
| **Skill (SKILL.md)** | Core protocol — governs Claude's behavior during the autonomous loop |
| **Scripts (Python)** | State management — results.tsv, state.json, lessons.md |
| **Hooks (hooks.json)** | Event monitoring — session resume, iteration tracking, stop prevention |
| **Command (autoresearch.md)** | Entry point — `/autoresearch` slash command |

### 3.2 Execution Model

Claude itself is the loop executor. Unlike the reference project (which spawns detached `codex exec` processes), Claude Code runs the loop directly in the current session. The Stop hook prevents premature exit.

**Foreground (primary)**: User invokes `/autoresearch` → interactive wizard → autonomous loop in current session.

**Background (stretch)**: Launch via `claude -p` in detached tmux session.

### 3.3 Core Loop

Each iteration follows this cycle:

```
Scan → Modify → Commit → Verify → Decide → Log → Escalate? → Repeat
```

1. **Scan**: Read state.json for current metric, goal, and strategy
2. **Modify**: Make one focused change using Edit/Write tools
3. **Commit**: `git add` + `git commit` the change
4. **Verify**: Run the user-defined verification command
5. **Decide**: Compare metric — keep (improvement ≥1%) or revert (`git revert`)
6. **Log**: Record iteration via `autoresearch_record_iteration.py`
7. **Escalate?**: Check consecutive failures against escalation ladder
8. **Repeat**: Continue to next iteration

### 3.4 Two-Phase Boundary

**Phase 1 — Interactive (before "go"):**
- Wizard scans repo, asks clarifying questions
- User approves goal, metric, verification command
- Progressive disclosure keeps entry simple

**Phase 2 — Autonomous (after "go"):**
- No further human input requested
- One focused change per iteration
- Mechanical verification only
- Full audit trail maintained

## 4. Operational Modes

### 4.1 Loop Mode (metric-driven)
Drive a measurable metric in a specified direction. Examples: "increase test coverage to 80%", "reduce lint warnings to zero".

### 4.2 Debug Mode (hypothesis-driven)
Evidence-based hypothesis testing for bugs. Each iteration: form hypothesis → test → confirm/reject → narrow scope.

### 4.3 Fix Mode (error-count-driven)
Iteratively reduce error count to zero. Each iteration targets one error, verifies the fix, moves to next.

## 5. Escalation Ladder

When progress stalls:

| Trigger | Action |
|---|---|
| 3 consecutive discards | **REFINE** — adjust approach within current strategy |
| 5 consecutive non-keeps | **PIVOT** — fundamentally different strategy |
| 2 PIVOTs without improvement | Search web for solutions |
| 3 PIVOTs without improvement | **STOP** — report to human |

## 6. State Management

### 6.1 Artifacts Directory

All run artifacts stored in `autoresearch-results/` (gitignored in target repo):

| File | Purpose |
|---|---|
| `results.tsv` | Iteration log with TSV header comments |
| `state.json` | Current state snapshot (metric, consecutive failures, pivot count) |
| `lessons.md` | Cross-run learnings and patterns |
| `context.json` | Hook context pointer for session resume |

### 6.2 State Schema (state.json)

```json
{
  "run_id": "string",
  "goal": "string",
  "metric_name": "string",
  "direction": "maximize|minimize",
  "verify_command": "string",
  "guard_command": "string|null",
  "current_metric": "number",
  "baseline_metric": "number",
  "iteration_count": "number",
  "consecutive_discards": "number",
  "pivot_count": "number",
  "status": "running|paused|completed|stopped",
  "last_updated": "ISO8601"
}
```

## 7. Hooks Design

### 7.1 SessionStart Hook
- Checks for active run in `autoresearch-results/state.json`
- If active: emits `additionalContext` with run state and resume instructions
- Enables seamless session resume after interruption

### 7.2 PostToolUse Hook (Bash)
- Monitors Bash tool calls during the loop
- Tracks iteration timing
- Detects stalls (same error pattern repeated)
- Emits warnings via `hookSpecificOutput`

### 7.3 Stop Hook
- Checks if autoresearch loop is active and goal not reached
- If so: returns non-zero exit to block premature stop
- Includes message instructing Claude to continue iterating

## 8. Context Management

Long autonomous loops will approach Claude's context limit. Mitigations:
- SKILL.md instructs Claude to use `/compact` every ~10 iterations
- After compaction, re-read SKILL.md protocol and state.json
- Lessons.md provides cross-compaction continuity

## 9. Security Considerations

- Verification commands run in user's shell with user's permissions
- No secrets or credentials stored in plugin files
- All paths use `${CLAUDE_PLUGIN_ROOT}` (no hardcoded absolute paths)
- Guard commands prevent regressions (e.g., existing tests must still pass)

## 10. Dependencies

- Python 3.8+ (for helper scripts)
- Git (for commit/revert operations)
- Claude Code CLI with plugin support
