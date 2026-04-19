# Interaction Wizard Contract

How to collect missing information before launching an autoresearch run. The user says one sentence. Claude figures out the rest through guided conversation. The user should never need to know field names or write config.

## Global Rules

1. Accept natural language input. The user's first message may be as short as "improve my test coverage".
2. Scan the repo before asking anything — read directory structure, key config files, scripts, and code.
3. ALWAYS ask at least one round of clarifying questions, even when all fields seem inferable.
4. Guide through conversation. Ask one question at a time (or batch tightly related ones).
5. Propose concrete defaults with every question.
6. Aim to finish clarification in 1 to 3 rounds. Never exceed 5 rounds.
7. Present a structured confirmation summary before launching.
8. The mandatory confirmation round must never collapse into a bare "foreground/background + go" prompt.
9. The user should never see raw field names. Translate everything into natural conversation.
10. After the user approves the summary, follow the chosen run mode directly. Foreground stays in the current session; background persists the config and starts the detached loop.
11. End the confirmation summary with a short runtime checklist: baseline first, then initialize artifacts, always log a completed experiment before the next one starts.

## Clarification Protocol

### Step 1: Scan

Read the repo — source files, config files, test suites, build systems, etc. Check manifest files (`package.json`, `requirements.txt`, `pyproject.toml`, `go.mod`) to understand the stack.

### Step 2: Guided Questions (MANDATORY — at least 1 round)

ALWAYS ask at least one round. Use the question guide below to pick the shortest useful set.

| What you need | Bad (skipping) | Good (confirming) |
|---------------|----------------|-------------------|
| Scope | Silently pick src/ | "I see `src/models/` and `src/api/` — should I touch the model layer only, or the whole src?" |
| Metric | Silently pick line coverage | "Your test suite reports line coverage (currently 58%). Track that, or care more about branch coverage?" |
| Target | Assume "as high as possible" | "Coverage is at 58% now. Target — 80%? 90%? Or push as high as I can?" |
| Verify command | Silently pick pytest | "I can run `pytest --cov=src` to measure coverage. Different runner?" |
| Guard | Skip it | "Should I make sure `npm test` still passes after each change?" |
| Duration | Assume unlimited | "Want me to run 10 iterations as a test, or keep iterating until you interrupt me?" |

Rules:
- Each round must add new information. Never ask the same question twice.
- Prefer multiple-choice questions over open-ended ones.
- If the goal is still unclear after 3 rounds, propose the most reasonable interpretation.
- When the user explicitly describes multiple goals, suggest multi-metric tracking with a primary metric.

### Step 3: Confirm (Structured Format)

Before launching, present a structured confirmation summary.

#### English Format

```
**Confirmed**
- Target: eliminate `any` types in src/**/*.ts
- Results directory: `./autoresearch-results/`
- Metric: `any` occurrence count (current: 47), direction: lower
- Verify: `grep -r ":\s*any" src/ --include="*.ts" | wc -l`
- Guard: `tsc --noEmit` must still pass
- Also keeping: hard_conflicts == 0 *(only for multi-metric)*

**Need to confirm**
- Run until all gone, or cap at N iterations?
- Foreground or background mode?

**Runtime checklist**
- Baseline first, then initialize results/state.
- Log every completed experiment before the next one starts.
- Use helper scripts for authoritative row/state updates.

**Next step**
- Reply "go" to start, or tell me what to change.
```

#### Format Rules

1. Always use the user's language — Chinese prompt gets Chinese headings.
2. Keep the confirmation scannable — aim for under 15 lines.
3. Show concrete numbers (current metric value, file count) so the user can sanity-check.
4. The "Need to confirm" section should only contain genuine blockers.
5. End with a clear call to action.
6. Do not replace the structured summary with a single-line "foreground/background?" prompt.
7. Keep the base template minimal. Add optional blocks only when genuinely needed.
8. Always show the `Results directory`.

The user replies "go", "start", "launch", or corrects something. No field names, no YAML.

## Launch Handoff

When the user replies with launch approval:
1. Require an explicit run-mode choice: **foreground** or **background**.
2. If **foreground**: keep the loop in the current session. Initialize `results.tsv`, `state.json`, `context.json`. Do not create `launch.json`, `runtime.json`, `runtime.log`. Report that the foreground run has started.
3. If **background**: persist the confirmed config, start the detached loop via `claude -p` in a tmux/screen session. Report the Results directory.

## Optional Question Guide

### Scope & Boundaries
- "I see both `src/models/` and `src/api/` — optimize the model layer only, or the full src?"
- "Should I only modify test files, or also refactor the source code?"

### Metric & Target
- "Your test suite reports line coverage (currently 58%). Track that, or branch coverage?"
- "What's your target — 80%? 90%? Or push as high as I can?"

### Verification & Guard
- "I can run `pytest --cov=src` to measure coverage. Different runner?"
- "Should I make sure `npm test` still passes after each change?"

### Duration
- "Want me to run 10 iterations as a test, or let it go overnight?"
- "Should this be an unattended run that keeps going, or a bounded trial run?"

## Internal Field Mapping

The wizard maps conversation to these fields (user never sees them):

- **Goal** — extracted from user's description
- **Scope** — inferred from repo + user's answers
- **Metric** — proposed by Claude, confirmed by user
- **Direction** — inferred from goal ("improve" = higher, "reduce/eliminate" = lower)
- **Verify** — Claude proposes a command based on repo tooling
- **Guard** — suggested if there's a regression risk
- **Iterations** — asked only if user wants bounded run
- **Run mode** — foreground (default) or background
- **Rollback** — `revert` (default) or `reset` (ask only if destructive rollback may be needed)

## Validation Rules

Before launching, silently validate:
- scope resolves to real files
- metric is mechanical (a command can produce a number)
- verify command is runnable
- guard command is pass/fail only
- iterations is a positive integer when provided

If validation fails, tell the user in plain language what went wrong and suggest a fix.

## Two-Phase Boundary

ALL questions happen BEFORE launch. Once the loop starts, it is fully autonomous. NEVER pause to ask anything during execution. If you encounter ambiguity mid-loop, apply best practices, log your reasoning, and keep iterating.
