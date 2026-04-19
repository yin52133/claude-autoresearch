# Session Resume Protocol

Detect and recover from interrupted runs. Resume from the last consistent retained state.

## Detection Signals

At the start of every invocation, check for prior run artifacts:

| Priority | Signal | Weight |
|----------|--------|--------|
| 1 | `autoresearch-results/state.json` exists and valid JSON | **primary** |
| 2 | `autoresearch-results/results.tsv` has a baseline row | strong |
| 3 | `autoresearch-results/lessons.md` exists | moderate |
| 4 | Git history with `experiment:` commits | moderate |

If none present, proceed with fresh run.

## Recovery Priority Matrix

| Condition | Decision |
|-----------|----------|
| JSON valid + TSV consistent | **Full resume** (skip wizard) |
| JSON valid + TSV inconsistent | **Mini-wizard** (1 round) |
| JSON missing + TSV exists | **TSV fallback** (reconstruct state) |
| Both missing | **Fresh start** |

### Full Resume

1. Restore loop variables from JSON `state` and `config`.
2. Print resume banner: "Resuming from iteration N, retained metric: X, best metric: Y. N kept, M discarded, K crashed so far."
3. Skip the wizard entirely.
4. Read lessons file if present.
5. If metric drifted, log a `drift` row and continue.

### Mini-Wizard

1. Show what was detected (prior run tag, iteration count, best metric, last status).
2. Ask exactly one question: resume from JSON state, or start fresh.
3. Present condensed confirmation block.
4. User replies "go" and the loop starts immediately.

### TSV Fallback

1. Reconstruct retained state from integer main rows in `results.tsv`.
2. Present condensed confirmation block.
3. After confirmation, continue from the next main iteration.

### Fresh Start

1. Proceed with the normal wizard flow.
2. Archive prior persistent run-control artifacts to `.prev` variants.

## Edge Cases

- **Corrupt JSON**: rename to `.bak`, fall back to TSV.
- **Corrupt TSV**: start fresh.
- **Different goal**: start fresh, archive old artifacts.
