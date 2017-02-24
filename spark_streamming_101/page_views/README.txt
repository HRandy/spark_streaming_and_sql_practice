
# start kafka server

cd ~/Desktop/spark_streamming_101/page_views/kafka_2.11-0.10.0.0/
bin/kafka-server-start.sh config/server.properties

# create topic: page_views_logs_stream

cd ~/Desktop/spark_streamming_101/page_views/kafka_2.11-0.10.0.0/
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic page_views_logs_stream

# consumer
# caculate unique user count of each page from page_views logs stream using spark streaming

cd ~/Desktop/spark_streamming_101/page_views/

spark-submit page_views_realtime_stats.py


# producer
# simulate page_views logs data streams

cd ~/Desktop/spark_streamming_101/page_views/kafka_2.11-0.10.0.0/

cat ../page_views_logs/* | bin/kafka-console-producer.sh --broker-list localhost:9092 --topic page_views_logs_stream


# consumer
# get data from page_views stream and store it in a staging file

cd ~/Desktop/spark_streamming_101/page_views/kafka_2.11-0.10.0.0/

bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic page_views_logs_stream > ../staging/page_views_logs.staging


