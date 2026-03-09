import asyncio
from typing import Dict, Any, List, Callable, Coroutine
from src.agents.state import AgentState, NewsCluster
from src.utils.helpers import run_parallel

class BaseClusterAgent:
    """
    Abstract-style base for agents processing news clusters concurrently.
    
    This class handles the boilerplate of parallel execution and 
    rate limiting across multiple clusters in the pipeline state.
    """
    
    def __init__(self, semaphore: asyncio.Semaphore):
        """
        Args:
            semaphore: Shared concurrency control object.
        """
        self.semaphore = semaphore
        self.default_next_step = "end" # Default transition

    async def process_all_clusters(
        self, 
        state: AgentState, 
        processor_func: Callable[[NewsCluster], Coroutine]
    ) -> Dict[str, Any]:
        """
        Generic entry point for parallel cluster analysis.
        
        Args:
            state: The current LangGraph state.
            processor_func: The async method to apply to each cluster.
        Returns:
            Dictionary with updated clusters and the next state transition.
        """
        clusters = state.get("clusters", [])
        if not clusters:
            return {"next_step": self.default_next_step}

        # Apply processor function to all clusters in parallel with rate limit
        await run_parallel([self._safe_process(c, processor_func) for c in clusters])
        
        return {"clusters": clusters, "next_step": self.default_next_step}

    async def _safe_process(self, cluster: NewsCluster, processor_func: Callable):
        """Wraps the node logic with a semaphore context manager."""
        async with self.semaphore:
            await processor_func(cluster)
