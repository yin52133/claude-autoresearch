---
name: autoresearch
description: "Autonomous goal-driven experimentation for Claude Code. Use when the user wants Claude to plan or run an unattended improve-verify loop toward a measurable or verifiable outcome. Covers loop, debug, fix, and more. Do not use for ordinary one-shot coding help."
metadata:
  short-description: "Run an unattended improve-verify loop"
---

# Autoresearch

An autonomous goal-driven experimentation framework. Tell it what to improve, then walk away — it modifies code, verifies results, keeps or discards changes, and repeats.

## When Activated

1. Classify the request as `loop`, `debug`, `fix`, `security`, `ship`, `plan`, or `exec`.
2. Load `references/core-principles.md` and `references/structured-output-spec.md`. For active execution modes (`loop`, `debug`, `fix`, `security`, `ship`, `exec`), also load `references/runtime-hard-invariants.md`.
3. Load only additional references the current situation needs:
   - `references/session-resume-protocol.md` when resuming or controlling an existing run
   - `references/interaction-wizard.md` for every new interactive launch before execution begins
   - `references/results-logging.md` only when debugging TSV/state semantics
4. Load the selected mode workflow reference plus cross-cutting protocols as needed (`lessons`, `pivot`, `health-check`, `web-search`, `hypothesis-perspectives`).
5. Use bundled helper scripts for stateful artifacts and runtime control. Resolve the scripts path once at the start of each run:
   - If `$CLAUDE_PLUGIN_ROOT` is set: `SCRIPTS="${CLAUDE_PLUGIN_ROOT}/scripts"`
   - Otherwise, find the cached plugin: `SCRIPTS=$(ls -d ~/.claude/plugins/cache/local/claude-autoresearch/*/scripts 2>/dev/null | tail -1)`
   - Always set `PYTHONPATH=$SCRIPTS` when calling helper scripts so cross-imports work.
6. Execute the selected workflow exactly as written and produce required structured output and artifacts.

## Core Loop

```
Read → Baseline → Ideate → Modify → Commit → Verify → Guard → Decide → Log → Health Check → Re-anchor → Repeat
```

## Modes

| Mode | Purpose | Primary Reference |
|------|---------|-------------------|
| `loop` | Autonomous metric-driven improvement | `references/loop-workflow.md` |
| `plan` | Convert vague goal into launch-ready config | `references/plan-workflow.md` |
| `debug` | Hunt bugs with evidence and hypotheses | `references/debug-workflow.md` |
| `fix` | Iteratively reduce errors to zero | `references/fix-workflow.md` |
| `security` | Structured security audit | `references/security-workflow.md` |
| `ship` | Gate and execute ship workflow | `references/ship-workflow.md` |
| `exec` | Non-interactive CI/CD with JSON output | `references/exec-workflow.md` |

## Required Config

For loop mode, infer these from natural language input and repo context:

- `Goal` — what to improve
- `Scope` — files/directories in scope
- `Metric` — measurable indicator
- `Direction` — `lower` or `higher`
- `Verify` — shell command that returns a numeric metric value

Optional but recommended:
- `Guard` — regression test command (must pass)
- `Iterations` — max iterations (default: unlimited)
- `Run tag` — identifier for this run
- `Stop condition` — when to stop
- `Verify format` — `scalar` (default) or `metrics_json`
- `Primary metric key` — for JSON verify format
- `Acceptance criteria` — multi-metric success thresholds
- `Required keep criteria` — hard gates for every kept result
- `Rollback policy` — `revert` (default) or `reset` (destructive)

For every new interactive run, use the wizard contract in `references/interaction-wizard.md`.

## Run Modes

**Foreground:** Keep the loop in the current Claude session. Use helper scripts directly. No launch manifest created.

**Background:** Launch via `claude -p` in a detached session. A launcher script persists the confirmed config and starts the background loop. (Stretch goal — implement foreground first.)

**Run mode selection:** The interaction wizard MUST ask the user to choose foreground or background before launch. Both are mutually exclusive for a given workspace/run.

## Explicit Entry Points

- `/autoresearch` — primary entry point for interactive runs
- For `status` or `stop` requests, stay on the same skill entry
- `exec` mode is fully configured upfront with no launch questions

## Hard Rules

**1. Ask before act for new interactive launches.**
For `loop`, `debug`, `fix`, `security`, and `ship`, ALWAYS scan the repo and ask at least one round of clarifying questions before the run starts. Load and follow `references/interaction-wizard.md` for every new interactive launch. The launch wizard must include an explicit run-mode choice: foreground or background. `exec` mode is the exception — fully configured upfront.

**2. Respect the chosen run mode after launch approval.**
Once the user says "go" (or "start", "launch"), follow the selected run mode exactly. Foreground stays in the current session. Background persists the confirmed config and starts the detached loop. After launch, NEVER pause to ask anything — not for clarification, not for confirmation, not for permission.

**3. Never ask after the user approves the run.**
If you encounter ambiguity during the loop, apply best practices and keep going. The user may be asleep.

**4. Read all in-scope files before the first write.**

**5. One focused change per iteration.**

**6. Mechanical verification only.**
Run the verify command; interpret results objectively. No subjective judgment.

**7. Commit before verification only when every managed repo's worktree stays within declared scope or autoresearch-owned artifacts.**

**8. Never stage or revert unrelated user changes.**

**9. Keep run artifacts uncommitted and never stage them.**
The following are experiment-owned artifacts:
- `autoresearch-results/results.tsv`
- `autoresearch-results/state.json`
- `autoresearch-results/context.json`
- `autoresearch-results/lessons.md`
- `autoresearch-results/launch.json` (background only)
- `autoresearch-results/runtime.json` (background only)
- `autoresearch-results/runtime.log` (background only)

**10. Use the rollback strategy approved during setup.**
In a dedicated experiment branch/worktree with pre-launch approval, `git reset --hard HEAD~1` is allowed. Otherwise use `git revert --no-edit HEAD`.

**11. Discard gains under 1% that add disproportionate complexity.**

**12. Unlimited runs by default unless the user explicitly asks for `Iterations: N`.**
The iteration cap, if set, is a terminal condition.

**13. External ship actions (deploy, publish, release) must be confirmed during the pre-launch wizard phase.**

**14. Do not ask "should I continue?" during the loop.**
Do not pause between iterations. Once launched, after each iteration is logged, immediately begin the next iteration cycle. The helper output includes `"next_action": "BEGIN_NEXT_ITERATION"` — treat it as a mandatory directive. Keep the chosen run mode active until interrupted or a hard blocker appears.

**15. During active execution, keep `references/runtime-hard-invariants.md` as the primary runtime checklist.**
Foreground persistent artifacts: `results.tsv`, `state.json`, `context.json`, `lessons.md`. Background also uses `launch.json`, `runtime.json`, `runtime.log`.

**16. When stuck (3+ consecutive discards), use the PIVOT/REFINE escalation ladder from `references/pivot-protocol.md`.**

**17. Prefer the bundled helper scripts over hand-editing artifacts.**
Always call them via `${SCRIPTS}` (resolved at run start; see rule 5).

**18. In `exec` mode, never leave repo-root state artifacts behind.**
Use exec scratch path and clean up before exit.

**19. After any context compaction event, re-read `references/runtime-hard-invariants.md`, `references/core-principles.md`, and the selected mode workflow from disk before the next iteration.**

**20. Every 10 iterations, perform the Protocol Fingerprint Check from `references/runtime-hard-invariants.md`.**
If any item fails, re-read all loaded runtime docs from disk before continuing.

## Structured Output

Every mode should follow `references/structured-output-spec.md`.

Minimum requirement:
- Setup summary before the loop starts
- Progress updates during the loop
- Completion summary at the end
- For `exec`, emit only machine-readable JSON payloads

## Quick Start

```
/autoresearch increase test coverage to 80%
/autoresearch eliminate all TypeScript any types
/autoresearch reduce lint warnings to zero
/autoresearch fix the memory leak in the cache module
```

Claude scans the repo, asks targeted questions, asks to choose foreground or background, then starts the loop.

## Helper Scripts

All scripts require `PYTHONPATH=${SCRIPTS}` and are called as `PYTHONPATH=${SCRIPTS} python3 ${SCRIPTS}/<script>`.

| Script | CLI Usage |
|--------|-----------|
| `autoresearch_init_run.py` | `--repo <path> --goal "..." --metric-name "..." --direction lower\|higher --verify "..." --baseline-metric <N>` |
| `autoresearch_record_iteration.py` | `--repo <path> --status keep\|discard\|crash\|no-op\|refine\|pivot\|search\|blocked\|drift --metric <N> [--commit <sha>] [--guard pass\|fail] [--description "..."]` |
| `autoresearch_state.py` | `[--repo <path>] check\|summary\|pause\|resume\|complete\|stop` |
| `autoresearch_decision.py` | Evaluate keep/discard/trial decisions |
| `autoresearch_lessons.py` | `append\|list [--repo <path>] [--lesson "..."]` |
| `autoresearch_session_start.py` | (hook only) |
| `autoresearch_stop_check.py` | (hook only) |
| `autoresearch_hooks_monitor.py` | (hook only) |

## References

- `references/core-principles.md`
- `references/runtime-hard-invariants.md`
- `references/loop-workflow.md`
- `references/autonomous-loop-protocol.md`
- `references/interaction-wizard.md`
- `references/structured-output-spec.md`
- `references/modes.md`
- `references/plan-workflow.md`
- `references/debug-workflow.md`
- `references/fix-workflow.md`
- `references/security-workflow.md`
- `references/ship-workflow.md`
- `references/exec-workflow.md`
- `references/results-logging.md`
- `references/lessons-protocol.md`
- `references/pivot-protocol.md`
- `references/web-search-protocol.md`
- `references/environment-awareness.md`
- `references/parallel-experiments-protocol.md`
- `references/session-resume-protocol.md`
- `references/health-check-protocol.md`
- `references/hypothesis-perspectives.md`
