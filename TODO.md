# 📝 Unbiased India News - Development Roadmap

This document tracks the critical refinements needed to move the pipeline from prototype to a production-ready batch process.

---

## 🔴 High Priority (Immediate Actions)

- [ ] **Activate LLM Logic:** Uncomment the `llm_light.invoke()` and `llm_heavy.invoke()` calls in `src/agents/nodes/`. 
- [x] **Robust JSON Parsing:** (Completed) Implement a safe parser to extract and validate JSON from LLM responses in the Auditor and Summarizer nodes.
- [x] **Markdown Report Generator:** (Completed)
 Create a utility to export the daily findings from the SQLite DB into a beautiful `DAILY_REPORT.md` file for GitHub.

## 🟡 Medium Priority (Engineering & Reliability)

- [x] **LLM Rate Limiting:** (Completed) Implement `asyncio.Semaphore` to limit concurrent AI calls and avoid Gemini 429 rate limit errors.
- [x] **Content Sanitization:** (Completed) Add a filter to discard junk text (e.g., cookie walls, "Access Denied") from the `full_text` before sending to analysis.
- [x] **Pre-Clustering Deduping:** (Completed)
- [x] **Reasoning Trace Storage:** (Completed)
- [x] **LangGraph Checkpointing:** (Completed)

## 🟢 Low Priority (Scaling & Polishing)

- [x] **CI/CD Model Caching:** (Completed)
- [x] **Modular Helpers:** (Completed) Extracted reusable text cleaning and domain parsing into `src/utils/helpers.py`.
- [x] **Unit Testing:** (Completed) Added `pytest` suite for core ingestion and helper logic in `tests/unit`.
- [ ] **Judge LLM (GPT-4o) Integration:** Fully automate the `tests/evals/runner.py` by integrating a "Judge LLM" call to dynamically evaluate the Auditor's accuracy.
- [ ] **Frontend Dashboard:** Create a simple Streamlit or Next.js dashboard to visualize the daily bias reports, ownership influence, and blindspot alerts.

---

## ✅ Completed Foundations

- [x] **Modular Architecture:** Fully decoupled Ingestion, Clustering, Agentic, and Storage modules.
- [x] **Repository Pattern:** Decoupled database connection from data access logic.
- [x] **Cross-lingual Support:** Multilingual-E5 embeddings for semantic grouping across 7+ languages.
- [x] **Robust Source Matching:** Using `tldextract` for domain-level ownership lookups.
- [x] **GitHub Action:** Automated daily 8 AM IST runs with persistence.
- [x] **Externalize Source Metadata:** Moved the `SOURCE_KB` from `src/config/sources.py` into `data/source_kb.json` for better maintainability.
- [x] **Async Ingestion & LLM Calls:** Refactored the `IngestionCoordinator` and LLM nodes to use `asyncio` and `aiohttp` for parallel processing.
