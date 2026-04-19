# Claude Autoresearch

## Development

- Python scripts in `scripts/` require Python 3.8+
- Run scripts with `PYTHONPATH=scripts/` for cross-imports
- Test pipeline: see `docs/spec/design-spec.md` for architecture

## Plugin Structure

- `.claude-plugin/plugin.json` — manifest
- `commands/autoresearch.md` — `/autoresearch` slash command
- `skills/autoresearch/SKILL.md` — core protocol
- `hooks/hooks.json` — event hooks
- `scripts/` — Python state management

## Testing

```bash
cd /tmp && mkdir test-repo && cd test-repo && git init
PYTHONPATH=/path/to/scripts python3 /path/to/scripts/autoresearch_init_run.py \
  --goal "test" --metric-name "coverage" --direction maximize \
  --verify "echo 75" --baseline-metric 75
```
