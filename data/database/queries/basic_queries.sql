Select * from complaint
where status = 'OPEN';

Select * from complaint
WHERE priority IN ('High', 'Critical')
AND status <> 'CLOSED';

Select status as Status_type, COUNT(*) as Number_of_complaint from complaint
Group by status;

Select category as category_type, COUNT(*) as Number_of_complaint from complaint
Group by category;

Select * from complaint
where customer_id = 'CUS003';

Select *
From complaint
where received_at >= '2026-10-20'
AND   received_at< '2026-10-21'
ORDER BY received_at;

Select c.* , csh.changed_at as date
From complaint c
Join complaint_status_history csh
ON c.complaint_id = csh.complaint_id
where csh.new_status = 'CLOSED' AND csh.changed_at IS NULL;

SELECT *
FROM complaint
ORDER BY received_at DESC, complaint_id DESC
LIMIT 10;