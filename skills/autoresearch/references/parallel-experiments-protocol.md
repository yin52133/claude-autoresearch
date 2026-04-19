# Parallel Experiments Protocol

Test multiple hypotheses simultaneously.

## When to Use

Use parallel mode when:
- Multiple promising hypotheses exist
- Environment has resources (CPU cores, time)
- Hypotheses are independent

## How It Works

Instead of one hypothesis per iteration, generate N hypotheses (default: 2, max: 3).

Each hypothesis gets its own "worker" that:
1. Makes the change
2. Runs verification
3. Records the result

## Batch Selection

After all workers complete:
1. Compare metrics across workers
2. Select the best result (keep)
3. Discard the rest
4. Log the winning iteration

## TSV Notation

Workers use structured labels in descriptions:

```
iteration	commit	metric	delta	guard	status	description
1a	abc123	44	-3	pass	keep	[worker-a] narrowed auth types
1b	def456	46	-1	pass	discard	[worker-b] generic wrapper
2	ghi789	41	-3	pass	keep	[worker-a] refined auth approach
```

## Limitations

- Workers cannot depend on each other's results
- Each worker needs its own git commit
- Verification must be independently runnable
- Guard must pass for all workers to proceed

## When to Enable

Ask during the wizard if:
- Multiple promising approaches are obvious
- CPU >= 4 cores available
- The problem is parallelizable
