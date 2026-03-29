
# Secure by Design POC

This project demonstrates a **secure-by-design** approach to AWS infrastructure using CDK, where security guardrails are enforced by a separate security library (`secure-by-design-lib`) maintained by the security team — independent of the developer's own infrastructure code and tests.

---

## Project Structure

```
secure-by-design/
├── secure_by_design/
│   └── secure_by_design_stack.py   # Developer's CDK stack (S3 bucket)
├── tests/
│   └── unit/
│       └── test_secure_by_design_stack.py  # Developer's unit tests
├── app.py                          # CDK app entry point (security aspect applied here)
├── requirements.txt
└── requirements-dev.txt
```

---

## Two Layers of Testing

### 1. Developer Unit Tests (`tests/`)

Written by the infra developer to validate that the CDK stack is built correctly. These tests are **completely independent** of the security library — the developer does not need to know what's inside `secure-by-design-lib`.

Tests use `aws_cdk.assertions` to inspect the synthesized CloudFormation template in-memory — no AWS credentials or deployment needed.

| Test | What it checks |
|---|---|
| `test_s3_bucket_created` | Bucket is created with the correct name |
| `test_s3_bucket_public_access_block` | All 4 public access block flags are enabled |
| `test_s3_bucket_encryption` | SSE-S3 (AES256) encryption is configured |
| `test_s3_bucket_has_lifecycle_policy` | Lifecycle rule transitions objects to GLACIER after 30 days |

Run developer tests:
```bash
source .venv/bin/activate
pytest tests/
```

---

### 2. Security Aspect (`secure-by-design-lib`)

Provided by the security team as a separate library. It is applied in `app.py` as a CDK Aspect and runs during `cdk synth`. It scans every construct in the app and raises warnings if security configurations are missing.

```python
# app.py
cdk.Aspects.of(app).add(S3SecurityCheck())
```

The security aspect checks are **not part of the developer's test suite**. They run at synth time and are owned by the security team.

Sample output when security configs are missing:
```
cdk synth
[Warning at /SecureByDesignStack/SecureByDesignBucket/Resource] S3 Bucket should have server-side encryption enabled
[Warning at /SecureByDesignStack/SecureByDesignBucket/Resource] S3 Bucket should have public access block enabled
```

---

## Why They Are Independent

| | Developer Tests | Security Aspect |
|---|---|---|
| Owned by | Infra developer | Security team |
| Lives in | `tests/` in this repo | `secure-by-design-lib` (separate repo) |
| Runs during | `pytest` | `cdk synth` |
| Purpose | Validate infra is built correctly | Enforce org-wide security guardrails |
| Needs AWS? | No | No |

The developer writes tests to assert their intent (e.g. "I configured public access block"). The security aspect independently verifies the same at synth time. Both can catch the same misconfiguration but from different angles and ownership boundaries.

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```
