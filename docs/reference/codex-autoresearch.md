# Reference: codex-autoresearch

This project is adapted from [codex-autoresearch](https://github.com/leo-lilinxiao/codex-autoresearch) by [leo-lilinxiao](https://github.com/leo-lilinxiao).

## About the Original

**codex-autoresearch** is an autonomous experimentation framework for OpenAI's Codex CLI. It enables continuous, self-directed code improvement through a structured feedback loop.

Core concept: *"Tell it what you want to improve, then walk away. It modifies your code, verifies results, keeps or discards changes, and repeats."*

## Key Features (Original)

- 7 operational modes: loop, plan, debug, fix, security, ship, exec
- Foreground and background execution
- Escalation ladder for stalled progress
- Full audit trail in `autoresearch-results/results.tsv`
- Session resumability
- Written primarily in Python

## Adaptations for Claude Code

| Aspect | codex-autoresearch | claude-autoresearch |
|---|---|---|
| Platform | OpenAI Codex CLI | Anthropic Claude Code |
| Packaging | Codex skill (SKILL.md) | Claude Code plugin |
| Execution | `codex exec` subprocess | Claude session (direct) |
| Runtime controller | Python runtime_ctl.py | Not needed (Stop hook) |
| Hook events | SessionStart, Stop | SessionStart, PostToolUse, Stop |
| Modes (MVP) | 7 modes | 3 modes (loop, debug, fix) |

## Acknowledgment

This project would not exist without the excellent design and implementation of codex-autoresearch. We gratefully acknowledge the original authors' work under the MIT License.
