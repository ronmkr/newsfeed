# Unbiased India News

## Overview
Unbiased India News is a production-grade, agentic AI news aggregation and analysis platform focused on the Indian media landscape. The system operates as a daily batch pipeline that fetches, clusters, analyzes, and summarizes top political and national news stories. It provides deep context on ideological framing by cross-referencing article content with a specialized Knowledge Base of publisher ownership and funding.

## Core Pipeline Architecture
The system utilizes a modular, asynchronous multi-agent workflow built with LangGraph:

1.  **Triple-Track Ingestion (The Scout):** 
    - **RSS Polling:** Concurrent fetching of verified Indian news feeds.
    - **Sitemap Discovery:** Professional-grade link extraction from publisher `sitemap.xml` endpoints (highly reliable).
    - **Homepage Spider:** Fallback HTML scanning for publications with blocked or fragile feeds.
2.  **Clustering (The Matchmaker):** Uses cross-lingual semantic embeddings (`multilingual-e5-small`) to group articles from 7+ languages (English, Hindi, Marathi, etc.) into unified "Story Clusters."
3.  **Summarization:** Parallel generation of neutral three-bullet summaries using Gemini 1.5 Flash.
4.  **Ideological Audit (The Auditor):** Nuanced bias and framing analysis using Gemini 1.5 Pro. It evaluates "adjective density" and "omitted perspectives," contextualized by ownership metadata (e.g., Adani-owned, Independent).
5.  **Quality Control (Editor-in-Chief):** Blindspot detection logic that flags major stories covered by only one side of the political spectrum.

## Project Structure
- `src/ingestion`: Specialized fetchers, sitemap engines, and discovery spiders.
- `src/clustering`: Semantic grouping services and embedding management.
- `src/agents/nodes`: Modular, class-based agent reasoning components.
- `src/storage`: Repository pattern implementation using SQLAlchemy and SQLite.
- `src/utils`: Shared helpers for text sanitization, robust JSON parsing, and report generation.
- `src/config`: System configuration (YAML), Feed management, and Source Knowledge Base (JSON).
- `data/`: Persistent storage for raw logs, checkpoints, and the local database.
- `reports/`: Human-readable daily Markdown analysis reports.

## Key Technical Features
- **Parallel Processing:** Fully asynchronous I/O using `aiohttp` and `asyncio.gather` for both ingestion and LLM calls.
- **State Persistence:** Built-in LangGraph checkpointing (`SqliteSaver`) for crash recovery and resume capabilities.
- **Rate Limiting:** Global semaphore management to prevent API 429 errors during parallel AI analysis.
- **Content Sanitization:** Automated filtering of cookie walls, "Access Denied" pages, and junk text via `trafilatura`.
- **Deduplication:** Robust URL and Title-level filtering to reduce noise and LLM costs.

## Setup Instructions

### Prerequisites
- Python 3.11 or higher
- Google Gemini API Key

### Local Installation
1.  Clone the repository and navigate to the project root.
2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure your environment in a `.env` file:
    ```env
    OPENAI_API_KEY=your_google_gemini_api_key
    ```

## Usage

### Running the Pipeline
To execute the full daily batch run (Ingestion -> Analysis -> Reporting):
```bash
python3 main.py
```

### Viewing Reports
After a successful run, check the `reports/` directory for the latest findings:
- `reports/LATEST_REPORT.md`: A human-readable summary of daily news bias and blindspots.

### Testing and Validation
- **Unit Tests:** Verify core logic using Pytest:
    ```bash
    pytest tests/unit
    ```
- **Accuracy Evaluations:** Run the Auditor accuracy suite against human baselines:
    ```bash
    python3 -m tests.evals.runner
    ```

## Configuration
- **Settings:** Modify `config.yaml` to change models, storage paths, or concurrency limits.
- **Feeds:** Add or remove news sources in the `feeds` section of `config.yaml`.
- **Metadata:** Update publisher ownership details in `data/source_kb.json`.

## Technical Standards
- **Asynchronicity:** Non-blocking parallel execution for maximum efficiency.
- **Modularity:** Strict separation of data from logic following SOLID principles.
- **Transparency:** Full storage of AI reasoning traces ("Chain of Thought") in the database.
