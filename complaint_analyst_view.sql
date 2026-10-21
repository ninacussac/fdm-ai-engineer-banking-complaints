-- Create complaint_analyst_view containing only justified fields.
Select c.complaint_id , c.customer_id , c.account_id, a.account_type, c.category, c.status, c.priority
From complaints c 
Inner Join customers c2 
On c.customer_id = c2.customer_id 
Left Join accounts a 
On a.account_id = c.account_id
where c.status <> 'Closed';