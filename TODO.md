# 📝 Unbiased India News - Development Roadmap

This document tracks the progress of the Unbiased India News agentic pipeline.

---

## 🔴 High Priority (Final Steps)

- [ ] **Activate LLM Logic:** Uncomment the `llm.ainvoke()` calls in `src/agents/nodes/summarizer.py` and `src/agents/nodes/auditor.py`. Currently, these nodes use simulated logic to prevent unintended API costs.
- [ ] **Real-World Parsing Validation:** Once LLM logic is active, verify that the `RobustJSONParser` correctly handles various edge cases in Gemini's responses.

## 🟡 Medium Priority (Expansion)

- [ ] **Regional Source Deep-Dive:** Expand the `sitemap_urls` in `IngestionCoordinator` to include regional language sitemaps (Hindi, Marathi, etc.) for deeper cross-lingual coverage.
- [ ] **Judge LLM (GPT-4o) Integration:** Automate the evaluation suite in `tests/evals/runner.py` by integrating a "Judge" call to compare the Auditor's score against human baselines.

## 🟢 Low Priority (UX & Polishing)

- [ ] **Frontend Dashboard:** Create a simple Streamlit or Next.js dashboard to visualize the clusters, bias trends, and "Blindspot" alerts stored in the SQLite database.
- [ ] **Email/Telegram Alerts:** Add a utility to send the daily `LATEST_REPORT.md` to a Telegram bot or email list.

---

## ✅ Completed Foundations

### Ingestion & Data Quality

- [x] **Triple-Track Ingestion:** Concurrent fetching via RSS, Sitemap XML, and Homepage HTML Spiders.
- [x] **Asynchronous Fetching:** Fully parallelized I/O using `aiohttp` and `asyncio.gather`.
- [x] **Full Text Extraction:** Integrated `trafilatura` for clutter-free article body extraction.
- [x] **Content Sanitization:** Automated filtering of cookie walls, error pages, and "junk" text.
- [x] **Pre-Clustering Deduping:** URL and Title-based deduplication to reduce noise and cost.

### Agentic Intelligence

- [x] **Modular Node Architecture:** Decoupled agents (Scout, Summarizer, Auditor, Editor) into independent, testable classes.
- [x] **Cross-lingual Clustering:** Multilingual-E5 embeddings for grouping stories across 7+ languages.
- [x] **LangGraph Checkpointing:** State persistence using `SqliteSaver` to allow resuming after crashes.
- [x] **LLM Rate Limiting:** Implemented `asyncio.Semaphore` to prevent 429 rate limit errors.
- [x] **Robust JSON Parsing:** Regex-based extraction of AI responses from raw strings.

### Engineering & Storage

- [x] **Externalized Data:** RSS feeds (`data/rss_feeds.json`) and Ownership KB (`data/source_kb.json`) managed outside of code.
- [x] **Repository Pattern:** Decoupled database connection from data access logic using SQLAlchemy.
- [x] **Reasoning Trace Storage:** Persistent storage of AI "Chain of Thought" for transparency.
- [x] **Markdown Report Generator:** Automated export of daily findings to human-readable reports.
- [x] **Unit Testing Suite:** `pytest` infrastructure for core helpers and ingestion logic.
- [x] **GitHub Action:** Automated daily 8 AM IST runs with model caching.
