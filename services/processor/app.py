import json
from kafka import KafkaConsumer

# ----------------------------
# Configuration
# ----------------------------

KAFKA_TOPIC = "github_raw_events"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

# ----------------------------
# Kafka Consumer setup
# ----------------------------

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest",  # read from beginning if first run
    enable_auto_commit=True,
)

print("Listening for GitHub events from Kafka...")

# ----------------------------
# Main loop (stream consumption)
# ----------------------------

for message in consumer:
    event = message.value
    event_type = event.get("type")
    repo_name = event.get("repo", {}).get("name")

    print(f"Consumed event: {event_type} | Repo: {repo_name}")
