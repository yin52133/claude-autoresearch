# Modes

Quick reference for all available modes.

| Mode | When to use | Key difference |
|------|-------------|---------------|
| `loop` | Measurable metric improvement | Default metric-driven loop |
| `debug` | Bug investigation | Hypothesis-driven, not metric-driven |
| `fix` | Error elimination | Metric = error count (minimize to 0) |
| `security` | Security audit | Structured threat investigation |
| `ship` | Pre-launch readiness | Checklist-driven |
| `plan` | Convert vague goal to config | Does not edit code |
| `exec` | CI/CD automation | JSON output only, no human text |

Use `Mode: <name>` to force a specific mode.
