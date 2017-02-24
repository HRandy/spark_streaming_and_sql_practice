from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext

conf = SparkConf().setAppName("test Spark SQL")
sc = SparkContext(conf = conf)

hiveCtx = HiveContext(sc)
hiveCtx.sql("CREATE TEMPORARY FUNCTION revs AS 'com.iii.udf.MyReverse'")

rows = hiveCtx.sql("SELECT os, revs(os) as rev_os FROM page_views")
rows.show()



