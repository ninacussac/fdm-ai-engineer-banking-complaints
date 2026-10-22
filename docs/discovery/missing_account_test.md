# Verify a complaint without account_id stays visible : 
With the previous data we have we can't verify that because all complaints have an associated account_id.

Using data from the shared documents containing more than 10 records, we can confirm that the query works as expected, as complaints without an account_id are still included in the results.
<img src="./images/test_missing_account.png" width="600">