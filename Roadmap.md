# Unbiased India News - Strategic Roadmap

This document outlines the current production capabilities and future engineering milestones for the Unbiased India News platform.

---

## Technical Pipeline Flow

```mermaid
flowchart TD
    subgraph STAGE_1 ["1. DISCOVERY"]
        direction LR
        RSS([RSS])
        XML([Sitemap])
        WEB([Spider])
    end

    subgraph STAGE_2 ["2. PRE-PROCESSING"]
        IC{{"Coordinator"}}
        DDP["Deduplication"]
        FTE["Extraction"]
    end

    subgraph STAGE_3 ["3. AGENTIC ANALYSIS"]
        direction TB
        SN[["Scout"]]
        SUM[["Summarizer"]]
        AUD[["Auditor"]]
        ED[["Editor"]]
    end

    subgraph STAGE_4 ["4. PERSISTENCE"]
        direction LR
        REPO["Repository"]
        SQL[("SQLite DB")]
        MD["Markdown"]
    end

    %% Flow Connections
    STAGE_1 ==> IC
    IC --> DDP --> FTE
    FTE ==> SN
    SN --> SUM --> AUD --> ED
    ED -.->|Loop| SN
    ED ==> REPO
    REPO --> SQL & MD

    %% Dark-Mode Friendly Technical Styling
    classDef stage fill:none,stroke:#8b949e,stroke-width:2px,stroke-dasharray: 5 5,color:#8b949e;
    classDef item fill:#161b22,stroke:#58a6ff,stroke-width:2px,color:#58a6ff;
    classDef ai fill:#161b22,stroke:#ea4335,stroke-width:2px,color:#ea4335;

    class STAGE_1,STAGE_2,STAGE_3,STAGE_4 stage;
    class RSS,XML,WEB,IC,DDP,FTE,REPO,SQL,MD item;
    class SN,SUM,AUD,ED ai;
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
- Automated Accuracy Evaluation (Issue #5): Integrate a Judge LLM (GPT-4o) into the evaluation suite to provide automated bias scoring benchmarks.

## Long Term: Platform Growth (2027)

- Vector Story Tracking (Issue #6): Implement a vector database (e.g. ChromaDB) to track story evolution over multiple months.
- REST API Layer (Issue #7): Develop a FastAPI-based service to expose daily report data to external frontends.
- Real-time Notifications (Issue #8): Implement an alerting utility for high-priority coverage blindspots.
