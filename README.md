# Real-Time Intelligence Platform

A collaborative project to build a production-style real-time data + AI system using:
- Kafka (event-driven architecture)
- Streaming pipelines
- FastAPI backend
- RAG (Retrieval Augmented Generation)
- Agentic AI workflows
- Fully reproducible local environment (Docker)

## Goals
- Learn real-world data engineering (Kafka, async, streaming)
- Learn AI engineering (RAG, embeddings, vector search)
- Learn agent systems (tool use, orchestration, reasoning)
- Build a portfolio-grade project

## Architecture (high-level)

[ Live Data Source ]
        ↓
    Kafka Topics
        ↓
 Stream Processing Services
        ↓
     Storage (DuckDB/Postgres)
        ↓
    FastAPI Backend
        ↓
   AI Layer (RAG + Agents)
        ↓
     Dashboard / API Consumers

## Repo Structure
See `/docs/architecture.md` for detailed design.

## Team Workflow
- Feature branches only
- PR reviews before merge
- Issues used for task tracking

## Status
Phase 1: Repo + architecture setup
