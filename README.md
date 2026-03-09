# Unbiased India News

## Overview
Unbiased India News is an agentic AI news aggregation and analysis platform focused on the Indian media landscape. The system operates as a daily batch pipeline that fetches, clusters, analyzes, and summarizes top political and national news stories. It assigns political bias ratings and provides context based on publication ownership (e.g., Reliance-owned, Adani-owned, Independent).

## Core Pipeline Architecture
The system utilizes a modular, asynchronous multi-agent workflow built with LangGraph:

1.  **Ingestion (The Scout):** Parallel fetching of over 40 RSS feeds with automated de-duplication and full-text extraction using Trafilatura.
2.  **Clustering (The Matchmaker):** Cross-lingual semantic grouping using Multilingual-E5 embeddings.
3.  **Summarization:** Parallel generation of neutral three-bullet summaries using Gemini 1.5 Flash.
4.  **Audit (The Auditor):** Nuanced bias and framing analysis using Gemini 1.5 Pro and a Source Knowledge Base.
5.  **Quality Control (Editor-in-Chief):** Blindspot detection and final report validation.

## Project Structure
- `src/ingestion`: Asynchronous fetching and content extraction logic.
- `src/clustering`: Semantic grouping and embedding services.
- `src/agents/nodes`: Modular agentic reasoning components.
- `src/storage`: Repository pattern for database persistence.
- `src/utils`: Shared helpers, robust parsers, and report generators.
- `src/config`: Externalized feeds and source metadata (JSON).

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
4.  Configure environment variables in a `.env` file:
    ```env
    OPENAI_API_KEY=your_google_gemini_api_key
    ```

### Running the Pipeline
To execute the full daily batch run:
```bash
python3 main.py
```

### Testing and Evaluations
- **Unit Tests:** Run core logic tests using Pytest:
    ```bash
    pytest tests/unit
    ```
- **Bias Evaluations:** Run the Auditor accuracy suite:
    ```bash
    python3 -m tests.evals.runner
    ```

## Technical Standards
- **Asynchronicity:** Parallel I/O using Aiohttp and Asyncio. gathered execution.
- **Robustness:** LangGraph checkpointing for state persistence.
- **Modularity:** Strict separation of data (JSON/CSV) from logic.
- **Transparency:** Storage of full reasoning traces for all AI analysis.
