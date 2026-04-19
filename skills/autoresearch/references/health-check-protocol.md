# Health Check Protocol

Self-monitoring system that validates environment and run integrity.

## Lightweight Checks (Every Iteration Boundary)

| Check | How | Failure Action |
|-------|-----|----------------|
| Disk space | `df -m . \| awk 'NR==2{print $4}'` | Warning at <1GB, hard blocker at <500MB |
| Git state | `git status --porcelain` | Warning if unexpected files; hard blocker if repo corrupt |
| Verify command | Confirm verify command still resolves | Hard blocker if missing |
| Log integrity | TSV has baseline + consistent row count | Hard blocker if corrupt |

## Extended Checks (Every 10 Iterations)

| Check | How | Failure Action |
|-------|-----|----------------|
| External modifications | `git log --oneline -5` matches expected | Warning if unexpected commits |
| Scope integrity | All in-scope files still exist | Hard blocker if deleted |
| Environment drift | Re-check disk space | Warning on degradation |
| Verify consistency | Run verify twice, compare | Warning if results differ |
| Context health | Protocol Fingerprint Check | Re-read runtime docs |

## Hard Blocker Criteria

These stop the loop immediately:

| Issue | Reason |
|-------|--------|
| Disk < 500MB | Cannot safely commit |
| Results log corrupted | Cannot track progress |
| Git repo broken | Cannot commit or revert |
| Verify command missing | Cannot measure progress |
| All scope files deleted | Nothing to modify |

## Wall-Clock Tracking

Track iteration timing to detect resource contention:
- Warning: current_time > 3x rolling average of last 5 iterations
- No hard blocker for timing alone

## Helper Output Contract

Return structured JSON:
```json
{
  "decision": "ok|warn|block",
  "warnings": ["..."],
  "blockers": ["..."],
  "resume_decision": "full_resume|tsv_fallback|mini_wizard|fresh_start"
}
```
