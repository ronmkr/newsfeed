import os
from src.ingestion.collector import IngestionCoordinator
from src.agents.graph import create_pipeline
from src.storage.connection import DatabaseConnection
from src.storage.repository import ClusterRepository
from src.utils.logger import project_logger as logger
from src.config.settings import settings
from src.config.feeds import RSS_FEEDS

class UnbiasedIndiaNewsPipeline:
    """Central orchestrator for the modular news pipeline."""
    
    def __init__(self):
        self.ingestion = IngestionCoordinator()
        self.agentic_app = create_pipeline()
        
        # Initialize Database using Repository Pattern
        self.db_connection = DatabaseConnection()
        self.repository = ClusterRepository(self.db_connection)

    def run_daily_batch(self):
        """Executes the full daily run."""
        
        # 1. Environment Check
        if not settings.OPENAI_API_KEY:
            logger.critical("MISSING API KEY: 'OPENAI_API_KEY' not found.")
            return

        logger.info(f"Starting {settings.PROJECT_NAME} Pipeline...")

        # 2. Ingestion
        raw_articles = self.ingestion.fetch_all(RSS_FEEDS)
        if not raw_articles:
            logger.error("No articles found during ingestion. Stopping.")
            return

        # Convert RawArticle models to dicts for the LangGraph state
        raw_data = [art.to_dict() for art in raw_articles]

        # 3. Agentic Workflow
        initial_state = {
            "clusters": [],
            "current_cluster_index": 0,
            "raw_data": raw_data,
            "errors": [],
            "next_step": "",
            "loop_count": 0
        }
        
        logger.info(f"Processing {len(raw_data)} articles through agents...")
        final_state = self.agentic_app.invoke(initial_state)

        # 4. Storage
        if final_state.get("clusters"):
            self.repository.save_clusters(final_state["clusters"])
            logger.success(f"Pipeline complete. {len(final_state['clusters'])} clusters saved.")
        else:
            logger.warning("No clusters generated to save.")

if __name__ == "__main__":
    # Create required dirs
    os.makedirs(settings.RAW_DATA_PATH, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    pipeline = UnbiasedIndiaNewsPipeline()
    pipeline.run_daily_batch()
