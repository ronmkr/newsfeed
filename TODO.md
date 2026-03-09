# 📝 Unbiased India News - Development Roadmap

This document tracks the critical refinements needed to move the pipeline from prototype to a production-ready batch process.

---

## 🔴 High Priority (Immediate Actions)

- [ ] **Activate LLM Logic:** Uncomment the `llm_light.invoke()` and `llm_heavy.invoke()` calls in `src/agents/graph.py`. Currently, the agents are using fallback/mock logic to avoid API costs during setup.
- [ ] **Robust Source Matching:** Refine `src/config/sources.py` and `src/agents/graph.py` to use a more flexible domain matching (e.g., using `tldextract`) to ensure the Ownership Knowledge Base correctly identifies sources like `indiatimes.com` vs `timesofindia.com`.
- [ ] **Environment Validation:** Add a check in `main.py` to verify that `OPENAI_API_KEY` (Gemini Key) is present before starting the run, providing a clear error message if missing.

## 🟡 Medium Priority (Enhancements)

- [ ] **Full Text Extraction:** Implement a tool like `trafilatura` or `newspaper3k` in the `NewsCollector` to fetch the full article body from the source `link`. Currently, analysis is limited to the short RSS summary/snippet.
- [ ] **CI/CD Model Caching:** Update `.github/workflows/daily_run.yml` to cache the HuggingFace model directory (`~/.cache/huggingface`). This prevents the 100MB `multilingual-e5` model from being re-downloaded on every 8 AM run.
- [ ] **Database Migration Strategy:** Re-evaluate the strategy of committing the SQLite `.db` file back to Git. Consider moving to a hosted PostgreSQL (Supabase/Neon) or exporting a daily `report.json` to avoid binary merge conflicts.

## 🟢 Low Priority (Scaling & Polishing)

- [ ] **Regional Language Expansion:** Add more RSS feeds for Hindi, Marathi, Tamil, and Bengali publications to the `RSS_FEEDS` list in `src/config/settings.py` to test the cross-lingual clustering.
- [ ] **Judge LLM (GPT-4o) Integration:** Fully automate the `tests/evals/runner.py` by integrating a "Judge LLM" call to dynamically evaluate the Auditor's bias score against the gold standard.
- [ ] **Frontend Dashboard:** Create a simple Streamlit or Next.js dashboard to visualize the clusters, bias trends, and "Blindspot" alerts stored in the database.

---

## ✅ Completed Foundations

- [x] Multi-agent StateGraph architecture (Scout, Summarizer, Auditor, Editor).
- [x] Cross-lingual embedding comparison (Multilingual-E5).
- [x] Source Knowledge Base with Indian Media ownership data.
- [x] Structured logging and relational database storage.
- [x] GitHub Action for automated daily 8 AM IST runs.
