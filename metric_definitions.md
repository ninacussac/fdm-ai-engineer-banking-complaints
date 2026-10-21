# Metric Definitions and Caveats

These metrics summarize complaint volumes and resolution time in the BankCRS SQLite dataset.

## Complaint volume
Number of complaint records in each group.

- Numerator / value: COUNT(*), the number of complaint rows in the group.
- Denominator: None for an absolute count. When interpreting proportions, the denominator would be the total number of complaints in the relevant population or period.
- Grouping: status, category, or strftime('%Y-%m', received_at).
- Filters: No status or category exclusions in the volume queries. Each complaint belongs to its recorded group. Rows with NULL grouping values would form a separate group if present.

## Distinct customer count
Number of unique customers represented by complaints in each group.

- Numerator / value: COUNT(DISTINCT customer_id).
- Denominator: None for an absolute count. For a proportion of all customers, a separate total-customer denominator would be needed.
- Grouping and filters: Same as complaint volume.
- Interpretation: A customer may submit multiple complaints, so complaint count can exceed distinct customer count.

## Average closed-case resolution time
Mean elapsed calendar days from complaint receipt (complaint.received_at) to its first recorded transition to CLOSED (complaint_status_history.changed_at), for complaints that are currently closed.

- Numerator: Sum of the valid individual elapsed durations (in calendar days) for qualifying closed complaints in a category.
- Denominator: Number of qualifying closed complaints in that category (closed_complaint_count). This is not the count of all complaints.
- Calculation: AVG(julianday(closed_at) - julianday(received_at)), rounded to zero decimal.
- Grouping: c.category.
- Filters: csh.new_status = 'CLOSED'.
- Unresolved cases: Open, in-progress, and under-review complaints are excluded from both numerator and denominator. They do not contribute zero-day durations. Categories with no qualifying closed complaints do not appear in the result.

## Data-quality limitations

Synthetic, small dataset: The provided seed data contains ten complaints; the resulting metrics are suitable for query validation, not representative performance benchmarks.


