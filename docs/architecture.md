# System Architecture

This project is built as a modular event-driven system.

## Services

- producer  
  Ingests real-time data (WebSocket / API) and publishes to Kafka

- processor  
  Consumes Kafka events, performs transformations and analytics

- api  
  Exposes REST endpoints over processed data

- agents (future)  
  LLM-based agents using tools over the system

## Core Technologies
- Kafka (Docker local)
- FastAPI
- Python AsyncIO
- DuckDB or Postgres
- FAISS (later for vector search)
- Local LLMs (later via Ollama)

## Design Principles
- Reproducible locally
- No paid infrastructure dependency
- Clear service boundaries
- Production-style architecture
