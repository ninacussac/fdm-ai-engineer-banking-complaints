-- AGE bucket query 

-- Use CASE for unresolved age buckets 0-7, 8-30 and 31+ days.
Select complaint_id, CASE
    WHEN CAST(JULIANDAY('now')-JULIANDAY(c.received_at)AS INTEGER) Between 0 AND 7 THEN '0-7 days'
    WHEN CAST(JULIANDAY('now')-JULIANDAY(c.received_at)AS INTEGER) Between 8 AND 30 THEN '8-30 days'
    ELSE '31+ days'
  END AS age_bucket, 
 CAST(JULIANDAY('now')-JULIANDAY(c.received_at)AS INTEGER) as time_bucket
from complaint c 
where c.status <> "CLOSED";

-- Test with different time (not 'now' as in the previous query)
-- Test for limit 7 and 30
Select complaint_id, CASE
    WHEN CAST(JULIANDAY('2025-02-01 08:45:00')-JULIANDAY(c.received_at) AS INTEGER) Between 0 AND 7 THEN '0-7 days'
    WHEN CAST(JULIANDAY('2025-02-01 08:45:00')-JULIANDAY(c.received_at) AS INTEGER) Between 8 AND 30 THEN '8-30 days'
    ELSE '31+ days'
  END AS age_bucket, 
  CAST(JULIANDAY('2025-02-01 08:45:00')-JULIANDAY(c.received_at) AS INTEGER) as time_bucket,
  c.received_at 
from complaint c 
where c.status <> "CLOSED";

-- test for 8 and 31
Select complaint_id, CASE
    WHEN CAST(JULIANDAY('2025-02-02 08:45:00')-JULIANDAY(c.received_at) AS INTEGER) Between 0 AND 7 THEN '0-7 days'
    WHEN CAST(JULIANDAY('2025-02-02 08:45:00')-JULIANDAY(c.received_at) AS INTEGER) Between 8 AND 30 THEN '8-30 days'
    ELSE '31+ days'
  END AS age_bucket, 
  CAST(JULIANDAY('2025-02-02 08:45:00')-JULIANDAY(c.received_at) AS INTEGER) as time_bucket,
  c.received_at 
from complaint c 
where c.status <> "CLOSED";

-- Use a CTE to identify repeat complainants.

WITH repeat_complainants AS ( 
Select 
c.customer_id,
c.complaint_id, 
c.status, 
c.category,
RANK() OVER (
PARTITION BY c.customer_id 
order by complaint_id
) as complaint_rank
from complaint c 
)
Select customer_id, complaint_rank as number_of_complaint from repeat_complainants
group by customer_id
having max(complaint_rank) > 1;

-- Use ROW_NUMBER to select latest status per complaint.
WITH complaint_evolution AS ( 
Select 
csh.complaint_id, 
csh.new_status, 
csh.changed_at,
ROW_NUMBER() OVER (
PARTITION BY csh.complaint_id  
order by csh.changed_at DESC
) as complaint_rank
from complaint_status_history csh
)
Select complaint_id, new_status as latest_status from complaint_evolution ce1
where complaint_rank = 1;


-- Rank customers by complaint count.
Select customer_id, COUNT(*) as number_of_complaint from complaint c 
group by customer_id
order by number_of_complaint DESC;