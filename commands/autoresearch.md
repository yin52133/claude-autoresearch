# /autoresearch

Activate the Autoresearch skill for autonomous code improvement.

## Usage

```
/autoresearch [goal]
```

If no goal is provided, the interaction wizard will ask.

## Examples

```
/autoresearch increase test coverage to 80%
/autoresearch eliminate all TypeScript any types
/autoresearch reduce lint warnings to zero
```

## What It Does

This command activates the Autoresearch skill, which drives an autonomous feedback loop:
1. The interaction wizard confirms your goal
2. Claude runs the autonomous loop: modify → verify → keep/discard → repeat
3. Results are logged to `autoresearch-results/results.tsv`

See the Autoresearch skill for full protocol details.
