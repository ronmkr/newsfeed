import asyncio
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from src.agents.state import AgentState
from src.utils.logger import project_logger as logger
from src.config.settings import settings
from src.agents.prompts import AUDITOR_PROMPT
from src.utils.parser import RobustJSONParser

class AuditorNode:
    """The Auditor Node: Asynchronous parallel bias analysis using Heavy Model."""
    
    def __init__(self, llm: ChatGoogleGenerativeAI, semaphore: asyncio.Semaphore):
        self.llm = llm
        self.semaphore = semaphore

    async def __call__(self, state: AgentState) -> Dict[str, Any]:
        logger.info(f"Auditor Node: Analyzing {len(state.get('clusters', []))} clusters in parallel (using {settings.MODEL_HEAVY})...")
        
        clusters = state.get("clusters", [])
        if not clusters:
            return {"next_step": "editor"}

        # Perform bias analysis on all clusters in parallel
        tasks = [self._analyze_cluster(cluster) for cluster in clusters]
        await asyncio.gather(*tasks)
        
        return {
            "clusters": clusters,
            "next_step": "editor"
        }

    async def _analyze_cluster(self, cluster: Any):
        """Analyzes a single cluster using the async heavy model call with rate limiting."""
        article_details = []
        for a in cluster.articles:
            m = a.source_metadata
            meta_str = f"Ownership: {m.ownership}, Lean: {m.ideological_lean}" if m else "Unknown Ownership"
            article_details.append(f"- {a.title} ({a.source})\n  [{meta_str}]")
        
        formatted_details = "\n".join(article_details)
        prompt = AUDITOR_PROMPT.format(article_details=formatted_details)
        
        async with self.semaphore: # Apply rate limiting
            try:
                # TODO: Activate LLM and parse JSON
                # response = await self.llm.ainvoke(prompt)
                # data = RobustJSONParser.extract_json(response.content)
                # if data:
                #     cluster.overall_bias = data.get("bias_score", 0.0)
                #     cluster.reasoning_trace = data.get("ownership_influence_note", "")
                
                # Simulated delay
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f"Error analyzing cluster {cluster.cluster_id}: {str(e)}")
