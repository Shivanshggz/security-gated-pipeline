# Severity Thresholds

Every security gate in this pipeline has a defined severity threshold. Any
finding at or above the threshold fails the build and blocks the pipeline.

## Threshold Table

| Gate | Tool | Threshold | Blocks | Rationale |
|------|------|-----------|--------|-----------|
| Functional Tests | PyTest | Any failure | Merge | Correctness is non-negotiable |
| Static Analysis (SAST) | Bandit | Medium and above | Merge | Medium findings still represent real risk in production code |
| Dependency Scan (SCA) | pip-audit | Any known CVE | Merge | Any known CVE in a pinned dependency is a known risk |
| Secret Detection | Gitleaks | Any detection | Merge | Secrets in git history are compromised the moment they are committed |
| Filesystem CVE Scan | Trivy | HIGH and CRITICAL | Deploy | Limits noise from LOW/MEDIUM; blocks only material risk |

## Why These Thresholds?

### Bandit — Medium and above
Bandit classifies findings as Low, Medium, or High. Medium covers issues
such as `subprocess` with `shell=True`, `assert` used for security checks,
and hardcoded bind addresses. These are real weaknesses — failing on Medium
prevents them from silently accumulating.

### pip-audit — Any CVE
Unlike SAST, dependency CVEs are **specific, published, and exploitable**.
There is no "false positive" for a CVE in a pinned version. Any finding
must be addressed — either by upgrading or by justified exception.

### Gitleaks — Any detection
Secrets, once committed, must be considered compromised. There is no
acceptable baseline number of secrets in a repository. Every detection
blocks the build.

### Trivy — HIGH and CRITICAL only
Trivy reports on both application and system packages. In this project, the
base image is `ubuntu-latest`, which may include LOW/MEDIUM findings that
are not actionable in a lab context. Restricting to HIGH/CRITICAL keeps
the gate meaningful without overwhelming the backlog.

## Overrides

Findings may be suppressed only with justification:

| Tool | Mechanism | Example |
|------|-----------|---------|
| Bandit | `.bandit` config with `skips` list | `B104` — dev-only `0.0.0.0` binding |
| pip-audit | `--ignore-vuln <ID>` with comment | No fix available upstream |
| Gitleaks | `.gitleaks.toml` allowlist | Test fixtures with fake secrets |
| Trivy | `--ignorefile` | Only if the finding is not exploitable |

**Every override must be justified in a pull request description.**