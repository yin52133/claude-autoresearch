# Autonomous Loop Protocol

Detailed reference for the generic research loop. During active execution, keep `runtime-hard-invariants.md` plus the selected mode workflow in memory first. Use this file when you need the full setup, recovery, artifact, or escalation details.

## Loop Modes

- `unbounded`: default. If the user does not specify `Iterations`, keep iterating until interrupted or another terminal condition is reached.
- `bounded`: when the user explicitly sets `Iterations: N`.

## Required Inputs

Before entering the loop, confirm these are known:
- `Goal`, `Scope`, `Metric`, `Direction`, `Verify`

Optional:
- `Guard`, `Iterations`, `Run tag`, `Stop condition`
- `Verify format` — `scalar` (default) or `metrics_json`
- `Primary metric key` — for JSON verify format
- `Acceptance criteria` — multi-metric success thresholds
- `Required keep criteria` — hard gates for every kept result
- `Rollback policy` — `revert` (default) or `reset` (destructive)

## Phase 0: Preconditions

### Session Resume Check

Check for a prior interrupted run per `session-resume-protocol.md`:
1. Resolve current run through git-local pointer and `autoresearch-results/context.json`
2. Check `autoresearch-results/state.json` first (primary recovery source)
3. Apply the Recovery Priority Matrix:
   - JSON valid + TSV consistent -> full resume (skip wizard)
   - JSON valid + TSV inconsistent -> mini-wizard (1 round)
   - JSON missing + TSV exists -> TSV fallback (reconstruct state, confirm)
   - JSON corrupt -> rename to `.bak`, fall back to TSV
4. If no prior run is detected, proceed with fresh setup.

### Run Artifact Initialization

Do not create `autoresearch-results/results.tsv` or `autoresearch-results/state.json` before the baseline metric is known. After baseline is established, initialize with:
```
PYTHONPATH=${SCRIPTS} python3 ${SCRIPTS}/autoresearch_init_run.py --repo <repo> --goal "..." --metric-name "..." --direction lower|higher --verify "..." --baseline-metric <value>
```

### Ask-Before-Act

Before starting any interactive loop, ALWAYS:
1. Scan the repo to understand context.
2. Ask at least one round of clarifying questions.
3. Present a plain-language summary for the user to approve.
4. Require an explicit run-mode choice: **foreground** or **background**.
5. Only start the loop after the user says "go" / "start" / "launch".

**Two-phase boundary:** All questions happen BEFORE launch. After "go", never pause to ask anything.

### Safety Checks

1. Confirm the repo is under git if the workflow depends on commits.
2. Inspect `git status --porcelain`.
3. If unrelated user changes are present, do not start the commit/revert loop.
4. Confirm the scope resolves to real files.
5. Confirm the verify command exists and is plausible.
6. If a guard exists, confirm it is pass/fail.
7. If destructive rollback may be needed, get approval during setup.

### Dirty Worktree Rule

If `git status --porcelain` is non-empty during Phase 0:
- If the only changes are autoresearch-owned artifacts, continue.
- Otherwise ask the user during the wizard phase.
If the worktree becomes dirty after launch, log a hard blocker and stop the loop. Do not ask.

## Phase 1: Read

Before the first edit:
1. Read all in-scope files.
2. Read configuration or build files that influence verification.
3. Read the latest results log if one exists.
4. Read recent git history relevant to scoped files.
5. Read `autoresearch-results/lessons.md` if it exists.

Before every later iteration:
1. Re-read the changed files.
2. Read the last 10-20 results rows.
3. Read recent commits or diffs to avoid repeating bad ideas.
4. Consult lessons for relevant insights on the current strategy direction.

## Phase 2: Baseline

Run the verify command on the current state before making changes. Record baseline metric, guard result, current commit hash. Initialize run artifacts immediately after baseline is known.

## Phase 3: Ideate

Choose one concrete hypothesis. Filter against environment constraints. Apply multi-perspective reasoning:
- **Optimist:** most impactful change?
- **Skeptic:** why might this fail?
- **Historian:** what do past results and lessons say?
- **Minimalist:** simpler version possible?

Good hypotheses:
- "Reduce retries from 5 to 2 to lower latency without changing behavior."
- "Add tests for uncovered auth edge cases to raise coverage."

Bad hypotheses:
- "Refactor several modules and see what happens."
- "Clean things up."

Priority order:
1. stabilize flaky setup
2. exploit the last successful direction
3. try an untested idea informed by lessons
4. simplify while preserving the metric
5. attempt a larger directional change when small ideas stall

## Phase 4: Modify

Make one focused change within scope. The change should fit in one sentence. Do not broaden scope mid-iteration.

## Phase 5: Commit

```bash
git add -- <scoped-files>
git diff --cached --name-only
git commit -m "experiment: <what changed and why>"
```

Rules:
- stage only files owned by the experiment
- never stage autoresearch-owned artifacts
- inspect the staged file list before committing
- if there is no diff, log `no-op` and move on

Commit failure:
- "nothing to commit" -> treat as `no-op`
- transient git error -> retry once
- persistent failure or hook rejection -> treat as `crash`

## Phase 6: Verify

Run the mechanical verify command. Capture metric value, relevant output excerpt, wall clock duration, crash signal if any.

Metric parsing:
- if `verify_format=scalar`, the final non-empty verify output line must be a single numeric scalar
- if `verify_format=metrics_json`, follow the JSON contract in `results-logging.md`
- if verify output is unparseable, rerun once only; if still unparseable, treat as `crash`

Timeout: if verification takes more than 2x the established baseline time, treat as a failed iteration.

## Phase 6.5: Guard

Guard is a separate gate from Verify, not part of it. Sequence: Verify -> Guard -> Decide.

If guard fails:
1. revert the experiment
2. log the result as discarded
3. optionally attempt up to 2 reworks if the failure is clearly fixable

## Phase 7: Decide

### Keep
- metric improved in the requested direction
- guard passed or no guard exists
- complexity cost is justified

### Discard
- metric stayed flat or regressed
- guard failed
- change added too much complexity for too little gain

Simplicity Override:
- Marginal improvement (< 1%) + significant complexity increase = discard
- Metric unchanged but code becomes simpler = keep

Rollback follows the strategy approved during setup:
- `reset`: `git reset --hard HEAD~1` (only with pre-approved destructive rollback)
- `revert`: `git revert --no-edit HEAD` (default)

### Crash
If the run crashes:
1. inspect the error
2. fix trivial mistakes if the hypothesis is still valid
3. retry at most 3 quick times
4. otherwise revert and log `crash`

## Phase 8: Log

Always log:
- iteration number
- commit hash or `-`
- metric
- delta vs retained metric
- guard outcome
- status
- one-line description

Use `autoresearch_record_iteration.py` for authoritative updates:
```
PYTHONPATH=${SCRIPTS} python3 ${SCRIPTS}/autoresearch_record_iteration.py \
  --repo <repo> --status keep|discard|crash|no-op|refine|pivot|search|blocked|drift \
  --metric <value> [--commit <sha>] [--guard pass|fail] [--description "one-line note"]
```

## Phase 8.5: Health Check

Run per `health-check-protocol.md`. Check disk space, git state, verify command existence, log integrity.

## Phase 8.7: Protocol Re-Anchoring

Run the Protocol Fingerprint Check when:
- `iteration % 10 == 0`
- A context compaction warning was observed since the last check
- Claude cannot recall a runtime checklist item

If any fingerprint item fails:
1. Re-read `runtime-hard-invariants.md`, `core-principles.md`, and the selected mode workflow from disk
2. In the next TSV row's description, include the `[RE-ANCHOR]` tag
3. Continue the loop

Compaction counter:
- 0 compactions: check every 10 iterations
- 1 compaction: check every 5 iterations
- 2+ compactions: check every iteration until stability returns

## Phase 9: Repeat

**This is a hard loop. After logging, you MUST return to Phase 1 immediately.**

For bounded runs: stop after `Iterations` completes or earlier if goal is achieved.

For unbounded runs:
- NEVER ask "should I continue?" after launch. The user may be asleep.
- NEVER pause to ask any question during the loop. If something is unclear, apply best practices and keep going.
- NEVER stop to summarize progress between iterations. The results log IS the summary.
- Continue until goal reached, user interrupts, iteration cap reached, true blocker appears, or soft-blocker handoff.
- If you run out of obvious ideas, revisit the results log for patterns, try combinations, or attempt bolder changes. Pausing to ask is not an option.
- **After this phase completes, return to Phase 1 (Read) NOW. Do not output any text between Phase 9 and the next Phase 1.**

### PIVOT / REFINE Stuck Recovery

Replace simple "5 discards -> re-read" with the graduated escalation system:
- **3 consecutive discards -> REFINE:** Adjust within current strategy. Consult lessons, change parameters, log as `refine`.
- **5 consecutive non-keeps -> PIVOT:** Abandon current strategy entirely. Re-read everything, choose fundamentally different approach, log as `pivot`.
- **2 PIVOTs without improvement -> Web Search:** Escalate per `web-search-protocol.md`, log as `search`.
- **3 PIVOTs without improvement -> Soft Blocker:** Print warning, stop, report that human review is needed.

A single `keep` resets all escalation counters to zero.

### Lessons Extraction

After every `keep` and every `pivot`, extract a lesson per `lessons-protocol.md`.

## Progress Reporting

Every 5 iterations and at completion, summarize:
- baseline vs best metric
- keep/discard/crash counts
- the last few statuses
- the next likely direction

## Stop Conditions

Hard blockers (stop immediately):
- verify command no longer exists
- scope files deleted externally
- git repository broken
- disk space exhausted
- same crash 5+ times with no variation
- repo not safe for iterative commits
- verification cannot produce a mechanical metric
- user interrupts

On hard blocker, log with status `blocked` and stop. Do not ask.
