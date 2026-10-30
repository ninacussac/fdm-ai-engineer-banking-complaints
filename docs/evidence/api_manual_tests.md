
# API Manual Test Evidence

## Overview

This document summarizes the manual API tests performed using
FastAPI Swagger UI.

The tests verify compliance with the API Contract Requirements,
including successful operations, request validation, error handling,
and complaint status transitions.

## Test 1 — Get Existing Complaint

**Endpoint:** GET /complaints/CMP016

**Expected HTTP status:** 200 OK

**Expected result:**
- Complaint ID: CMP016
- Customer ID: CUS001
- Status: UNDER_REVIEW

**Evidence:** screenshots/get_complaint_id_200.png

## Test 2 — Get Missing Complaint

**Endpoint:** GET /complaints/CMP9999

**Expected HTTP status:** 404 Not Found

**Expected response:**
```json
{
  "detail": "Complaint CMP9999 does not exist"
}
```

**Evidence:** screenshots/get_complaint_id_404.png

## Test 3 — Create Complaint

**Endpoint:** POST /complaints

**Expected HTTP status:** 201 Created

**Expected result:**
- The complaint is created successfully.
- A unique complaint_id is generated.
- The complaint is saved in SQLite.

**Evidence:** screenshots/post_complaint_201.png

## Test 4 — Valid Complaint Status Transition

**Endpoint:** PATCH /complaints/{complaint_id}/status

**Expected HTTP status:** 200 OK

**Expected result:**
- The complaint status is updated.
- A status history event is created.
- The previous and new statuses are recorded.

**Evidence:** screenshots/patch_status_200.png

## Test 5 — Invalid Complaint Status Transition

**Endpoint:** PATCH /complaints/{complaint_id}/status

**Expected HTTP status:** 409 Conflict

**Expected result:**
- The invalid transition is rejected.
- The complaint status remains unchanged.
- No new history event is created.

**Evidence:** screenshots/patch_status_409.png

## Test 6 — Invalid Status Value

**Endpoint:** PATCH /complaints/{complaint_id}/status

**Expected HTTP status:** 422 Unprocessable Entity

**Expected result:**
- The invalid status value is rejected by Pydantic.
- The complaint is not modified.

**Evidence:** screenshots/patch_status_422.png


## Test 7 — Get Existing Customer

**Endpoint:** GET /customers/CUS001

**Expected HTTP status:** 200 OK

**Expected result:**
- Customer ID: CUS001
- Customer information is returned successfully.

**Evidence:** screenshots/get_customer_id_200.png

## Test 8 — Get Customer Complaints

**Endpoint:** GET /customers/CUS001/complaints

**Expected HTTP status:** 200 OK

**Expected result:**
- A list of complaints belonging to CUS001 is returned.
- Each complaint is associated with the requested customer.

**Evidence:** screenshots/get_customer_complaints_200.png

## Test 9 — Get Missing Customer

**Endpoint:** GET /customers/CUS999

**Expected HTTP status:** 404 Not Found

**Expected response:**
```json
{
  "detail": "Customer CUS999 does not exist"
}
```

**Evidence:** screenshots/get_customer_id_404.png

## Automated Test Results

**Command:**

```bash
python -m pytest -v
```

**Result:**

30 passed in 1.16s

**Evidence:** api_test_results.txt

## Conclusion

The REST API endpoints have been manually tested using Swagger UI.

The tests demonstrate successful complaint retrieval, complaint
creation, status updates, request validation, and error handling.

Complaint status transitions are validated by the domain model,
and successful changes are recorded in the complaint status history.

All 30 automated tests passed successfully.
