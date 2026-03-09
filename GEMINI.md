# GEMINI.md - Project Mandates & Technical Standards

## 1. Foundational Principles
- **Bias Neutrality:** Every agent, summary, and bias report must be neutral and data-driven. The Auditor Agent must explicitly use ownership metadata (`data/source_kb.json`) in its reasoning.
- **Architectural Purity:** All logic must follow the modular, decoupled patterns established (Repository Pattern for storage, Service-based clustering, Node-based agents).
- **Asynchronicity:** All I/O operations (fetching news, LLM calls) must be asynchronous to maintain batch run-time under 5 minutes for 40+ sources.

## 2. Technical Stack
- **Framework:** LangGraph for cyclic agentic workflows.
- **LLMs:** Gemini 1.5 Pro (Auditor) and Gemini 1.5 Flash (Summarizer).
- **Embeddings:** Multilingual-E5 (`intfloat/multilingual-e5-small`) for semantic grouping across languages.
- **Storage:** SQLite for persistent storage of daily analysis.
- **Type Safety:** Strict Python type hinting (`Dict`, `Optional`, `List`) for all pipeline functions.

## 3. Mandatory Development Workflow
- **Research:** Map the `data/source_kb.json` before adding new publishers to the `src/config/feeds.py`.
- **Strategy:** All major changes must be documented in `TODO.md` before execution.
- **Execution:** Follow the **Plan -> Act -> Validate** cycle. Every node in the `PipelineGraph` must be tested against a mock state before final integration.
- **Testing:** New features must have a corresponding test case added to `tests/evals/gold_standard.json`.

## 4. Operational Boundaries
- **No Manual Commits:** The `data/newsfeed.db` is managed by the automated GitHub Action. Avoid manual pushes that could cause binary merge conflicts.
- **Credential Safety:** Never print or log the `OPENAI_API_KEY`.
- **Loop Protection:** Agentic cycles must terminate after a maximum of 3 loops.
