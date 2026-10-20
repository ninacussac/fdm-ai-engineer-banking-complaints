Select * from complaint 
where status = 'OPEN';

Select * from complaint
where priority =  'High' AND status <> 'CLOSED';

Select status as Status_type, COUNT(*) as Number_of_complaint from complaint 
Group by status;

Select category as category_type, COUNT(*) as Number_of_complaint from complaint 
Group by category;

Select * from complaint
where customer_id = 'CUS003';

Select c.* , csh.changed_at as date 
From complaint c 
Join complaint_status_history csh 
ON c.complaint_id = csh.complaint_id 
where csh.new_status = 'OPEN' AND csh.changed_at BETWEEN '2026-10-20' AND '2026-10-21';

Select c.* , csh.changed_at as date 
From complaint c 
Join complaint_status_history csh 
ON c.complaint_id = csh.complaint_id 
where csh.new_status = 'CLOSED' AND csh.changed_at IS NULL;

Select c.* , csh.changed_at as date 
From complaint c 
Join complaint_status_history csh 
ON c.complaint_id = csh.complaint_id 
where csh.new_status = 'OPEN' 
ORDER BY date DESC
LIMIT 10;