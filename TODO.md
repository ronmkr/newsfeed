# Unbiased India News - Development Roadmap

This document tracks the engineering progress and future milestones for the Unbiased India News agentic pipeline.

---

## High Priority (Final Validation)

- [ ] Real-World Parsing Validation: Verify that the RobustJSONParser correctly handles high-token Gemini responses during major breaking news cycles (e.g., 20+ sources in a single cluster).
- [ ] Cross-Lingual Clustering Verification: Empirically validate that Marathi articles from Sakal and Hindi articles from Navbharat Times correctly group with English reports from The Hindu using the Multilingual-E5 vector space.

## Medium Priority (Expansion and Evaluation)

- [ ] Regional Source Expansion: Implement additional sitemap discovery for regional powerhouses including Mathrubhumi (Malayalam) and Anandabazar Patrika (Bengali).
- [ ] Judge LLM (GPT-4o) Integration: Automate the tests/evals/runner.py by integrating a GPT-4o "Judge" to provide an objective score comparison against the Auditor's bias findings.

## Good to Have (Future Enhancements)

- [ ] Vector Database Integration: Implement ChromaDB to enable long-term story tracking and narrative shift detection over time.
- [ ] REST API Layer: Develop a FastAPI-based service to expose daily reports and cluster data to external web or mobile applications.
- [ ] LLM Response Caching: Integrate LangChain SQLiteCache to minimize API costs during development and repeated batch runs.
- [ ] Automated Data Retention: Implement a pruning utility to archive raw article data and logs older than 30 days to manage database growth.

---

## Completed Foundations

### Ingestion and Data Quality
- [x] Triple-Track Discovery: Concurrent fetching via RSS, Sitemap XML, and Homepage HTML Spiders.
- [x] Asynchronous I/O: Fully parallelized fetching and extraction logic using aiohttp and asyncio.gather.
- [x] Full Text Extraction: Integration of Trafilatura for clutter-free article body retrieval.
- [x] Content Sanitization: Heuristic-based filtering of cookie walls, access denied pages, and junk text.
- [x] Pre-Clustering Deduping: URL and Title-level filtering to optimize token usage and system noise.

### Agentic Intelligence
- [x] Modular Node Architecture: Decoupled agent logic (Scout, Summarizer, Auditor, Editor) into independent, testable classes.
- [x] State Persistence: Asynchronous LangGraph checkpointing using AsyncSqliteSaver for crash recovery.
- [x] Rate Limiting: Implementation of asyncio.Semaphore to manage concurrent LLM API calls.
- [x] Robust JSON Parsing: Regex-based extraction and validation of AI-generated responses.

### Engineering and Configuration
- [x] Universal YAML Configuration: Centralized system settings and feed network in config.yaml.
- [x] Repository Pattern: Decoupled database persistence from core pipeline logic using SQLAlchemy.
- [x] Reporting Engine: Automated export of daily database findings to structured Markdown reports.
- [x] Dockerization: Fully containerized setup with Python 3.12, persistent volumes, and dynamic configuration support.
