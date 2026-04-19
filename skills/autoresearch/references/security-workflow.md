# Security Workflow

Structured security audit and remediation.

## When to Use

Use security mode when:
- Auditing for security vulnerabilities
- Checking for OWASP top 10 issues
- Verifying authentication/authorization
- Scanning for secrets or credentials

## Workflow

### Phase 1: Scope and Focus

1. Scan the codebase to identify attack surface
2. Ask clarifying questions:
   - Audit whole codebase or specific layer?
   - Focus on specific threats (injection, auth, data exposure)?
   - Report only, or also fix critical findings?

### Phase 2: Threat Model

Build a mental model of the attack surface:
- Entry points (APIs, user inputs)
- Authentication/authorization mechanisms
- Data flows
- Dependencies

### Phase 3: Systematic Audit

For each area:
1. Review code for vulnerability patterns
2. Use verification commands to detect issues:
   - Static analysis tools
   - Pattern matching for common vulnerabilities
   - Dependency vulnerability scanning
3. Document each finding

### Phase 4: Findings

Record findings with severity:
- Critical: immediate action required
- High: fix soon
- Medium: fix when possible
- Low: informational

### Phase 5: Remediation (if requested)

Iteratively fix findings using the same loop protocol.

## Output

Artifacts:
- `security/{timestamp}/overview.md` — executive summary
- `security/{timestamp}/findings.md` — detailed findings by severity
- `security/{timestamp}/recommendations.md` — fix recommendations
- `autoresearch-results/results.tsv` — if remediation is iterative
