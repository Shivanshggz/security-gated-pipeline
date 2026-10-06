# Security-Gated Release Pipeline

A CI/CD pipeline that enforces automated security gates before any code can
be merged or deployed to production.

## Overview

Every commit flows through a sequence of automated security checks. Any
finding above the defined severity threshold fails the build and blocks the
pipeline, ensuring code never reaches AWS EC2 unless it satisfies security
standards.

The Flask app in this repository is intentionally minimal — it exists only
to exercise the pipeline. The core engineering focus is the sequence of
automated gates.

## Stack

- **App:** Python 3.11 + Flask
- **Production Server:** Gunicorn (WSGI)
- **Gates:**
  - Bandit (SAST — static code analysis)
  - pip-audit (SCA — dependency vulnerabilities)
  - Gitleaks (secret detection)
  - Trivy (filesystem CVE scan)
- **CI/CD:** GitHub Actions
- **Agile Tracking:** GitHub Projects
- **Deploy:** AWS EC2 (Ubuntu) via SSH + systemd

## Severity Thresholds

Any finding at or above these thresholds blocks the corresponding stage.

| Gate | Tool | Fail On | Blocks |
|------|------|---------|--------|
| Functional Testing | PyTest | Any failure | Merge |
| Static Analysis | Bandit | Medium and above | Merge |
| Dependencies | pip-audit | Any known CVE | Merge |
| Secrets | Gitleaks | Any detection | Merge |
| Filesystem CVE | Trivy (fs) | HIGH / CRITICAL | Deploy |

## Local Development

### Setup

```bash
python -m venv venv
source venv/bin/activate           # Windows: venv\Scripts\Activate.ps1
pip install -r app/requirements.txt
pip install pytest bandit pip-audit