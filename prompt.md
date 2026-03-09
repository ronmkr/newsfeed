# Master Context: Building "Unbiased India News"

This document contains the foundational context and technical mandates required to build a production-grade, agentic news aggregation and analysis platform from the ground up.

---

## 1. Project Objective
Build a daily batch pipeline that fetches, clusters, and analyzes news from the Indian media landscape. The goal is to reveal ideological framing and provide transparency regarding publisher ownership.

## 2. Core Architecture Mandates
- **Framework:** Use **LangGraph** for a cyclic, multi-agent workflow.
- **Language:** Python 3.11+.
- **Design Pattern:** Modular and decoupled. Use the **Repository Pattern** for database access and **Service-based** logic for NLP tasks.
- **Asynchronicity:** Every I/O operation (Network, DB, LLM) must be `async`. CPU-bound tasks (Clustering) must be offloaded to `asyncio.to_thread`.
- **Configuration:** Externalize settings in `config.yaml` and static metadata in `data/source_kb.json`.

## 3. Module Specifications

### A. Triple-Track Ingestion
- **RSS Track:** Poll verified feeds.
- **Sitemap Track:** Parse `sitemap.xml` for highly reliable link discovery.
- **Spider Track:** Fallback HTML scraper for sites with blocked feeds.
- **Sanitization:** Implement heuristic filters to discard "Cookie Walls," error pages, and content under 300 characters.
- **Deduplication:** Filter by URL and normalized Title similarity before processing.

### B. NLP & Clustering
- **Embeddings:** Use **FastEmbed (ONNX)** with the `BAAI/bge-small-en-v1.5` or `multilingual-e5` model to ensure the Docker image remains under 1GB.
- **Algorithm:** Implement Agglomerative Clustering using a precomputed cosine similarity distance matrix.
- **Cross-Lingual:** Ensure the vector space supports grouping articles across different Indian languages.

### C. Agentic Workflow (LangGraph Nodes)
- **Node 1 (Scout):** Coordinates clustering and enriches articles with ownership metadata from the JSON KB.
- **Node 2 (Summarizer):** Uses **Gemini 1.5 Flash** to generate neutral 3-bullet summaries.
- **Node 3 (Auditor):** Uses **Gemini 1.5 Pro** to analyze bias, framing, and adjective density.
- **Node 4 (Editor):** Checks for "Blindspots" (e.g., stories covered only by one ideological side).
- **Concurrency:** Implement an `asyncio.Semaphore` to rate-limit parallel LLM calls.

### D. Persistence & Reporting
- **Database:** Use **SQLAlchemy** with **SQLite**. Store full reasoning traces ("Chain of Thought") for every AI analysis.
- **Checkpointing:** Use `AsyncSqliteSaver` to persist LangGraph state for crash recovery.
- **LLM Caching:** Implement `SQLiteCache` to save costs on redundant API calls.
- **Output:** Automatically generate a daily Markdown report (`DAILY_REPORT.md`) with a summary table and bias emojis.

## 4. Engineering Standards
- **Functional Coding:** Use list comprehensions, mapping, and reusable helpers instead of nested imperative loops.
- **Type Safety:** Enforce strict Python type hinting across all modules.
- **Documentation:** Use Google-style docstrings for every class and method.
- **DevOps:** Create a multi-stage `Dockerfile` (optimized for CPU) and a GitHub Action for automated 8:00 AM IST runs.

---

## 5. Development Strategy (The Prompts)

### Step 1: Ingestion Foundation
"Build an asynchronous Ingestion Module that fetches data from RSS feeds, Sitemaps, and Homepages in parallel. Implement strict deduplication based on URL/Title and add a full-text extractor using Trafilatura. Sanitize content to remove junk text."

### Step 2: Clustering Engine
"Implement a Clustering Service using FastEmbed (ONNX). Create an algorithm that groups articles into story clusters based on semantic similarity. Ensure it handles cross-lingual comparisons."

### Step 3: Agentic Graph
"Set up a LangGraph workflow with four nodes: Scout, Summarizer, Auditor, and Editor. Map Gemini 1.5 Flash for summaries and Gemini 1.5 Pro for auditing. Implement a global semaphore for rate limiting and AsyncSqliteSaver for state persistence."

### Step 4: Storage & Reporting
"Implement the Repository Pattern using SQLAlchemy. Save analyzed clusters, articles, and AI reasoning traces. Create a utility that exports the database findings into a daily Markdown report with a summary table."

### Step 5: Optimization
"Dockerize the application using a multi-stage build. Implement LLM response caching via SQLiteCache. Ensure all configuration is loaded from a config.yaml that can be overridden at runtime."

### Step 6: Compliance and Monitoring
"Implement a final analytics logging step that summarizes articles processed, clusters formed, and blindspots found. Add a legal disclaimer to the project documentation regarding fair use and automated data sourcing."
