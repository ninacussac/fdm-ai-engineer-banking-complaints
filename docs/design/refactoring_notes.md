# Service Layer Refactoring Notes

**Exercise:** Week 3 — Exercise 3.1.2: Create the Complaint Service Layer

## 1. Overview

The objective of this refactoring was to improve the architecture of the Banking Complaint Management application by separating responsibilities between API routers, services, repositories, schemas, and domain models.

The main goals were to:

- Separate business logic from database operations.
- Introduce dependency injection to make services independently testable.
- Implement business validation before complaint creation.
- Coordinate complaint status changes through the service layer.
- Organize the codebase into dedicated modules for each business entity.
- Preserve existing functionality throughout the refactoring.

The refactoring followed the principles of separation of concerns, loose coupling, and testability.

## 2. Architecture Before Refactoring

### 2.1 Mixed Responsibilities

Initially, multiple business entities were handled within the same Python files.

For example:

- `customer_service.py` contained CustomerService, AccountService, ComplaintService, and ComplaintStatusEventService.
- `customer_repository_sqlalchemy.py` contained all four SQLAlchemy repositories.
- `customer_schema.py` defined the Pydantic schemas for all four entities.
- `complaint_routers.py` contained the API endpoints for customers, accounts, complaints, and status events.

Although these files were organized into architectural layers, they grouped several business entities together, making the code harder to maintain and navigate.

### 2.2 Tight Coupling

Services initially instantiated their own repositories.

For example:

```python
class ComplaintService:
    def __init__(self):
        self.repository = ComplaintRepository()
```

This created tight coupling between services and their concrete SQLAlchemy repositories.

As a result, replacing database dependencies with fake implementations during unit testing was more difficult.

### 2.3 Limited Business Validation

The initial ComplaintService mainly delegated database operations to ComplaintRepository.

Complaint creation did not explicitly verify that:

- The referenced customer existed.
- The referenced account existed.
- The account belonged to the customer submitting the complaint.

Complaint status transition rules existed in the domain model but were not coordinated through a dedicated service operation.

## 3. Refactoring Implementation

### 3.1 Separation of Modules

Each business entity now has dedicated schema, service, repository, and router modules.

The resulting structure is:

```text
src/
├── api/
│   ├── customer_router.py
│   ├── account_router.py
│   ├── complaint_router.py
│   └── complaint_status_event_router.py
│
├── schemas/
│   ├── customer_schema.py
│   ├── account_schema.py
│   ├── complaint_schema.py
│   └── complaint_status_event_schema.py
│
├── services/
│   ├── customer_service.py
│   ├── account_service.py
│   ├── complaint_service.py
│   └── complaint_status_event_service.py
│
├── repositories/
│   ├── customer_repository_sqlalchemy.py
│   ├── account_repository_sqlalchemy.py
│   ├── complaint_repository_sqlalchemy.py
│   └── complaint_status_event_repository_sqlalchemy.py
│
└── models/
    └── models.py
```

This organization makes responsibilities easier to identify and allows each module to evolve independently.

### 3.2 Dependency Injection

All four services were modified to receive their repository dependencies through their constructors instead of creating them internally.

For example:

```python
class ComplaintService:
    def __init__(
        self,
        complaint_repository,
        customer_repository,
        account_repository
    ):
        self.complaint_repository = complaint_repository
        self.customer_repository = customer_repository
        self.account_repository = account_repository
```

The application routers construct the services using the SQLAlchemy repository implementations.

During unit testing, these dependencies can be replaced with fake repositories.

This improves test isolation and reduces coupling between the service and persistence layers.

### 3.3 Complaint Creation Validation

Business validation was introduced in ComplaintService before persisting a complaint.

The service performs the following checks:

1. Verify that the customer exists.
2. If an account is provided, verify that the account exists.
3. Verify that the account belongs to the specified customer.
4. Delegate persistence to ComplaintRepository only when validation succeeds.

Invalid requests raise ValueError before the complaint is saved.

This prevents complaints from being associated with nonexistent customers, nonexistent accounts, or accounts owned by another customer.

### 3.4 Complaint Retrieval

A `get_complaint_by_id()` method was added to ComplaintService.

The service delegates data retrieval to the repository and raises ValueError when the complaint does not exist.

The repositories also provide `get_by_id()` methods for retrieving customers, accounts, and complaints by their identifiers.

### 3.5 Complaint Status Management

A `change_status()` operation was implemented in ComplaintService.

The service:

1. Retrieves the complaint.
2. Invokes the domain model's `change_status()` method.
3. Relies on the domain model to validate the requested transition.
4. Receives the generated ComplaintStatusEvent.
5. Delegates persistence of the complaint and event to ComplaintRepository.

This maintains a clear separation between business coordination, domain validation, and database persistence.

### 3.6 Transaction Management

ComplaintRepository provides a `save_status_change()` method that persists both:

- The updated Complaint.
- The associated ComplaintStatusEvent.

Both operations are committed in a single database transaction.

If an exception occurs during persistence, the repository rolls back the transaction and re-raises the exception.

This protects consistency between a complaint's current status and its recorded status history.

### 3.7 API Router Refactoring

The original combined router was separated into four dedicated API routers.

Each router handles one business resource:

| Router | Endpoints |
|---|---|
| CustomerRouter | GET and POST `/bank/customers` |
| AccountRouter | GET and POST `/bank/accounts` |
| ComplaintRouter | GET and POST `/bank/complaints` |
| ComplaintStatusEventRouter | GET and POST `/bank/events` |

The routers delegate operations to their corresponding services.

The existing endpoint paths and HTTP methods were preserved.

All four routers are registered in the FastAPI application through `app.include_router()`.

### 3.8 Schema Refactoring

The original `customer_schema.py` was separated into four dedicated Pydantic schema modules.

Each schema defines the input data expected for its corresponding entity.

This improves organization and keeps API data validation separate from business rules.

## 4. Architecture After Refactoring

The application now follows a layered architecture.

```text
HTTP Request
     |
     v
API Router
     |
     v
Pydantic Schema Validation
     |
     v
Service Layer
     |
     +----> Domain Model
     |      (Business Rules)
     |
     v
Repository Layer
     |
     v
SQLAlchemy / SQLite
```

The responsibilities of each layer are:

| Layer | Responsibility |
|---|---|
| API Router | Handle HTTP requests and delegate operations |
| Schema | Validate and structure request data |
| Service | Coordinate business logic and use cases |
| Domain Model | Enforce entity-level business rules |
| Repository | Execute database operations and manage persistence |
| Database | Store application data |

The service layer does not execute SQL queries directly.

Database operations remain encapsulated in the repository layer.

## 5. Testing and Validation

### 5.1 Unit Tests

The ComplaintService was tested using fake repositories to avoid dependence on the SQLAlchemy database.

The 11 unit tests cover:

- Fake customer repository behavior.
- Fake account repository behavior.
- Fake complaint repository behavior.
- Successful complaint creation.
- Rejection of nonexistent customers.
- Rejection of nonexistent accounts.
- Rejection of accounts belonging to another customer.
- Retrieval of nonexistent complaints.
- Valid complaint status transitions.
- Invalid complaint status transitions.
- Status changes for nonexistent complaints.

**Result: 11 ComplaintService unit tests passed.**

### 5.2 Regression Testing

The existing domain model tests were executed after the refactoring to ensure that previously implemented behavior was preserved.

The combined test suite was also run after the architectural changes.

**Result: 23 tests passed.**

### 5.3 FastAPI Verification

The API was checked after the router and module restructuring.

The OpenAPI schema confirmed that the following endpoints remained registered:

- `/bank/customers`
- `/bank/accounts`
- `/bank/complaints`
- `/bank/events`
- `/health`

Additional API checks confirmed that:

- GET `/health` returned HTTP 200.
- POST `/bank/complaints` with an empty body returned HTTP 422 due to missing required fields.

These results confirmed that the application remained importable and that FastAPI request validation continued to operate.

## 6. Limitations and Future Improvements

The current implementation meets the main objectives of Exercise 3.1.2, but some improvements remain possible.

- Add isolated unit tests for CustomerService, AccountService, and ComplaintStatusEventService.
- Add integration tests using a dedicated test database to verify SQLAlchemy persistence and transaction rollback behavior.
- Map service-level ValueError exceptions to appropriate HTTP error responses.
- Review direct status-event creation to prevent bypassing domain transition rules.
- Consider using explicit repository interfaces or Protocol classes to formalize repository contracts.
- Consider centralizing dependency construction using FastAPI's dependency injection system.

These improvements can be addressed in future iterations without affecting the current service-layer separation.

## 8. Conclusion

The refactoring transformed the application into a more modular and testable layered architecture.

Business validation and use-case coordination are handled by the service layer, entity-level rules remain in the domain models, and database operations remain in the repositories.

Dependency injection allows services to use fake repositories during unit tests while continuing to use SQLAlchemy implementations in the application.

The existing API endpoints were preserved, and the test suite continued to pass after the refactoring.

The implementation therefore satisfies the primary architectural requirements of Exercise 3.1.2 — Create the Complaint Service Layer.