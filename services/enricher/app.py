import json
import os
import time
from kafka import KafkaConsumer, KafkaProducer

from services.common.models import CanonicalGitHubEvent
from services.enricher.models import enrich_event

# ----------------------------
# Configuration
# ----------------------------

CLEAN_TOPIC = "github_clean_events"
ENRICHED_TOPIC = "github_enriched_events"
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

# ----------------------------
# Kafka Consumer setup (clean topic)
# ----------------------------

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

consumer = KafkaConsumer(
    CLEAN_TOPIC,
    group_id="enricher-v1",
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
)

# ----------------------------
# Kafka Producer setup (enriched topic)
# ----------------------------

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

print("Enricher started: listening on clean topic and producing enriched events...")

# ----------------------------
# Main loop
# ----------------------------

for message in consumer:
    clean_dict = message.value

    try:
        # Validate clean event against schema
        clean_event = CanonicalGitHubEvent.model_validate(clean_dict)

        # Enrich event
        enriched_event = enrich_event(clean_event)

        # Serialize for Kafka
        enriched_dict = enriched_event.model_dump(mode="json")

        # Produce to Kafka
        producer.send(ENRICHED_TOPIC, value=enriched_dict)
        producer.flush()

        print(
            f"Produced enriched event: "
            f"{enriched_dict['event_type']} | "
            f"{enriched_dict['repo_name']} | "
            f"{enriched_dict['activity_domain']}/{enriched_dict['activity_action']}"
        )

    except Exception as e:
        print("Enrichment failed, event skipped:")
        print(e)
