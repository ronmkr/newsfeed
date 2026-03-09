# Unbiased India News

## Overview
Unbiased India News is an agentic AI news aggregation and analysis platform focused on the Indian media landscape. The system operates as a daily batch pipeline that fetches, clusters, analyzes, and summarizes top political and national news stories. It assigns political bias ratings and provides context based on publication ownership (e.g., Reliance-owned, Adani-owned, Independent).

## Core Pipeline Architecture
The system utilizes a multi-agent workflow built with LangGraph to process news articles through several stages:

1.  **Ingestion (The Scout):** Fetches news from over 40 RSS feeds across English, Hindi, Marathi, Tamil, Telugu, Malayalam, Bengali, Kannada, and Gujarati.
2.  **Clustering (The Matchmaker):** Uses cross-lingual semantic embeddings (multilingual-e5-small) to group articles from different languages into single "Story Clusters."
3.  **Summarization:** Employs Gemini 1.5 Flash to generate neutral, three-bullet summaries for each story.
4.  **Audit (The Auditor):** Uses Gemini 1.5 Pro to analyze framing, adjective density, and ideological leaning, cross-referencing with a Source Knowledge Base containing ownership and funding metadata.
5.  **Quality Control (Editor-in-Chief):** Identifies "Blindspots" where major stories are only covered by one side of the political spectrum.

## Project Structure
- `src/ingestion`: Scripts for polling RSS feeds and wire services.
- `src/clustering`: Logic for semantic grouping of articles.
- `src/agents`: LangGraph definitions for agentic reasoning and flow.
- `src/storage`: SQLAlchemy models and SQLite database management.
- `src/config`: System settings, source metadata, and RSS feed lists.
- `tests/evals`: Evaluation suite to measure Auditor bias scoring against human baselines.

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

### Running Evaluations
To run the bias score evaluation suite:
```bash
python3 -m tests.evals.runner
```

## Automation
The project includes a GitHub Action workflow configured to run daily at 8:00 AM IST (02:30 UTC). This workflow automates the pipeline, caches the embedding models, and commits the updated analysis results to the repository's SQLite database.

## Technical Standards
- **Framework:** LangGraph for cyclic agentic workflows.
- **LLMs:** Gemini 1.5 Pro (Audit) and Gemini 1.5 Flash (Summarization).
- **Embeddings:** Multilingual-E5 for cross-lingual support.
- **Database:** SQLite with SQLAlchemy ORM.
- **Logging:** Structured logging via Loguru.
