# Real-Time GitHub Intelligence Platform

> A production-style data engineering + AI system built end-to-end for
> deep learning, not demos.

---

## 🎯 Project Goal

Build a **real-time intelligence platform** over GitHub public events
that demonstrates:

* Event-driven architecture (Kafka)
* Data modeling and schema design
* Stream processing (validation, enrichment, aggregation)
* Storage layer (analytics-ready data)
* Query + API layer
* Analytics and anomaly detection
* RAG over our own structured data
* Agentic workflows using our own APIs

This project is designed to reflect how **real data platforms are built
in industry**, not tutorials.

---

## 🧠 High-Level Architecture Vision

```
GitHub Public Events (Live)
        ↓
Producer (ingestion service)
        ↓
Kafka Topic: github_raw_events
        ↓
Processor: validation + normalization
        ↓
Kafka Topic: github_clean_events
        ↓
Enrichment & Aggregation processors
        ↓
Storage Layer (DuckDB / Postgres)
        ↓
Query Layer (FastAPI APIs)
        ↓
Analytics (trends, anomalies, summaries)
        ↓
RAG over structured data
        ↓
Agentic workflows (investigator, reporter, monitor)
```

---

## 📂 Repository Structure (Current)

```
real-time-intelligence-platform/
```

├── .venv/
├── data/
│   └── sample/
│       └── README.md
├── docs/
│   ├── architecture.md
│   ├── project_overview.md
│   └── roadmap.md
├── scripts/
│   └── dev.sh
├── services/
│   ├── agents/
│   │   └── placeholder.md
│   ├── api/
│   │   ├── main.py
│   │   └── requirements.txt
│   ├── processor/
│   │   ├── app.py
│   │   ├── models.py
│   │   └── requirements.txt
│   └── producer/
│       ├── app.py
│       └── requirements.txt
├── storage/
│   └── schema.sql
├── .env.example
├── .gitignore
├── docker-compose.yml
├── LICENSE
└── README.md

---

## ✅ Current Status

### Infrastructure

* Docker Desktop installed
* Kafka + Zookeeper running via `docker compose up`
* Verified using `docker ps`

### Python Environment

* Clean Python 3.12 installed

* Project venv created with:

  ```bash
  py -3.12 -m venv .venv
  ```

* SSL / pip issues resolved

### Streaming Pipeline

* Producer working:

  * Fetches events from GitHub public API
  * Produces to Kafka topic: `github_raw_events`
  * Logs: `Produced event: PushEvent`
* Processor working:

  * Consumes from `github_raw_events`
  * Validates using Pydantic data contract
  * Transforms into canonical flat schema
  * Produces validated events into `github_clean_events`
  * Logs: `Produced clean event: PushEvent | Repo: ...`
* Kafka verification completed:

  * Confirmed clean events visible using `kafka-console-consumer` inside Kafka container

This confirms:

> End-to-end multi-stage real-time streaming pipeline is operational.

---

## 🧭 Roadmap

### Phase 0 — Foundations ✅ (Completed)

* Docker
* Kafka
* Producer
* Consumer
* End-to-end streaming confirmed

---

### Phase 1 — Data Understanding & Modeling ✅ (Completed)

**Goal:** Turn raw JSON chaos into a stable internal data contract.

Completed:

* Inspected real GitHub event JSON from live stream
* Identified entities (event, actor, repo, org, time, payload)
* Designed canonical flat schema
* Implemented schema enforcement using Pydantic
* Built processor to transform raw → canonical events
* Created new Kafka topic: `github_clean_events`
* Verified data flow end-to-end using Kafka console consumer

Skills learned:

* Data modeling
* Schema design
* Data contracts
* Validation pipelines
* Kafka multi-stage stream architecture

---

### Phase 2 — Enrichment & Feature Engineering (NEXT)

Planned:

* Add derived fields (is_bot, hour_of_day, day_of_week, repo_owner, etc.)
* Normalize event types (e.g., PushEvent → code_change)
* Apply domain logic for analytics readiness

Skills:

* Stream processing
* Business logic in pipelines
* Data semantics

---

### Phase 3 — Storage Layer

Planned:

* Add Postgres or DuckDB
* Design tables:

  * events
  * repos
  * actors
  * orgs
* Idempotent writes
* Replay/backfill from Kafka

Skills:

* OLTP vs OLAP modeling
* Persistence design
* Backfill strategies

---

### Phase 4 — Query & API Layer

Planned endpoints:

* `/trending-repos`
* `/org/{org}/summary`
* `/repo/{repo}/activity`
* `/actors/top`

Skills:

* FastAPI
* Query modeling
* Turning data into product

---

### Phase 5 — Analytics & Metrics

Planned:

* Trending logic
* Velocity metrics
* Spike detection
* Time-windowed aggregation

Skills:

* Analytical thinking
* Windowing
* Metric systems

---

### Phase 6 — RAG (Retrieval-Augmented Generation)

Planned:

* Build documents from structured data
* Embeddings
* Retrieval
* Grounded question answering

Skills:

* Embeddings
* Chunking
* Retrieval design

---

### Phase 7 — Agentic Systems

Planned:

* Agents using project APIs as tools
* Example agents:

  * Repo Analyst Agent
  * Org Health Agent
  * Anomaly Investigator

Skills:

* Tool-using agents
* Multi-step reasoning
* AI system design

---

## 📌 Current Focus

We are currently at:

> **Phase 2 — Enrichment & Feature Engineering**

Next concrete step:

* Design enriched schema (derived features)
* Decide architecture (extend canonical vs separate enriched model)
* Implement enrichment processor

---

## 🧑‍🏫 Project Principles

* No jumping steps
* Understand *why* before writing code
* Design-first, implementation-second
* Every tool must serve a clear purpose
* Tradeoffs and alternatives discussed explicitly
* Focus on deep understanding over speed

---

## 🗓️ Daily Update Log (Add as you work)

### 2026-01-25

* Confirmed Kafka producer fetching live GitHub events
* Built multi-stage Kafka pipeline (`github_raw_events` → `github_clean_events`)
* Designed and implemented canonical data contract using Pydantic
* Verified clean events via `kafka-console-consumer` inside Kafka container
* Phase 1 officially completed

## Current Status

The platform is now running as a multi-service, multi-stage Kafka pipeline with contract enforcement and enrichment.

### What is working end-to-end

**Streaming pipeline (operational):**
* Producer pulls live GitHub public events and publishes to Kafka topic: `github_raw_events`
* Processor consumes `github_raw_events`, validates + normalizes into a canonical contract, and publishes to: `github_clean_events`
* Enricher consumes `github_clean_events`, derives analytics-ready features, and publishes to: `github_enriched_events`

**Contract + schema discipline:**
* Canonical event contract implemented with Pydantic (`CanonicalGitHubEvent`)
* Enriched contract implemented as an extension of the canonical contract (`EnrichedGitHubEventV1` inherits canonical fields and adds derived features)
* Shared models centralized in `services/common/models.py` to avoid duplication across services

---

## How to Run

### Option A — Docker Compose (recommended)

From project root:

```bash
docker compose up --build
