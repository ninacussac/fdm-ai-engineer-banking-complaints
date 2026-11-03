
-- Create a view containing the relevant fields
-- for unresolved complaints.

CREATE VIEW IF NOT EXISTS complaint_analyst_view AS

SELECT
    c.complaint_id,
    c.customer_id,
    c.account_id,
    a.account_type,
    c.category,
    c.status,
    c.priority

FROM complaint c

INNER JOIN customer cu
    ON c.customer_id = cu.customer_id

LEFT JOIN account a
    ON c.account_id = a.account_id

WHERE c.status <> 'CLOSED';