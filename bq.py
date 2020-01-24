from google.cloud import bigquery
from datetime import datetime
import paho.mqtt.publish as publish
import websockets
import asyncio
import sys
import argparse

def main():
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
		WHERE pollutant = "pm10" AND EXTRACT(DATE FROM timestamp) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
		ORDER BY timestamp desc""")

	results = query_job.result()

	for row in results:
		location = row.location
		value = row.value
		timestamp = datetime.fromisoformat(str(row.time))
		print(row.time)
		print(timestamp)
		print("location: {}, value: {}, timestamp: {}".format(location.encode("utf-8"), value, timestamp))
		if sys.argv[1] == "--mqtt":
			publish.single("iot/air", "location: {}, value: {}, timestamp: {}".format(location.encode("utf-8"), value, timestamp), hostname="localhost")
		elif sys.argv[1] == "--ws":
			asyncio.get_event_loop().run_until_complete(send_websocket("location: {}, value: {}, timestamp: {}".format(location.encode("utf-8"), value, timestamp)))

async def send_websocket(data):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send(data)
        print(f"< {data}")

if __name__ == '__main__':
	if sys.argv[1] == "--mqtt" or sys.argv[1] == "--ws":
		main()
	else:
		print("Specify protocol with '--mqtt' or '--ws'")