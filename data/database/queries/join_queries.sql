-- Show each complaint with customer name.

Select c2.first_name as first_name, c2.last_name as last_name, c.* 
From complaints c 
Inner Join customers c2 
On c.customer_id = c2.customer_id ;

-- Add optional account type without dropping complaints that have no account.

Select c2.first_name as first_name, c2.last_name as last_name, a.account_type as account_type, c.* 
From complaints c 
Inner Join customers c2 
On c.customer_id = c2.customer_id 
Left Join accounts a 
On a.account_id = c.account_id ;

-- Verify distinct complaint count before and after joins.

Select count(Distinct complaint_id) as unique_complaint_id
From complaints c;

Select count(*), count(Distinct complaint_id)
From complaints c 
Inner Join customers c2 
On c.customer_id = c2.customer_id; 

Select count(*), count(Distinct complaint_id)
From complaints c 
Inner Join customers c2 
On c.customer_id = c2.customer_id 
Left Join accounts a 
On a.account_id = c.account_id ;





