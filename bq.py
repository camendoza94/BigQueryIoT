from google.cloud import bigquery
from datetime import datetime
import paho.mqtt.publish as publish

client = bigquery.Client()
query_job = client.query("""
	SELECT
	  location,
	  country,
	  value,
	  latitude,
	  longitude,
	  EXTRACT(DATETIME FROM timestamp) as time
	FROM `bigquery-public-data.openaq.global_air_quality`
	WHERE pollutant = "pm10" AND EXTRACT(DATE FROM timestamp) = CURRENT_DATE()
	ORDER BY timestamp desc""")

results = query_job.result()  # Waits for job to complete.

for row in results:
	location = row.location
	value = row.value
	timestamp = datetime.fromisoformat(str(row.time))
	print(row.time)
	print(timestamp)
	print("location: {}, value: {}, timestamp: {}".format(location.encode("utf-8"), value, timestamp))
	publish.single("iot/air", value, hostname="localhost")