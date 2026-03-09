from typing import Dict, Any
from langgraph.graph import END
from src.agents.state import AgentState
from src.clustering.engine import ClusteringEngine
from src.config.sources import get_source_metadata
from src.utils.logger import project_logger as logger

class ScoutNode:
    """The Scout Node: Async node for clustering and metadata enrichment."""
    
    def __init__(self, clustering_engine: ClusteringEngine):
        self.clustering_engine = clustering_engine

    async def __call__(self, state: AgentState) -> Dict[str, Any]:
        logger.info("Scout Node: Identifying Story Threads and Enriching Metadata...")
        
        loop_count = state.get("loop_count", 0) + 1
        raw_data = state.get("raw_data")
        
        if not raw_data:
            logger.warning("Scout Node: No raw data found.")
            return {"next_step": END, "errors": ["No raw data found."], "loop_count": loop_count}
        
        # Clustering is currently synchronous (CPU-bound)
        clusters = self.clustering_engine.group_articles(raw_data)
        
        # Enrich metadata
        for cluster in clusters:
            for article in cluster.articles:
                article.source_metadata = get_source_metadata(article.source)
        
        return {
            "clusters": clusters,
            "next_step": "summarizer" if clusters else END,
            "loop_count": loop_count
        }
