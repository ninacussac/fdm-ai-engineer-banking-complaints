# Banking Complaint API — Setup and Run Guide

## 1. Overview

This project provides a REST API for a Banking Complaint Management application using FastAPI, SQLAlchemy, and SQLite.

The API supports the management of customers, accounts, complaints, and complaint status events.

It also provides health check endpoints to monitor application availability and database connectivity.

## 2. Requirements

- Python with a version compatible with `requirements.txt`
- Git
- Windows PowerShell (commands below)
- pip

## 3. Installation

Clone the repository and navigate to the project directory.

```powershell
git clone <repository-url>
cd fdm-ai-engineer-banking-complaints
```

Create a Python virtual environment:

```powershell
python -m venv venv
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

If PowerShell blocks virtual environment activation, use a process-scoped execution policy:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## 4. Environment Configuration

The application loads its settings from environment variables using `python-dotenv`.

Copy the provided configuration template:

```powershell
Copy-Item .env.example .env
```

Example configuration:

```dotenv
APP_NAME=Banking Complaint App
DATABASE_URL=sqlite:///bank_complaint.db
```

The SQLite database file is created or accessed relative to the current working directory.

The `.env` file is excluded from Git to avoid exposing local configuration or sensitive credentials.

## 5. Database Initialization

The application uses SQLAlchemy ORM models.

To create missing tables in the configured SQLite database, run the following command from the repository root:

```powershell
python -c "import src.models.models; from src.data.base import Base; from src.data.connection import engine; Base.metadata.create_all(bind=engine); print('Database tables initialized')"
```

This command creates missing tables without deleting existing tables or records.

It is intended for initial local setup. Schema changes in a production environment should be managed using database migrations.

## 6. Running the Application

Start the FastAPI development server:

```powershell
python -m uvicorn src.main:app --reload
```

The application is available at:

`http://127.0.0.1:8000`

Stop the server using `Ctrl + C`.

## 7. API Documentation

FastAPI automatically generates interactive documentation.

Swagger UI:

`http://127.0.0.1:8000/docs`

ReDoc:

`http://127.0.0.1:8000/redoc`

OpenAPI JSON:

`http://127.0.0.1:8000/openapi.json`

## 8. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/bank/customers` | Retrieve customers |
| POST | `/bank/customers` | Create a customer |
| GET | `/bank/accounts` | Retrieve accounts |
| POST | `/bank/accounts` | Create an account |
| GET | `/bank/complaints` | Retrieve complaints |
| POST | `/bank/complaints` | Create a complaint |
| GET | `/bank/events` | Retrieve complaint status events |
| POST | `/bank/events` | Create a complaint status event |

## 9. Health Checks

### Liveness

Endpoint:

`GET /health/live`

Checks whether the application can respond to HTTP requests.

Expected response:

```json
{
  "status": "alive"
}
```

HTTP status: `200 OK`

The liveness endpoint does not depend on the database.

### Readiness

Endpoint:

`GET /health/ready`

Checks whether the application can connect to SQLite and execute a simple SQL query.

When the database is accessible:

```json
{
  "status": "ready"
}
```

HTTP status: `200 OK`

When the database is unavailable:

```json
{
  "detail": "Database unavailable"
}
```

HTTP status: `503 Service Unavailable`

The readiness check does not return internal database error messages.

Note: The current readiness check verifies SQL connectivity, not whether every application table exists.

## 10. Running Tests

Run the complete test suite:

```powershell
python -m pytest -v
```

The project includes tests for domain models and the ComplaintService business logic.

## 11. Troubleshooting

**ModuleNotFoundError**

Ensure the virtual environment is activated and all requirements are installed.

**Port 8000 already in use**

Stop the existing server or start FastAPI on another port:

```powershell
python -m uvicorn src.main:app --reload --port 8001
```

**Database connection errors**

Check the `DATABASE_URL` value in `.env` and verify that the database file location is accessible.

**PowerShell activation blocked**

Use a process-scoped execution policy or execute Python directly from the virtual environment.

## 12. Security Considerations

- Do not commit `.env`, API keys, passwords, or other credentials.
- Use `.env.example` to document configuration variables without exposing secrets.
- Return generic error messages from readiness checks.
- Keep database access and business logic separate from API routing.

## 13. Project Architecture

The application follows a layered architecture:

```text
API Routers
    |
    v
Service Layer
    |
    v
Repository Layer
    |
    v
SQLAlchemy / SQLite
```

Pydantic schemas validate API requests, while domain models enforce business rules.

Configuration is centralized in `src/config.py`, and database session dependencies are exposed through `src/dependencies.py`.