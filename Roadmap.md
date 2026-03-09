# Unbiased India News - Strategic Roadmap

This document outlines the current production capabilities and future engineering milestones for the Unbiased India News platform.

---

## Technical Pipeline Flow

```mermaid
flowchart TD
    subgraph Data_Sources ["1. Multi-Channel Discovery"]
        direction LR
        RSS["RSS Feeds"]
        XML["Sitemaps"]
        HTML["Spiders"]
    end

    subgraph Pre_Processing ["2. Data Normalization"]
        IC["Ingestion Coordinator"]
        DDP["Deduplication"]
        FTE["Full-Text Extraction"]
    end

    subgraph Agentic_Core ["3. Intelligence Layer (LangGraph)"]
        SN["Scout Node<br/>(Semantic Clustering)"]
        SUM["Summarizer<br/>(Gemini Flash)"]
        AUD["Auditor Node<br/>(Gemini Pro)"]
        ED["Editor Node<br/>(Final Validation)"]
    end

    subgraph Persistence ["4. Storage & Reporting"]
        RPL["Repository Layer"]
        SQL[("SQLite DB")]
        MD["Daily Reports"]
    end

    %% Flow
    Data_Sources ==> IC
    IC --> DDP --> FTE
    FTE ==> SN
    SN --> SUM --> AUD --> ED
    ED -.->|Refinement Loop| SN
    ED ==> RPL
    RPL --> SQL & MD

    %% Styling
    classDef layer fill:#f8f9fa,stroke:#202124,stroke-width:2px,font-weight:bold
    classDef item fill:#ffffff,stroke:#4285f4,stroke-width:2px

    class Data_Sources,Pre_Processing,Agentic_Core,Persistence layer
    class RSS,XML,HTML,IC,DDP,FTE,SN,SUM,AUD,ED,RPL,SQL,MD item
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

- Regional Sitemap Expansion: Implement sitemap discovery for additional regional languages including Tamil and Telugu.
- Automated Accuracy Evaluation: Integrate a Judge LLM (GPT-4o) into the evaluation suite to provide automated bias scoring benchmarks.

## Long Term: Platform Growth (2027)

- Vector Story Tracking: Implement a vector database (e.g. ChromaDB) to track story evolution over multiple months.
- REST API Layer: Develop a FastAPI-based service to expose daily report data to external frontends.
- Real-time Notifications: Implement an alerting utility for high-priority coverage blindspots.
