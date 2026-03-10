# Unbiased India News - Strategic Roadmap

This document outlines the current production capabilities and future engineering milestones for the Unbiased India News platform.

---

## Technical Pipeline Flow

```text
[ Data Sources ]
       |
       | (Parallel Fetch)
       v
[ Ingestion Coordinator ] ----> [ Deduplication ] ----> [ Full-Text Extraction ]
                                                               |
                                                               v
+--------------------------------------------------------------+
|                                                              |
|   [ Scout Node ] --------> [ Summarizer ] --------> [ Auditor Node ]
|   (Clustering)             (Gemini Flash)           (Gemini Pro)
|        ^                                                 |
|        |                                                 v
|        +------------------ [ Editor Node ] <-------------+
|                      (Blindspot Detection & Loop)
|                                |
+--------------------------------+
                                 |
                                 v
                  [ Repository & Persistence Layer ]
                                 |
                +----------------+----------------+
                |                                 |
         [( SQLite DB )]                 [ Markdown Reports ]
```

---

## Current Production Foundations

### Ingestion and Data Quality
- Triple-Track Discovery: Parallelized fetching via RSS, Sitemap XML, and Homepage Spiders.
- High-Volume Scaling: Implementation of semaphores for high-concurrency article processing.
- Deep Extraction: Integrated Trafilatura for sanitized article body retrieval.
- Pre-Clustering Deduping: URL and Title-level filtering to optimize token usage.

### Agentic Intelligence
- Live AI Reasoning: Multi-agent flow utilizing Gemini 1.5 Pro and Flash.
- LLM Caching: Persistence of AI responses via SQLiteCache to minimize operational costs.
- Rate Limiting: Concurrency management via global semaphores to ensure API stability.
- State persistence: Asynchronous LangGraph checkpointing for workflow recovery.

### Engineering and DevOps
- Dockerization: Multi-stage, CPU-optimized container builds using Python 3.12.
- Universal Configuration: Centralized YAML management with environment variable overrides.
- CI/CD: Automated GitHub Action workflows with HuggingFace model caching.

---

## Medium Term: Expansion (Q3 2026)

- Regional Sitemap Expansion (Issue #4): Implement sitemap discovery for additional regional languages including Tamil and Telugu.
- Automated Accuracy Evaluation (Issue #5): Integrate a Judge LLM (GPT-4o) into the evaluation suite.
- Semantic Deduplication (Issue #9): Implement vector-based pre-clustering deduplication to catch near-duplicate headlines.
- Database Migrations (Issue #10): Integrate Alembic to manage SQLAlchemy schema changes without data loss.
- Ideological Mirror Agent (Issue #17): Add specialized agent to stress-test analysis via counter-narrative reasoning.
- Fact-Checking & Credibility (Issue #22): Integrate with Fact-Checking APIs to cross-reference claims and weight source credibility.
- Hallucination Detection (Issue #23): Implement automated self-reflection grounding checks to ensure summaries strictly adhere to extracted facts.

## Long Term: Platform Growth (2027)

- Vector Story Tracking (Issue #6): Implement a vector database (e.g. ChromaDB) to track story evolution.
- REST API Layer (Issue #7): Develop a FastAPI-based service to expose daily report data to external frontends.
- Real-time Notifications (Issue #8): Implement an alerting utility for high-priority coverage blindspots.
- Workflow Observability (Issue #11): Integrate LangSmith for deep visual debugging of LangGraph flows.
- Ethical Scraping Compliance (Issue #24): (Completed) Integrated robots.txt parser and per-domain rate limiting logic.
- Human-in-the-Loop Workflow (Issue #25): Implement an interrupt-and-review system for high-polarization stories.
