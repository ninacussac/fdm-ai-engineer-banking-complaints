# Explain and validate

## Use CASE for unresolved age buckets 0-7, 8-30 and 31+ days :
### Business and SQL Reasoning

The objective of this query is to classify unresolved complaints according to how long they have remained open.
This helps identify complaints requiring attention and prioritize older cases.
The query uses JULIANDAY() to calculate the difference between the current date and the complaint's received_at timestamp.

A CASE statement then assigns each complaint to one of three age categories:
- 0-7 days: Recently received complaints.
- 8-30 days: Complaints that have remained unresolved for a moderate period.
- 31+ days: Older unresolved complaints that may require additional attention.

The WHERE status <> 'CLOSED' condition excludes closed complaints from the analysis.

### Boundaries and Validation
The expected age bucket boundaries are:
| Age (days) | Expected bucket |
|---|---|
| 0 | 0-7 days |
| 7 | 0-7 days |
| 8 | 8-30 days |
| 30 | 8-30 days |
| 31 | 31+ days |

Two additional queries use fixed reference dates (`2025-02-01` and `2025-02-02`) to test the transitions between categories.
### Partitions and Expected Grain

No window function or SQL partition is required.
Expected grain: One row per unresolved complaint.
Each complaint is assigned one age value and one age bucket.

### Limitation
The current sample dataset contains mostly older complaints, limiting the diversity of age buckets.

## Use a CTE to identify repeat complainants :

### Business and SQL Reasoning

The objective is to identify customers who have submitted more than one complaint.
Repeat complainants may indicate recurring service issues or unresolved customer problems.
The query uses a Common Table Expression (CTE) named `repeat_complainants`.
Within the CTE, `RANK()` assigns a ranking to each customer's complaints.
`PARTITION BY customer_id` creates a separate ranking for each customer.
The outer query groups records by customer and uses `HAVING MAX(complaint_rank) > 1` to identify customers with multiple complaints.

### Boundaries and Validation

A repeat complainant is defined as a customer associated with more than one complaint.
The original dataset contains one complaint per customer, meaning no repeat complainants should be returned unless additional test data has been inserted.

### Partitions and Expected Grain

Partition: `customer_id`.
Each customer's complaints are ranked independently.
Expected grain: One row per customer identified as a repeat complainant.

### Limitations

- No time window is applied.
- Multiple complaints do not necessarily concern the same issue.


## Use ROW_NUMBER to select latest status per complaint :

### Business and SQL Reasoning

The objective is to retrieve the most recent recorded status for each complaint.
The `complaint_status_history` table stores the history of complaint status changes.
A CTE named `complaint_evolution` uses `ROW_NUMBER()` to rank these changes.
`PARTITION BY complaint_id` separates the history of each complaint.
`ORDER BY changed_at DESC` sorts status changes from newest to oldest.
The most recent status receives `complaint_rank = 1`.
The final query selects only these records using `WHERE complaint_rank = 1`.

### Boundaries and Validation

For every complaint with status history:
- The most recent event should receive rank 1.
- Older events should receive ranks 2, 3, etc.
- Only one event per complaint should appear in the final result.
The result can be validated by comparing the returned timestamp with the maximum `changed_at` for each complaint.

### Partitions and Expected Grain

Partition: `complaint_id`.
Each complaint's status history is ranked independently.
Expected grain: One row per complaint with at least one status history record.

### Limitations

- If two events have identical timestamps, the query does not guarantee which event receives rank 1.
- Adding `history_id DESC` as a secondary ordering criterion would make the result deterministic, assuming higher IDs correspond to later recorded events.
- Complaints without history records are excluded.
- Some sample timestamps are unrealistic because they were automatically generated during data insertion.

## Rank customers by complaint count :

### Business and SQL Reasoning

The objective is to identify customers who have submitted the highest number of complaints.
This analysis can support customer service monitoring and the identification of recurring issues.
The query uses `COUNT(*)` to calculate the number of complaints associated with each customer.
`GROUP BY customer_id` aggregates the data at the customer level.
`ORDER BY number_of_complaint DESC` sorts customers from the highest complaint count to the lowest.

### Boundaries and Validation

Each complaint is counted once.
Only customers with at least one complaint appear in the results.
To validate the calculation, the sum of all customer complaint counts should equal the total number of records in the `complaint` table.
Customers with the same number of complaints should have identical counts.

### Partitions and Expected Grain

No window function or `PARTITION BY` clause is used.
The aggregation is performed using `GROUP BY customer_id`.
Expected grain: One row per customer with at least one complaint.

### Limitations

- Customers without complaints are excluded.
- The query sorts customers by complaint count but does not assign explicit ranking numbers.
- Customers with identical complaint counts have no guaranteed relative order.

