import requests
import json
import time
from kafka import KafkaProducer

# ----------------------------
# Configuration
# ----------------------------

GITHUB_EVENTS_URL = "https://api.github.com/events"
KAFKA_TOPIC = "github_raw_events"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

# ----------------------------
# Kafka Producer setup
# ----------------------------

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

# ----------------------------
# Fetch data from GitHub
# ----------------------------

def fetch_github_events():
    response = requests.get(GITHUB_EVENTS_URL, timeout=10)
    response.raise_for_status()  # crash if GitHub gives 4xx/5xx
    return response.json()

# ----------------------------
# Main loop (streaming behavior)
# ----------------------------

def main():
    print("Starting GitHub → Kafka producer...")

    while True:
        try:
            events = fetch_github_events()

            for event in events:
                producer.send(KAFKA_TOPIC, event)
                print(f"Produced event: {event.get('type')}")

            producer.flush()
            time.sleep(5)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

# ----------------------------
# Entry point
# ----------------------------

if __name__ == "__main__":
    main()
