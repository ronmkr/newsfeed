from typing import Dict, Any
from langgraph.graph import END
from src.agents.state import AgentState
from src.utils.logger import project_logger as logger

class EditorNode:
    """The Editor Node: Blindspot detection and quality control."""
    
    def __call__(self, state: AgentState) -> Dict[str, Any]:
        logger.info("Editor-in-Chief Node: Finalizing Quality Control and Detecting Blindspots...")
        
        clusters = state.get("clusters", [])
        updated_clusters = []
        
        for cluster in clusters:
            # Logic: Check if major ideological perspectives are missing
            leans = [a.source_metadata.ideological_lean for a in cluster.articles if a.source_metadata]
            
            has_left = any("Left" in l for l in leans)
            has_right = any("Right" in l for l in leans)
            
            # A "Blindspot" is when a story is ONLY covered by one side
            if (has_left and not has_right) or (has_right and not has_left):
                cluster.is_blindspot = True
                logger.warning(f"BLINDSPOT DETECTED: {cluster.main_event}")
            
            updated_clusters.append(cluster)
            
        # Loop back to Scout if deep blindspot detected, but only if loop_count < 3
        if state.get("loop_count", 0) >= 3:
            logger.warning("Max loop count (3) reached. Forcing termination.")
            return {"clusters": updated_clusters, "next_step": END}
            
        return {"clusters": updated_clusters, "next_step": END}
