from typing import Dict, Any
from langgraph.graph import END
from src.agents.state import AgentState, NewsCluster
from src.utils.logger import project_logger as logger

class EditorNode:
    """The Editor Node: Refactored with functional patterns."""
    
    async def __call__(self, state: AgentState) -> Dict[str, Any]:
        logger.info("Editor-in-Chief Node: Finalizing Quality Control...")
        
        clusters = state.get("clusters", [])
        # Functional update of clusters
        [self._detect_blindspot(c) for c in clusters]
            
        next_step = END if state.get("loop_count", 0) >= 3 else END # Terminate for now
        if state.get("loop_count", 0) >= 3:
            logger.warning("Max loop count reached. Forcing termination.")
            
        return {"clusters": clusters, "next_step": next_step}

    def _detect_blindspot(self, cluster: NewsCluster):
        """Logic to flag ideological gaps in coverage."""
        leans = [a.source_metadata.ideological_lean for a in cluster.articles if a.source_metadata]
        has_left = any("Left" in l for l in leans)
        has_right = any("Right" in l for l in leans)
        
        if (has_left and not has_right) or (has_right and not has_left):
            cluster.is_blindspot = True
            logger.warning(f"BLINDSPOT DETECTED: {cluster.main_event}")
