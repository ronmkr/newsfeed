# GEMINI.md - Technical Mandates and Architectural Standards

## 1. Architectural Integrity
- **Single Responsibility:** Every module must perform one specialized task. Fetchers are separate from Orchestrators; Agents are separate from state definitions.
- **Node-Based Agents:** All agent logic must be encapsulated in independent classes within `src/agents/nodes/`, inheriting from `BaseClusterAgent` where parallel processing is required.
- **Repository Pattern:** Direct database calls are strictly prohibited outside of `src/storage/repository.py`. All persistence must be handled through the repository layer.

## 2. Ingestion and Data Quality
- **Triple-Track Convergence:** Ingestion must utilize the established RSS, Sitemap, and Homepage Spider tracks to ensure maximum resilience against broken or blocked feeds.
- **Strict Deduplication:** All raw articles must pass through the `deduplicate` logic (URL and Title-based) before entering the agentic state to minimize noise and token expenditure.
- **Deep Content Extraction:** Analysis must rely on full-text bodies retrieved via `trafilatura` rather than short RSS snippets.

## 3. Technical Stack Constraints
- **Model Routing:** Always use Gemini 1.5 Flash for high-volume summarization and Gemini 1.5 Pro for nuanced ideological auditing.
- **Vector Space:** Maintain the `fastembed` (BAAI/bge-small-en-v1.5) ONNX engine for semantic clustering to ensure the Docker image remains under 1GB.
- **Asynchronicity:** All I/O-bound operations (network requests, database writes, and LLM calls) must utilize `asyncio` and `aiohttp`.

## 4. Configuration and Credentials
- **Standardized Config:** All operational parameters must be defined in `config.yaml`. Use the `CONFIG_PATH` environment variable for runtime overrides.
- **Credential Governance:** Use `GOOGLE_API_KEY` for all Gemini operations. Never hardcode keys; always retrieve them from the environment via the `Settings` class.
- **State Persistence:** Utilize `AsyncSqliteSaver` for LangGraph checkpointing and `SQLiteCache` for LLM response caching to ensure cost efficiency and crash recovery.

## 5. Development and Testing
- **Validation Cycle:** Every core feature must have a corresponding unit test in `tests/unit/` using `pytest`.
- **Audit Accuracy:** Significant changes to the Auditor Agent must be validated against the `tests/evals/` suite to ensure bias scoring remains within the 20 percent variance threshold.
- **Deployment:** The `Dockerfile` must utilize a multi-stage build to maintain a lean production environment.
