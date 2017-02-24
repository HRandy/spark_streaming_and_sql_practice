from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext

conf = SparkConf().setAppName("test Spark SQL")
sc = SparkContext(conf = conf)

hiveCtx = HiveContext(sc)
rows = hiveCtx.sql("SELECT os, count(*) as total FROM page_views GROUP BY os ")
rows.show()

