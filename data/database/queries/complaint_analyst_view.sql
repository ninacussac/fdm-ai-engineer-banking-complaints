-- Create complaint_analyst_view containing only justified fields.
CREATE VIEW complaint_analyst_view AS
Select c.complaint_id , c.customer_id , c.account_id, a.account_type, c.category, c.status, c.priority
From complaint c 
Inner Join customer c2 
On c.customer_id = c2.customer_id 
Left Join account a 
On a.account_id = c.account_id
where c.status <> 'CLOSED';