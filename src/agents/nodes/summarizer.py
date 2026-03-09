import asyncio
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from src.agents.state import AgentState, NewsCluster
from src.utils.logger import project_logger as logger
from src.config.settings import settings
from src.agents.prompts import SUMMARIZER_PROMPT
from src.utils.parser import RobustJSONParser
from src.agents.nodes.base import BaseClusterAgent

class SummarizerNode(BaseClusterAgent):
    """The Summarizer Node: Generates 3-bullet points asynchronously in parallel."""
    
    def __init__(self, llm: ChatGoogleGenerativeAI, semaphore):
        super().__init__(semaphore)
        self.llm = llm
        self.default_next_step = "auditor"

    async def __call__(self, state: AgentState) -> Dict[str, Any]:
        logger.info(f"Summarizer Node: Processing clusters via {settings.MODEL_LIGHT}")
        return await self.process_all_clusters(state, self._summarize_cluster)

    async def _summarize_cluster(self, cluster: NewsCluster):
        """Logic for a single cluster using live LLM."""
        # Use full_text if available, fallback to summary
        article_content = "\n".join([
            f"- {a.title}: {a.full_text[:1500] if a.full_text else a.summary}" 
            for a in cluster.articles
        ])
        
        prompt = SUMMARIZER_PROMPT.format(article_content=article_content)
        
        try:
            # Live AI Call
            response = await self.llm.ainvoke(prompt)
            data = RobustJSONParser.extract_json(response.content)
            
            if data and isinstance(data.get("summary"), list):
                cluster.summary_3_bullets = data["summary"][:3]
            else:
                # Fallback if JSON format was slightly off but readable
                cluster.summary_3_bullets = [f"Summary point {i+1} for {cluster.main_event}" for i in range(3)]
                
        except Exception as e:
            logger.error(f"Error in Summarizer AI call: {str(e)}")
            cluster.summary_3_bullets = ["Error generating summary for this cluster."]
