-- Volume queries :

-- Complaint volume by status, category and month.
-- Distinguish complaint count from distinct customer count.

Select COUNT(complaint_id) as number_of_complaint, COUNT(distinct customer_id) as number_unique_customer, status from complaint
group by status;

Select COUNT(complaint_id) as number_of_complaint, COUNT(distinct customer_id) as number_unique_customer, category from complaint
group by category;

SELECT strftime('%Y-%m', received_at) AS year_month,
    COUNT(*) AS number_of_complaints,
    COUNT(DISTINCT customer_id) AS number_unique_customers
FROM complaint
GROUP BY strftime('%Y-%m', received_at)
ORDER BY year_month;

-- Resolution measures queries :

-- Average closed-case resolution days by category.
Select c.complaint_id, c.received_at , csh.changed_at,  ROUND(AVG(julianday(csh.changed_at) - julianday(c.received_at)),0) AS avg_duration_days, c.category 
from complaint c
Join complaint_status_history csh
On c.complaint_id =	csh.complaint_id
Where csh.new_status = 'CLOSED'
group by c.category;