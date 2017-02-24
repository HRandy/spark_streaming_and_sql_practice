from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Create a local StreamingContext with two working thread and batch interval of 1 second
sc = SparkContext("local[2]", "WindowedNetworkWordCount")
ssc = StreamingContext(sc, 1)

# Create a DStream that will connect to hostname:port, like localhost:9999
lines = ssc.socketTextStream("localhost", 9999)
lines_windowed = lines.window(20,10) # process last 20 seconds of data, every 10 seconds

# Split each line into words
words = lines_windowed.flatMap(lambda line: line.split(" "))

# Count each word in each batch
pairs = words.map(lambda word: (word, 1))
wordCounts = pairs.reduceByKey(lambda x, y: x + y)

# Print the first ten elements of each RDD generated in this DStream to the console
wordCounts.saveAsTextFiles("file:///home/cloudera/Desktop/out/")

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate


