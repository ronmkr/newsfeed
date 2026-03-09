# GEMINI.md - Technical Mandates and Architectural Standards

## 1. Architectural Integrity
- **Single Responsibility:** Every module must perform one specialized task. Ingestion coordinators are separate from fetchers; agent nodes are separate from the graph assembly.
- **Node-Based Agents:** All agent logic must be encapsulated in independent classes within `src/agents/nodes/`, inheriting from `BaseClusterAgent` to leverage standardized parallel processing and rate limiting.
- **Repository Pattern:** Direct database calls are strictly prohibited outside of `src/storage/repository.py`. All persistence must be handled through the repository layer using SQLAlchemy.

## 2. Ingestion and Data Quality
- **Triple-Track Convergence:** Ingestion must utilize the established RSS, Sitemap, and Homepage Spider tracks to ensure maximum resilience against broken or blocked feeds.
- **Strict Deduplication:** All raw articles must pass through the `deduplicate` logic (URL and Title-based) before entering the agentic state to minimize noise and token expenditure.
- **Heuristic Sanitization:** Article content must be filtered for cookie walls, error messages, and minimal character counts before being passed to the analysis layer.
- **Parallel Enrichment:** Full-text extraction must be performed asynchronously with semaphore-based concurrency control to maintain system stability.

## 3. Technical Stack Constraints
- **Model Routing:** Always use Gemini 1.5 Flash for high-volume summarization and Gemini 1.5 Pro for nuanced ideological auditing.
- **Vector Space:** Maintain the `fastembed` (BAAI/bge-small-en-v1.5) ONNX engine for semantic clustering to ensure the Docker image remains under 1GB and inference remains high-speed.
- **Asynchronicity:** All I/O-bound operations (network requests, database writes, and LLM calls) must utilize `asyncio` and `aiohttp`. CPU-bound tasks (Clustering) must be offloaded to threads via `asyncio.to_thread`.

## 4. Configuration and Credentials
- **Standardized Config:** All operational parameters must be defined in `config.yaml`. Use the `CONFIG_PATH` environment variable for runtime overrides.
- **Credential Governance:** Use `GOOGLE_API_KEY` for all Gemini operations. Never hardcode keys; always retrieve them from the environment via the `Settings` class.
- **State Persistence:** Utilize `AsyncSqliteSaver` for LangGraph checkpointing and `SQLiteCache` for LLM response caching to ensure cost efficiency and crash recovery.

## 5. Development and Testing
- **Functional Patterns:** Prefer functional mappings, list comprehensions, and reusable helpers over imperative loops to maintain code readability and reduce side effects.
- **Validation Cycle:** Every core feature must have a corresponding unit test in `tests/unit/` using `pytest`.
- **Audit Accuracy:** Significant changes to the Auditor Agent must be validated against the `tests/evals/` suite to ensure bias scoring remains within the 20 percent variance threshold.
- **Deployment:** The `Dockerfile` must utilize a multi-stage build to maintain a lean production environment.
