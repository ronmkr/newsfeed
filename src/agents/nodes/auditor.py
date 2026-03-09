from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from src.agents.state import AgentState, NewsCluster
from src.utils.logger import project_logger as logger
from src.config.settings import settings
from src.agents.prompts import AUDITOR_PROMPT
from src.utils.parser import RobustJSONParser
from src.agents.nodes.base import BaseClusterAgent

class AuditorNode(BaseClusterAgent):
    """The Auditor Node: Analyzes ideological bias using live Heavy Model."""
    
    def __init__(self, llm: ChatGoogleGenerativeAI, semaphore):
        super().__init__(semaphore)
        self.llm = llm
        self.default_next_step = "editor"

    async def __call__(self, state: AgentState) -> Dict[str, Any]:
        logger.info(f"Auditor Node: Processing clusters via {settings.MODEL_HEAVY}")
        return await self.process_all_clusters(state, self._analyze_cluster)

    async def _analyze_cluster(self, cluster: NewsCluster):
        """Analyzes a single cluster using live LLM reasoning."""
        article_details = "\n".join([
            f"- {a.title} ({a.source})\n  [Ownership: {a.source_metadata.ownership if a.source_metadata else 'Unknown'}]" 
            for a in cluster.articles
        ])
        
        prompt = AUDITOR_PROMPT.format(article_details=article_details)
        
        try:
            # Live AI call for deep reasoning
            response = await self.llm.ainvoke(prompt)
            data = RobustJSONParser.extract_json(response.content)
            
            if data:
                cluster.overall_bias = float(data.get("bias_score", 0.0))
                cluster.reasoning_trace = data.get("ownership_influence_note", "")
                # We can also store missing_perspectives if we expand the model
            
        except Exception as e:
            logger.error(f"Error in Auditor AI call: {str(e)}")
            cluster.reasoning_trace = "Failed to perform bias analysis for this cluster."
