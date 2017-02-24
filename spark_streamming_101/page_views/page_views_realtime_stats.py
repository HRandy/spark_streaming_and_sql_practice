from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

# Functions for DStraem operators
def count_stats(iter):
  total = 0
  uu = set()
  for uid in iter:
    total = total + 1
    uu.add(uid)
  return (total, len(uu))

# Initialize SparkContext and StreamingContext
conf = SparkConf().setAppName("page viewed")
sc = SparkContext()
ssc = StreamingContext(sc, 10)

# Create a DStream from Kafaka "page_views" topic and apply window to the stream
page_view_stream = KafkaUtils.createStream(ssc, "localhost:2181", "consumer-group", {"page_views_logs_stream": 1})
lines = page_view_stream.map(lambda (k,v): v).window(60,10)

# Count how many visits and unique users for each page
page_user = lines.map(lambda x: (x.split("\t")[3], x.split("\t")[1]))
page_uucount_total = page_user.groupByKey().map(lambda (x,y): (x,count_stats(y)))

# Print the result
page_uucount_total.pprint()

# Start it
ssc.start()
ssc.awaitTermination()


