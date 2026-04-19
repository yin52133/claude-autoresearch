[中文](README_CN.md) | English

# Claude Autoresearch

An autonomous goal-driven experimentation framework for [Claude Code](https://claude.ai/claude-code). Tell it what you want to improve, then walk away — it modifies your code, verifies results, keeps or discards changes, and repeats.

Adapted from [codex-autoresearch](https://github.com/leo-lilinxiao/codex-autoresearch) for Claude Code's plugin architecture.

## Features

- **Autonomous loop**: modify → commit → verify → keep/discard → repeat
- **Three modes**: loop (metric-driven), debug (hypothesis-driven), fix (error-count)
- **Escalation ladder**: refine → pivot → web search → stop when stuck
- **Session resume**: hooks detect active runs and inject context on restart
- **Full audit trail**: every iteration logged to `autoresearch-results/results.tsv`
- **Guard commands**: existing tests always pass, preventing regressions

## Installation

### Prerequisites

- [Claude Code CLI](https://claude.ai/claude-code) installed
- Python 3.8+
- Git

### Install as Plugin

```bash
claude plugin add /path/to/claude-autoresearch
```

Or clone and install:

```bash
git clone https://github.com/yin52133/claude-autoresearch.git
claude plugin add ./claude-autoresearch
```

## Usage

### Quick Start

In any Claude Code session:

```
/autoresearch increase test coverage to 80%
```

The interaction wizard will:
1. Scan your repository
2. Confirm the goal and metric
3. Measure baseline
4. Ask for "go"
5. Run the autonomous loop

### Modes

**Loop mode** — drive a measurable metric:
```
/autoresearch reduce lint warnings to zero
/autoresearch increase type coverage to 95%
```

**Debug mode** — investigate bugs:
```
/autoresearch debug the memory leak in the cache module
```

**Fix mode** — eliminate errors:
```
/autoresearch fix all TypeScript compilation errors
```

### Results

All results are stored in `autoresearch-results/`:

| File | Purpose |
|---|---|
| `results.tsv` | Iteration log |
| `state.json` | Current run state |
| `lessons.md` | Cross-run learnings |

### State Management

```bash
# Check if a run is active
python3 scripts/autoresearch_state.py check

# Get run summary
python3 scripts/autoresearch_state.py summary

# Pause/resume/complete
python3 scripts/autoresearch_state.py pause
python3 scripts/autoresearch_state.py resume
python3 scripts/autoresearch_state.py complete
```

## How It Works

### Two-Phase Boundary

**Phase 1 — Interactive**: The wizard confirms goal, metric, and verification command. This is the only phase that asks questions.

**Phase 2 — Autonomous**: After "go", Claude runs the loop with no further human input. Each iteration makes one focused change and verifies it mechanically.

### Escalation Ladder

| Trigger | Action |
|---|---|
| 3 consecutive discards | **Refine** — adjust within current strategy |
| 5 consecutive non-keeps | **Pivot** — fundamentally different approach |
| 2 pivots without improvement | **Web search** — look for external solutions |
| 3 pivots without improvement | **Stop** — report to human |

### Hooks

The plugin uses three Claude Code hooks:

- **SessionStart**: Detects active runs and provides resume context
- **PostToolUse**: Monitors iteration progress and detects stalls
- **Stop**: Warns before exiting with an active run

## Project Structure

```
claude-autoresearch/
├── .claude-plugin/plugin.json       # Plugin manifest
├── commands/autoresearch.md         # Slash command entry point
├── skills/autoresearch/
│   ├── SKILL.md                     # Core protocol
│   └── references/                  # Mode workflows, escalation, invariants
├── hooks/hooks.json                 # Hook configuration
├── scripts/                         # Python state management scripts
├── docs/
│   ├── spec/                        # Design specification
│   └── reference/                   # Credits and comparisons
├── README.md
├── README_CN.md
└── LICENSE
```

## Acknowledgments

This project is adapted from [codex-autoresearch](https://github.com/leo-lilinxiao/codex-autoresearch) by [leo-lilinxiao](https://github.com/leo-lilinxiao). We gratefully acknowledge the original authors' excellent design and implementation.

## License

[MIT](LICENSE)
