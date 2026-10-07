
---

## Severity Thresholds

| Gate | Tool | Fail Threshold | Blocks |
|------|------|----------------|--------|
| Functional Tests | PyTest | Any failure | Merge |
| Static Analysis (SAST) | Bandit | Medium and above | Merge |
| Dependencies (SCA) | pip-audit | Any known CVE | Merge |
| Secrets | Gitleaks | Any detection | Merge |
| Filesystem CVEs | Trivy | HIGH / CRITICAL | Deploy |

See [`docs/severity-thresholds.md`](docs/severity-thresholds.md) for
threshold rationale and override policy.

## Auto-Issue Filing

When any gate fails, the pipeline automatically files a GitHub issue with:

- The failed gate name
- `severity:*`, `gate:*`, and `type:security` labels
- A link to the failing workflow run
- Instructions to fix and re-run

Findings become tracked backlog items in the GitHub Projects board — no
manual triage required.

## Demo Patches

Ready-to-apply patches for demonstrating each gate are in
[`docs/demo-patches/`](docs/demo-patches/):

| Patch | Gate | What It Triggers |
|-------|------|------------------|
| `01-bandit-shell-injection.patch` | Bandit | `shell=True` command injection |
| `02-pip-audit-vulnerable-dep.patch` | pip-audit | Flask 3.0.3 CVE |
| `03-gitleaks-hardcoded-secret.patch` | Gitleaks | AWS access key |
| `04-trivy-vuln-package.patch` | Trivy | Vulnerable `requests` version |