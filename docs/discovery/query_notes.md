# Document choices

## Filter choice : 

Select * from complaint 
where status = 'OPEN';

This query uses a WHERE clause to filter the complaint table and retrieve only complaints with the status OPEN.
The equality operator (=) ensures that only records matching this exact status are returned. This filter is useful for identifying complaints that are still open and may require further processing by the AI agent.
Using SELECT * returns all columns, allowing us to inspect the complete complaint records during database exploration.

## Date condition choice :

Select c.* , csh.changed_at as date 
From complaint c 
Join complaint_status_history csh 
ON c.complaint_id = csh.complaint_id 
where csh.new_status = 'OPEN' AND csh.changed_at BETWEEN '2026-10-20' AND '2026-10-21';

This query retrieves complaints whose status changed to OPEN within a specified date range.
A JOIN is used to connect the complaint table with complaint_status_history through their shared complaint_id. This allows us to access the status change timestamps, which are stored separately from the main complaint records.
The BETWEEN operator filters records within the specified period, including both boundary values.

## Null-Handling choice :


Select c.* , csh.changed_at as date 
From complaint c 
Join complaint_status_history csh 
ON c.complaint_id = csh.complaint_id 
where csh.new_status = 'CLOSED' AND csh.changed_at IS NULL;

This query attempts to identify complaints that have a recorded status change to CLOSED but do not have a corresponding timestamp.
The IS NULL condition is used instead of = NULL because SQL requires IS NULL to test for missing values.