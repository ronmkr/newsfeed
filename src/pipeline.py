import os
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from src.ingestion.collector import IngestionCoordinator
from src.agents.graph import create_pipeline
from src.storage.connection import DatabaseConnection
from src.storage.repository import ClusterRepository
from src.utils.report_generator import MarkdownReportGenerator
from src.utils.logger import project_logger as logger
from src.config.settings import settings
from src.config.feeds import load_feeds

class UnbiasedIndiaNewsPipeline:
    """Central orchestrator for the modular news pipeline."""
    
    def __init__(self):
        self.ingestion = IngestionCoordinator()
        self.db_connection = DatabaseConnection()
        self.repository = ClusterRepository(self.db_connection)
        self.report_generator = MarkdownReportGenerator(self.db_connection)

    async def run_daily_batch(self):
        """Executes the full daily run with async checkpointer."""
        
        # 1. Environment Check
        if not settings.GOOGLE_API_KEY:
            logger.critical("MISSING API KEY: 'GOOGLE_API_KEY' not found.")
            return

        logger.info(f"Starting {settings.PROJECT_NAME} Pipeline...")

        # 2. Initialize Async Checkpointer and Agentic App
        checkpoint_dir = os.path.dirname(settings.CHECKPOINTS_PATH)
        if checkpoint_dir: os.makedirs(checkpoint_dir, exist_ok=True)
        
        async with AsyncSqliteSaver.from_conn_string(settings.CHECKPOINTS_PATH) as checkpointer:
            agentic_app = create_pipeline(checkpointer=checkpointer)

            # 3. Ingestion
            feeds = load_feeds()
            raw_articles = await self.ingestion.fetch_all(feeds)
            if not raw_articles:
                logger.error("No articles found during ingestion. Stopping.")
                return

            # Convert RawArticle models to dicts for the LangGraph state
            raw_data = [art.to_dict() for art in raw_articles]

            # 4. Agentic Workflow
            config = {"configurable": {"thread_id": "daily_run"}}
            initial_state = {
                "clusters": [],
                "current_cluster_index": 0,
                "raw_data": raw_data,
                "errors": [],
                "next_step": "",
                "loop_count": 0
            }
            
            logger.info(f"Processing {len(raw_data)} articles through agents...")
            final_state = await agentic_app.ainvoke(initial_state, config=config)

            # 5. Storage
            if final_state.get("clusters"):
                self.repository.save_clusters(final_state["clusters"])
                self.report_generator.generate_daily_report()

                # Final Analytics Log
                total_articles = len(raw_data)
                total_clusters = len(final_state["clusters"])
                blindspots = sum(1 for c in final_state["clusters"] if c.is_blindspot)

                logger.success("--------------------------------------------------")
                logger.success(f"PIPELINE RUN COMPLETE")
                logger.success(f"Total Articles Processed: {total_articles}")
                logger.success(f"Story Clusters Formed:    {total_clusters}")
                logger.success(f"Blindspots Identified:    {blindspots}")
                logger.success("--------------------------------------------------")
            else:

                logger.warning("No clusters generated to save.")

if __name__ == "__main__":
    import asyncio
    # Create required dirs
    os.makedirs(settings.RAW_DATA_PATH, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    pipeline = UnbiasedIndiaNewsPipeline()
    asyncio.run(pipeline.run_daily_batch())
