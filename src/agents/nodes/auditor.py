import asyncio
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from src.agents.state import AgentState, NewsCluster
from src.utils.logger import project_logger as logger
from src.agents.prompts import AUDITOR_PROMPT
from src.utils.parser import RobustJSONParser
from src.agents.nodes.base import BaseClusterAgent

class AuditorNode(BaseClusterAgent):
    """Analyzes ideological bias and framing context for news clusters."""
    
    def __init__(self, llm: ChatGoogleGenerativeAI, semaphore: asyncio.Semaphore):
        super().__init__(semaphore)
        self.llm = llm
        self.default_next_step = "editor"

    async def __call__(self, state: AgentState) -> Dict[str, Any]:
        logger.info(f"Auditor Node: Analyzing {len(state.get('clusters', []))} clusters.")
        return await self.process_all_clusters(state, self._analyze_cluster)

    async def _analyze_cluster(self, cluster: NewsCluster):
        """Asynchronously analyzes bias for a single cluster using LLM."""
        # Collate source and ownership details
        details = []
        for a in cluster.articles:
            m = a.source_metadata
            meta = f"Ownership: {m.ownership}, Lean: {m.ideological_lean}" if m else "Unknown"
            details.append(f"- {a.title} ({a.source})\n  [Meta: {meta}]")
        
        prompt = AUDITOR_PROMPT.format(article_details="\n".join(details))
        
        try:
            # Execute AI Call
            response = await self.llm.ainvoke(prompt)
            data = RobustJSONParser.extract_json(response.content)
            
            if data:
                cluster.overall_bias = float(data.get("bias_score", 0.0))
                cluster.reasoning_trace = data.get("ownership_influence_note", "")
            
        except Exception as e:
            logger.error(f"Audit AI Failure: {str(e)}")
            cluster.reasoning_trace = "Failed to perform bias analysis."
