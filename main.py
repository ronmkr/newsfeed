import os
from src.ingestion.collector import NewsCollector
from src.agents.graph import create_pipeline
from src.storage.db import DatabaseManager
from src.utils.logger import project_logger as logger

def run_daily_pipeline():
    """Orchestrates the full daily news pipeline."""
    from src.config.settings import settings
    
    # Pre-flight check: Verify API Key
    if not settings.OPENAI_API_KEY:
        logger.critical("MISSING API KEY: 'OPENAI_API_KEY' (Google Gemini Key) not found in .env or environment.")
        logger.info("Please add it to your .env file: OPENAI_API_KEY=your_gemini_key_here")
        return

    logger.info("Starting Unbiased India News: Daily Batch Run")

    # 1. Ingestion: Fetch raw news articles
    collector = NewsCollector()
    # We'll modify run_ingestion slightly to return articles for the pipeline
    logger.info("Step 1: Ingesting articles from RSS feeds...")
    all_articles = []
    from src.config.settings import settings
    for feed_url in settings.RSS_FEEDS:
        source_domain = feed_url.split("//")[-1].split("/")[0]
        feed_data = collector.fetch_feed(feed_url)
        if feed_data:
            processed = collector.process_entries(feed_data, source_domain)
            all_articles.extend(processed)

    if not all_articles:
        logger.error("No articles found during ingestion. Exiting.")
        return

    # 2. Agentic Workflow: Clustering -> Summarization -> Bias Analysis -> Blindspot Detection
    logger.info(f"Step 2: Starting Agentic Workflow for {len(all_articles)} articles...")
    pipeline = create_pipeline()
    initial_state = {
        "clusters": [],
        "current_cluster_index": 0,
        "raw_data": all_articles,
        "errors": [],
        "next_step": "",
        "loop_count": 0
    }
    
    # Run the LangGraph
    final_state = pipeline.invoke(initial_state)

    # 3. Storage: Persist analyzed clusters to SQLite
    logger.info("Step 3: Saving analyzed clusters to database...")
    db = DatabaseManager()
    db.save_clusters(final_state["clusters"])

    logger.success("Daily Batch Run Completed Successfully!")

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    run_daily_pipeline()
