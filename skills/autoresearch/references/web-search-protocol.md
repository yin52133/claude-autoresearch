# Web Search Protocol

When stuck, search for external solutions.

## When to Use

Activate after 2 PIVOTs without improvement (per `pivot-protocol.md`).

## Workflow

### Step 1: Form Query

Based on the current blocker and pivot history:
- What is the specific problem?
- What has been tried already?
- What might others have done?

Form a precise, searchable query.

### Step 2: Search

Use the web search tool to find solutions:
- Official documentation
- Stack Overflow discussions
- GitHub issues and PRs
- Blog posts
- Tutorial content

### Step 3: Evaluate

Assess results:
- Is the solution relevant to this specific codebase?
- Is it compatible with the current stack?
- What verification would confirm it works?

### Step 4: Apply

Treat search results as hypotheses — still verify mechanically.

### Step 5: Log

Log as status `search` in the results TSV:
```
iteration	commit	metric	delta	guard	status	description
N	-	38	-3	pass	search	web search: reduce latency in Python async
```

## Rules

- Always verify mechanically after applying a found solution
- Document what was searched and why
- If search finds nothing useful, continue pivoting
- Web search is an escalation tool, not a replacement for iteration
