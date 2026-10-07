
## Evidence Captured

| Demo | Result |
|------|--------|
| pip-audit blocks Flask 3.0.3 | CVE detected, pipeline failed |
| Fix: Flask 3.1.3 | Gate reopened |
| Gitleaks passes on clean repo | Passed |
| Trivy passes on clean repo | Passed |
| Bandit blocks `shell=True` | Auto-issue filed |
| File-security-issue job runs | Issue #7 created with 4 labels |

## Outcome

Security findings are now **automatically tracked as backlog items** — the shift-left, Agile-integrated security posture the project intended to demonstrate.