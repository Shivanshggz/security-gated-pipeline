# Continuous Compliance and Security-Gated Release Pipeline

**Name:** Shivansh Choukse
**Registration Number:** 24MIS0266
**Course:** Agile Development and DevOps
**Professor:** Dr. Arunkumar A

---

## Abstract

The Continuous Compliance and Security-Gated Release Pipeline is a DevOps
project that embeds automated security and compliance checks directly into
the software release process, ensuring that code cannot reach production
unless it satisfies defined security standards. Rather than treating
security as a manual, end-of-cycle audit, this project enforces it as a
hard, automated gate within the CI/CD pipeline itself.

A minimal Flask microservice is used as the deployable artifact to exercise
the pipeline, but the core engineering focus is the sequence of automated
gates: dependency vulnerability scanning, static code analysis, secret
detection, and filesystem security scanning. Any violation above a defined
severity threshold automatically blocks the build from being promoted or
deployed to the AWS EC2 production environment.

The project follows Agile methodology, using GitHub Projects to track
security findings as backlog items, and GitHub Actions to orchestrate the
gated pipeline, ensuring that security debt is visible, prioritized, and
resolved as part of normal sprint work rather than deferred indefinitely.

---

## 1. Project Overview

Most Agile teams treat security as a separate, occasional audit
disconnected from the sprint cycle. This project instead makes security a
first-class, automated part of every release: every commit passes through
a series of security gates before it can be built, promoted, or deployed.

The objective is to demonstrate how "shift-left" security practices can be
enforced through tooling rather than policy alone, while keeping the
underlying application intentionally simple so that the pipeline's gating
logic remains the central subject of study.

---

## 2. Technology Stack

The system relies entirely on free, open-source scanning tools integrated
into a standard GitHub Actions workflow, avoiding the need for paid
security platforms.

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Deployable App | Python 3.11, Flask | Minimal service used to exercise the pipeline |
| Production Server | Gunicorn (WSGI) | Serves the Flask app in production |
| Static Code Analysis (SAST) | Bandit | Detects insecure coding patterns in source code |
| Dependency Scanning (SCA) | pip-audit | Flags known vulnerabilities in Python dependencies |
| Secret Detection | Gitleaks | Detects hardcoded secrets and credentials in commits |
| Filesystem CVE Scan | Trivy (fs mode) | Scans repository files for known CVEs |
| Functional Testing | PyTest | Verifies application correctness |
| CI Orchestration | GitHub Actions | Runs the gated pipeline on every push and PR |
| Agile Tracking | GitHub Projects | Tracks security findings as sprint backlog items |
| Production Target | AWS EC2 (Ubuntu) | Deployment environment via SSH + systemd |

---

## 3. Severity Thresholds

Any finding at or above these thresholds blocks the corresponding stage.

| Gate | Tool | Fail Threshold | Blocks |
|------|------|----------------|--------|
| Functional Testing | PyTest | Any failure | Merge |
| Static Analysis | Bandit | Medium and above | Merge |
| Dependencies | pip-audit | Any known CVE | Merge |
| Secrets | Gitleaks | Any detection | Merge |
| Filesystem CVE | Trivy (fs) | HIGH / CRITICAL | Deploy |

---

## 4. Architecture

```mermaid
flowchart TD
    Dev[Developer Commit] --> PR[Pull Request]
    PR --> G1[Gate 1: PyTest + Bandit]
    G1 -->|Pass| G2[Gate 2: pip-audit]
    G1 -->|Fail| Block1[Blocked: Merge Denied]
    G2 --> G3[Gate 3: Gitleaks]
    G3 --> G4[Gate 4: Trivy fs]
    G4 -->|Pass| G5[Gate 5: SSH Deploy]
    G4 -->|Fail| Block2[Blocked: Deploy Denied]
    G5 --> EC2[AWS EC2 Production]
    Block1 --> Issue[GitHub Issue Filed]
    Block2 --> Issue
    Issue --> Board[GitHub Projects Board]