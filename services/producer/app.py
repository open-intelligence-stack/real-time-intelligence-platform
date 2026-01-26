import requests
import json
import time
import os
from kafka import KafkaProducer

# ----------------------------
# Configuration
# ----------------------------

GITHUB_EVENTS_URL = "https://api.github.com/events"
KAFKA_TOPIC = "github_raw_events"
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # optional

def wait_for_kafka(max_seconds: int = 90, sleep_seconds: int = 2) -> None:
    deadline = time.time() + max_seconds
    last_err = None

    while time.time() < deadline:
        try:
            p = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
            p.close()
            print(f"Kafka is ready at {KAFKA_BOOTSTRAP_SERVERS}")
            return
        except Exception as e:
            last_err = e
            print(f"Waiting for Kafka at {KAFKA_BOOTSTRAP_SERVERS}... ({e})")
            time.sleep(sleep_seconds)

    raise RuntimeError(f"Kafka not ready after {max_seconds}s: {last_err}")

wait_for_kafka()

# ----------------------------
# Kafka Producer setup
# ----------------------------

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

# ----------------------------
# Fetch data from GitHub (with ETag support)
# ----------------------------

last_etag = None

def fetch_github_events():
    global last_etag

    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    if last_etag:
        headers["If-None-Match"] = last_etag

    response = requests.get(GITHUB_EVENTS_URL, headers=headers, timeout=10)

    if response.status_code == 304:
        return []  # nothing new

    response.raise_for_status()

    last_etag = response.headers.get("ETag")
    return response.json()

# ----------------------------
# Main loop
# ----------------------------

def main():
    print("Starting GitHub → Kafka producer...")

    while True:
        try:
            events = fetch_github_events()

            if not events:
                print("No new events.")
            else:
                for event in events:
                    producer.send(KAFKA_TOPIC, event)
                    print(f"Produced event: {event.get('type')}")

                producer.flush()

            time.sleep(60)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

# ----------------------------
# Entry point
# ----------------------------

if __name__ == "__main__":
    main()
