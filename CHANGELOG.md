### What needs to be done

* sqlite3 Chinese display problem
* daily cost view in a month
* view default_values/currencies table
* "/view" total balances (month/year view, whole)

### What has been done in v0.2

* 2014-09-24  
  change server back to bottle default server  
  add function: deleting tally entries

* 2014-09-21  
  Try to use apache with bottle but failed  
  change server to CherryPyServer instead

* 2014-09-20  
  use a function decorate to do db transactions so that it commits after every operation

### What has been done in v0.1

* 2014-09-18  
  add function: deleting currencies

* 2014-09-17  
  add function: adding new currencies

* 2014-09-16  
  fixed the bug that "/view" cost column only displays integers  
  shows "/view" in date descending order  
  "/view" total rows show monthly income, expenses and balance  
  added the function that can change default currency

* 2014-09-14  
  add function that can change default number of rows in one db insertion

### What has been done in version 0.0

* 2014-09-13  
  test inputs before inserting them into db

* 2014-09-11  
  Can insert records into db  
  Can view records as a table