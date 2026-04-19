# Structured Output Specification

Every mode must produce predictable output. Interactive modes use human-readable sections. `exec` uses JSON-only machine-readable output.

## Status Values

| Status | Meaning |
|--------|---------|
| `baseline` | Initial measurement before any changes |
| `keep` | Change improved the metric and passed guard |
| `discard` | Change did not improve or failed guard |
| `crash` | Verification crashed or produced an error |
| `no-op` | No actual diff was produced |
| `blocked` | Hard blocker encountered, loop stopped |
| `refine` | Strategy adjustment within current approach |
| `pivot` | Strategy abandoned, fundamentally new approach |
| `search` | Web search performed for external knowledge |
| `drift` | Metric drifted from expected value during session resume |

## Common Response Sections

Before work starts: `Setup`, `Config`, `Baseline`
During work: `Iteration`, `Metric`, `Decision`
At completion: `Summary`, `Artifacts`, `Next Actions`

## Iteration Line

Use this shape during loops:
```
[iteration N] hypothesis -> metric result -> keep/discard/crash
```

Extended statuses:
```
[iteration N] [REFINE] adjusted strategy -> metric result -> refine
[iteration N] [PIVOT] abandoned strategy X, trying Y -> metric result -> pivot
[iteration N] [SEARCH] "query" -> found approach -> metric result -> search
```

## Completion Summary (loop mode)

Required:
- goal, baseline metric, best metric
- keep/discard/crash/refine/pivot counts
- lessons extracted count
- artifact path

Artifacts:
- `autoresearch-results/results.tsv`
- `autoresearch-results/lessons.md`
- `autoresearch-results/state.json`
- `autoresearch-results/context.json`

## Progress Reporting

Every 5 iterations and at completion:
- baseline vs best metric
- keep/discard/crash counts
- the last few statuses
- the next likely direction
