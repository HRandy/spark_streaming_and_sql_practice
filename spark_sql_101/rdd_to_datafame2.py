from pyspark import SparkConf, SparkContext
from pyspark.sql import *
from pyspark.sql.types import *

conf = SparkConf().setAppName("test Spark SQL")
sc = SparkContext(conf = conf)

sqlContext = SQLContext(sc)

# Load a text file and convert each line to a Row.
lines = sc.textFile("file:///home/cloudera/Desktop/spark_sql_101/data/people.txt")
parts = lines.map(lambda l: l.split(","))
people = parts.map(lambda p: (p[0], p[1].strip()))

# The schema is encoded in a string.
schemaString = "name age"

fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
schema = StructType(fields)

# Apply the schema to the RDD.
schemaPeople = sqlContext.createDataFrame(people, schema)

# Register the DataFrame as a table.
schemaPeople.registerTempTable("people")

# SQL can be run over DataFrames that have been registered as a table.
results = sqlContext.sql("SELECT name FROM people")

# The results of SQL queries are RDDs and support all the normal RDD operations.
names = results.map(lambda p: "Name: " + p.name)
for name in names.collect():
  print name


