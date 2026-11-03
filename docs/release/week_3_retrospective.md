# Week 3 — Retrospective

## 1. Overview

During Week 3, the Banking Complaint Resolution Assistant evolved from a data-access foundation into a FastAPI-based REST API.

The main objective was to implement a layered architecture, expose complaint management functionality, improve reliability, and establish a tested API baseline for Week 4.

## 2. Accomplishments

### API Development
- Implemented FastAPI endpoints for complaints, customers, accounts, and status-history events.
- Introduced Pydantic schemas for request validation.
- Implemented service and repository layers to separate business logic from database persistence.
- Added complaint status-transition validation and automatic history recording.

### Reliability and Testing
- Implemented SQLAlchemy transactions and rollback handling.
- Added standardized error responses using `AppError`.
- Implemented structured request logging and correlation IDs.
- Added health-check endpoints.
- Developed unit, integration, and end-to-end tests.

### Quality and Documentation
- Completed a structured code review.
- Integrated SonarQube Cloud with GitHub Actions.
- Exported the OpenAPI specification.
- Prepared architecture documentation, test evidence, and release notes.

## 3. Test Results

| Test Category | Result |
|---|---|
| Unit tests | 31 passed |
| Integration tests | 13 passed |
| Total | 44 passed |
| End-to-end scenarios | 2 passed |
| Transaction rollback scenario | Passed |

All reported results were obtained using automated pytest tests.

## 4. Challenges and Lessons Learned

### Separation of Responsibilities

One challenge was ensuring that business rules remained in the service layer while database operations were handled by repositories.

This improved the readability and testability of the application.

### Transaction Safety

Complaint creation and status-history insertion must remain consistent.

Testing simulated failures helped demonstrate that partial database writes can be rolled back.

### API Error Handling

The code review identified inconsistent error responses.

Standardizing them using `AppError` improved API consistency and client-facing error messages.

### Integration Test Isolation

Temporary SQLite databases and pytest fixtures helped avoid dependencies between tests and protect development data.

Using `try/finally` improved database engine cleanup.

### Code Quality

SonarQube Cloud provided automated static analysis, while the manual review identified application-level security concerns that static analysis did not resolve.

## 5. Known Limitations

- Authentication and role-based authorization are not yet implemented.
- Some advanced complaint workflows remain incomplete.
- Integration tests primarily use SQLite and simulated failures.
- RAG functionality has not yet been implemented.

## 6. Improvements for Future Work

- Introduce authentication and authorization before handling real customer data.
- Increase test coverage for failure scenarios and concurrent operations.
- Improve API response schemas and OpenAPI documentation.
- Extend automated quality checks.
- Strengthen audit traceability for human decisions.

## 7. Week 4 Dependencies

Week 4 RAG development will build on the Week 3 API baseline.

The existing complaint and customer endpoints should be reused rather than recreated.

The following components will support Week 4 development:

- FastAPI application and routers.
- Complaint and customer services.
- SQLAlchemy repositories and SQLite persistence.
- Standardized error handling.
- Structured logging and correlation IDs.
- Unit and integration test infrastructure.
- Exported OpenAPI contract.

## 8. Conclusion

Week 3 established a functional and tested complaint-management API.

The release provides a foundation for Week 4 RAG integration, while identified security limitations and remaining workflow requirements must be addressed before production deployment.