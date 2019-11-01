# ecb_aws_exchange
The file **lambda_test.py**  is an simple file to test db_access.  
Code pushed to aws_lambda via the deployment-package **lambda.zip**

This [package](https://github.com/jkehler/awslambda-psycopg2) was used to run the psycopg2 library on aws_lambda
---

To access the postgres database by another application use the following credentials:

HOST: database-ecb.cxkslz20bb7r.eu-central-1.rds.amazonaws.com  
PORT: 5432  
database: postgres  
user: openview  
password: postgres_free  


---


This might require you to install the following:

sudo apt-get install postgresql postgresql-contrib

