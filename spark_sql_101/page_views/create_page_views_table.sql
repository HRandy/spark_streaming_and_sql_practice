CREATE EXTERNAL TABLE page_views 
(
  logtime STRING, 
  userid INT, 
  ip STRING, 
  page STRING, 
  ref STRING, 
  os STRING, 
  os_ver STRING, 
  agent STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LOCATION '/user/cloudera/spark_sql_101/page_views/data';

