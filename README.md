# Unbiased India News

Unbiased India News is a production-grade, agentic AI news aggregation and analysis platform focused on the Indian media landscape. The system fetches, clusters, and analyzes top national stories to reveal ideological framing and publisher bias through a multi-agent workflow.

## Core Architecture
The platform utilizes a modular, asynchronous multi-agent system built with LangGraph:

1.  **Ingestion (The Scout):** Parallel fetching via RSS feeds, Sitemap XML discovery, and Homepage HTML spiders.
2.  **Clustering (The Matchmaker):** Cross-lingual semantic grouping using Multilingual-E5 embeddings to unify stories across 7+ languages.
3.  **Summarization:** Parallel generation of neutral three-bullet summaries using Gemini 1.5 Flash.
4.  **Ideological Audit (The Auditor):** Nuanced bias and framing analysis using Gemini 1.5 Pro and an Ownership Knowledge Base.
5.  **Quality Control (Editor-in-Chief):** Automated detection of coverage blindspots and state management for iterative refinement.

---

## Real-World Output Sample
Below is a sample of how the agentic pipeline analyzes a news cluster:

### Story: GST Council Meeting on Rate Rationalization
*   **Overall Bias Score:** -0.35 (Center-Left Leaning)
*   **Coverage Status:** Balanced Coverage Detected

#### AI Generated Summary
- The GST Council reached a consensus on reducing tax slabs for essential health insurance premiums and medical equipment.
- Opposition-led states requested a further reduction in the standard 18 percent bracket, citing inflationary pressures on middle-class consumers.
- Finance ministry officials highlighted that the revenue implications of these cuts would be offset by increased compliance in the service sector.

#### Auditor Reasoning Trace
"Analysis indicates a Center-Left leaning in the aggregate coverage of this cluster. Reports from The Hindu and The Wire focused heavily on the demands of opposition-led states and the burden on consumers. Conversely, reports from News18 (Reliance-owned) and NDTV (Adani-owned) prioritized the government's fiscal stability narrative and the benefits to the insurance industry. The overall framing reflects a tension between consumer welfare advocacy and pro-market fiscal policy."

---

## Setup and Installation

### Docker Installation (Recommended)
Running via Docker ensures a consistent Python 3.12 environment:

1.  **Configure Credentials:** Create a .env file:
    ```env
    GOOGLE_API_KEY=your_gemini_api_key
    HF_TOKEN=your_huggingface_token_optional
    ```
2.  **Execute Pipeline:**
    ```bash
    docker-compose up --build
    ```

### Local Installation
1.  Initialize virtual environment: `python3 -m venv venv && source venv/bin/activate`
2.  Install dependencies: `pip install -r requirements.txt`
3.  Run the orchestrator: `python3 main.py`

## Project Structure
- `src/ingestion`: Asynchronous fetchers, sitemap engines, and discovery spiders.
- `src/clustering`: Semantic grouping services and embedding management.
- `src/agents`: Modular reasoning nodes and state graph definitions.
- `src/storage`: Repository pattern implementation using SQLAlchemy and SQLite.
- `reports/`: Automated daily Markdown analysis reports.

## Technical Standards
- **Concurrency:** Fully asynchronous I/O using aiohttp and asyncio.gather.
- **Persistence:** LangGraph checkpointing via AsyncSqliteSaver for robust error recovery.
- **Modularity:** Strict separation of configuration (YAML), metadata (JSON), and business logic.
- **Transparency:** Comprehensive storage of raw AI reasoning traces for auditability.
