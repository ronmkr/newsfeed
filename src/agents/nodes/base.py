import asyncio
from typing import Dict, Any, List, Callable, Coroutine
from src.agents.state import AgentState, NewsCluster
from src.utils.helpers import run_parallel

class BaseClusterAgent:
    """Base class for agents that process clusters in parallel."""
    
    def __init__(self, semaphore: asyncio.Semaphore):
        self.semaphore = semaphore

    async def process_all_clusters(self, state: AgentState, processor_func: Callable[[NewsCluster], Coroutine]) -> Dict[str, Any]:
        """Generic parallel processor for all clusters in the state."""
        clusters = state.get("clusters", [])
        if not clusters:
            return {"next_step": self.default_next_step}

        # Apply processor function to all clusters in parallel
        await run_parallel([self._safe_process(c, processor_func) for c in clusters])
        
        return {"clusters": clusters, "next_step": self.default_next_step}

    async def _safe_process(self, cluster: NewsCluster, processor_func: Callable):
        """Wraps the processor function with a semaphore for rate limiting."""
        async with self.semaphore:
            await processor_func(cluster)
