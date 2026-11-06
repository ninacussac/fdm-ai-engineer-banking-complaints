# Week 3 — Complaint API Release Notes

## 1. Release Overview

The Week 3 release delivers a FastAPI-based REST API for the Banking Complaint Resolution Assistant.

This release establishes a tested API baseline for complaint management and prepares the application for Week 4 RAG integration.

**Release status:** Candidate — Pending final review and approval.

**Release tag:** To be assigned after approval.

## 2. Features Delivered

### Complaint Management
- Create complaints through the REST API.
- Retrieve individual complaints and complaint collections.
- Update complaint status according to business rules.
- Automatically record complaint status-history events.

### Customer and Account Access
- Retrieve customer information.
- Retrieve associated customer complaints.
- Access account information.

### Application Reliability
- SQLAlchemy-based database persistence.
- Transaction rollback handling.
- Standardized API error responses.
- Structured request logging and correlation IDs.
- Application liveness and readiness endpoints.

## 3. API Documentation

The API contract is exported using OpenAPI 3.1.0.

**Artifact:** `openapi.json`

The application currently exposes 11 documented API paths.

Swagger UI is available at `/docs` when the application is running.

## 4. Test Results

| Test Category | Result |
|---|---|
| Unit tests | 31 passed |
| Integration tests | 13 passed |
| Total automated tests | 44 passed |
| End-to-end scenarios | 2 passed (included in integration tests) |
| Transaction rollback test | Passed |

### End-to-End Validation

The successful scenario verifies complaint creation, initial history, status updates, and SQLite persistence.

The failure scenario verifies that an invalid `OPEN` to `CLOSED` transition returns HTTP 409 without changing the complaint or adding an event.

### Transaction Evidence

The rollback test verifies that a failed status-history insertion prevents the corresponding complaint creation from being persisted.

## 5. Quality and Security

SonarQube Cloud and GitHub Actions are configured for automated analysis.

The previous SonarQube analysis passed its Quality Gate. The final release analysis must be verified after this release PR is submitted.

### Known Security Limitation

**CR-001 — Missing Authentication and Authorization**

Complaint endpoints do not currently enforce authentication or role-based authorization.

This finding remains a security limitation requiring remediation or explicitly approved deferral before deployment with real customer data.

## 6. Release Artifacts

- [Architecture Diagram](../architecture/week3_architecture.md)
- [OpenAPI Specification](../../openapi.json)
- [End-to-End Report](../evidence/week3_release/end_to_end_report.md)
- [Unit Test Report](../evidence/week3_release/unit_test_report.txt)
- [Integration Test Report](../evidence/week3_release/integration_test_report.txt)
- [Error and Logging Evidence](../evidence/week3_release/error_logging_evidence.md)
- [Main README](../../README.md)

## 7. Known Limitations and Future Work

- Authentication and authorization remain to be implemented or formally deferred.
- Advanced complaint workflows, including multi-category handling and escalation, are not fully implemented.
- Integration testing currently uses temporary SQLite databases.
- Week 4 RAG functionality is not part of this release.

## 8. Release Approval

The release candidate must pass final testing and review before the Week 3 Git tag is created.

The approved release will serve as the baseline for subsequent Week 4 development.