# 📝 Unbiased India News - Development Roadmap

This document tracks the progress of the Unbiased India News agentic pipeline.

---

## 🔴 High Priority (Immediate Actions)

- [x] **Activate LLM Logic:** (Completed) Uncommented `llm.ainvoke()` calls and enabled live AI reasoning.
- [ ] **Real-World Parsing Validation:** Verify that the `RobustJSONParser` correctly handles various edge cases in Gemini's responses once active.

## 🟡 Medium Priority (Expansion & Eval)

- [ ] **Regional Source Expansion:** Add more regional language sitemaps (Hindi, Marathi, Tamil) to `IngestionCoordinator`.
- [ ] **Judge LLM (GPT-4o) Integration:** Automate `tests/evals/runner.py` by integrating a "Judge" LLM to evaluate Auditor accuracy.

## 🔵 Good to Have (Future Enhancements)

- [ ] **Vector Database (Story Tracking):** Integrate ChromaDB or Qdrant to track the evolution of a story over time.
- [ ] **Dockerization:** Create `Dockerfile` and `docker-compose.yml` for unified environment deployment.
- [ ] **REST API Layer:** Implement a FastAPI server to serve daily reports and cluster data to frontends.
- [ ] **LLM Response Caching:** Implement LangChain's `SQLiteCache` to save API costs on repeated runs.
- [ ] **Automated Data Pruning:** Add a task to archive or delete raw articles/logs older than 30 days.
- [ ] **Frontend Dashboard:** A Streamlit or Next.js UI to visualize the "Unbiased India" findings.

---

## ✅ Completed Foundations

### Ingestion & Data Quality

- [x] **Triple-Track Discovery:** Parallel fetching via RSS, Sitemaps, and Homepage Spiders.
- [x] **Asynchronous I/O:** Fully parallelized fetching and extraction using `aiohttp` and `asyncio.gather`.
- [x] **Deep Extraction:** Integrated `trafilatura` for clean full-text article body fetching.
- [x] **Content Sanitization:** Automated filtering of cookie walls, error pages, and junk content.
- [x] **Pre-Clustering Deduping:** URL and Title-based deduplication to optimize cost and noise.

### Agentic Intelligence

- [x] **Service-Node Architecture:** Fully modularized agent logic into independent, testable classes.
- [x] **Functional Patterns:** Replaced imperative loops with clean list comprehensions and mapping.
- [x] **Cross-lingual Grouping:** Multilingual-E5 embeddings for semantic clustering across 7+ languages.
- [x] **State Persistence:** LangGraph checkpointing using `SqliteSaver` for crash recovery.
- [x] **Stability:** LLM Rate Limiting using `asyncio.Semaphore` (max 3 concurrent calls).
- [x] **Robust Parsing:** Reliable regex-based JSON extraction from LLM responses.

### Engineering & Configuration

- [x] **YAML Configuration:** Centralized system settings and feed network in `config.yaml`.
- [x] **Knowledge Base Persistence:** Managed publisher metadata in `data/source_kb.json`.
- [x] **Repository Pattern:** Decoupled storage logic from core pipeline using SQLAlchemy.
- [x] **Reporting Engine:** Automated generation of human-readable Markdown reports.
- [x] **Testing Infrastructure:** `pytest` suite for core helpers and ingestion logic.
- [x] **Automation:** GitHub Action for daily 8 AM IST runs with HuggingFace model caching.
