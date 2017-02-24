from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext
from datetime import datetime
import time

def make_user_logtimeinfo_pairs(row):
  fmt = '%m/%d/%Y %H:%M:%S'
  current_d = datetime.strptime(row.logtime, fmt)
  c_ts = time.mktime(current_d.timetuple())
  return (row.userid, (c_ts,0))

def caculate_timeonsite(acc,logtimeinfo):
  acc_last_logtime = acc[0]
  acc_sum = acc[1]
  if (acc_last_logtime == 0):
    return (logtimeinfo[0],0)
  else:
    acc_sum += logtimeinfo[0] - acc_last_logtime
    acc_last_logtime = logtimeinfo[0]
    return (acc_last_logtime, acc_sum)


if __name__ == "__main__":
  conf = SparkConf().setAppName("time on site")
  sc = SparkContext(conf = conf)
  sqlContext = HiveContext(sc)

  # DataFrame from page_views table
  page_views_sorted = sqlContext.sql("SELECT * FROM page_views ORDER BY userid,logtime ")

  # use rdd in the DataFrame in future processing
  page_views_sorted_rdd = page_views_sorted.rdd

  result = page_views_sorted_rdd.map(make_user_logtimeinfo_pairs).reduceByKey(caculate_timeonsite).map(lambda x: (x[0],x[1][1])).collect()
  print result
