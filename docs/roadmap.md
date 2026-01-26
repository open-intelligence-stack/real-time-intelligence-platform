### 2026-01-26

* Refactored shared Pydantic contracts into `services/common/models.py` and imported them across services (no model duplication).
* Implemented Enricher service (Phase 2) consuming `github_clean_events` and producing `github_enriched_events` using `EnrichedGitHubEventV1` derived from the canonical contract.
* Stabilized Kafka consumption by introducing consumer `group_id` values (processor/enricher) to prevent replaying the full topic on every restart.
* Containerized the platform and orchestrated services via Docker Compose:
  * Added producer / processor / enricher services to `docker-compose.yml` alongside Kafka/Zookeeper.
  * Introduced dual Kafka listeners for local + container networking (`localhost:9092` and `kafka:29092`).
  * Standardized bootstrap server configuration via `KAFKA_BOOTSTRAP_SERVERS` environment variable.
* Fixed Docker runtime startup reliability:
  * Added Kafka readiness wait/retry in Python services to avoid early-connection exits during broker initialization.
  * Set `PYTHONPATH=/app` inside the Docker image to ensure `services.*` imports work consistently.
* Verified end-to-end pipeline running fully in Docker:
  * Producer → `github_raw_events`
  * Processor → `github_clean_events`
  * Enricher → `github_enriched_events`