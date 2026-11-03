# Query exploration

## Tables and Counts

### Query : 
![alt text](images/image-16.png)
![alt text](images/image-17.png)
### Result :

![alt text](images/image-18.png)
There are 10 samples in each tables.

## Feature, Data_type, null constraint

### Query : 
![alt text](images/query_data_exploration_type_null.png)

### Account table : 

![alt text](images/image.png)

### Audit_log table :

![alt text](images/image-1.png)

### Complaint table : 
![alt text](images/image-2.png)

### Complaint_status_history table :

![alt text](images/image-3.png)

### Customer table :
![](images/image-4.png)

### Customer_response table : 
![alt text](images/image-5.png)

### Employee table : 
![alt text](images/image-6.png)

### Fee table :

![alt text](images/image-7.png)

### Investigation table : 
![alt text](images/image-8.png)

### Policy_document table :

![alt text](images/image-9.png)

### Policy_section table : 
![alt text](images/image-10.png)

### Recommendation table :
![alt text](images/image-11.png)

### Review_decision table : 
![alt text](images/image-12.png)

### Review_request table :
![alt text](images/image-13.png)

### Service_request table : 
![alt text](images/image-14.png)

### Transactions table :
![alt text](images/image-15.png)

## Observation :

- In the complaint_status_history table, all status changes have identical timestamps. This is unrealistic for a banking environment, where complaints are typically processed and updated at different times.

- A similar issue appears in the audit_log table, where all event_timestamp values are recorded within the same second.

- In the fee table, several records have a NULL value in the transaction_id column.
![alt text](images/image-19.png)
However, this does not necessarily indicate a data quality issue. Some fees, such as account maintenance fees, are applied directly to a customer's account without being linked to a specific transaction.
The database schema explicitly allows transaction_id to be NULL, making this behavior consistent with the current data model.

- The database contains a relatively small number of records, with only 10 customers, 10 accounts, and 10 complaints. It is not representative of a real banking environment.