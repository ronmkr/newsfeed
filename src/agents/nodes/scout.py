import asyncio
from typing import Dict, Any
from langgraph.graph import END
from src.agents.state import AgentState
from src.clustering.engine import ClusteringEngine
from src.config.sources import get_source_metadata
from src.utils.logger import project_logger as logger

class ScoutNode:
    """
    Entry point for the agentic workflow. 
    Handles initial grouping and source enrichment.
    """
    
    def __init__(self, clustering_engine: ClusteringEngine):
        """
        Args:
            clustering_engine: The service used to group raw articles.
        """
        self.clustering_engine = clustering_engine

    async def __call__(self, state: AgentState) -> Dict[str, Any]:
        """
        Transforms raw data into enriched story clusters.
        """
        logger.info("Scout Node: Transforming raw articles into story threads...")
        
        loop_count = state.get("loop_count", 0) + 1
        raw_data = state.get("raw_data")
        
        if not raw_data:
            logger.warning("Scout Node: No raw news found to process.")
            return {"next_step": END, "errors": ["No data found"], "loop_count": loop_count}
        
        # 1. Semantic Clustering (CPU-bound call offloaded to thread)
        clusters = await asyncio.to_thread(self.clustering_engine.group_articles, raw_data)
        
        # 2. Source Enrichment (Metadata lookup)
        for cluster in clusters:
            for article in cluster.articles:
                article.source_metadata = get_source_metadata(article.source)
        
        return {
            "clusters": clusters,
            "next_step": "summarizer" if clusters else END,
            "loop_count": loop_count
        }
