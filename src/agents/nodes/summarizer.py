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
    """Generates neutral, fact-based summaries for news clusters."""
    
    def __init__(self, llm: ChatGoogleGenerativeAI, semaphore: asyncio.Semaphore):
        super().__init__(semaphore)
        self.llm = llm
        self.default_next_step = "auditor"

    async def __call__(self, state: AgentState) -> Dict[str, Any]:
        logger.info(f"Summarizer Node: Processing {len(state.get('clusters', []))} clusters.")
        return await self.process_all_clusters(state, self._summarize_cluster)

    async def _summarize_cluster(self, cluster: NewsCluster):
        """Asynchronously summarizes a single cluster using LLM."""
        # Collate text from all articles in cluster
        article_text = "\n".join([
            f"- {a.title}: {a.full_text[:1200] if a.full_text else a.summary}" 
            for a in cluster.articles
        ])
        
        prompt = SUMMARIZER_PROMPT.format(article_content=article_text)
        
        try:
            # Execute AI Call
            response = await self.llm.ainvoke(prompt)
            data = RobustJSONParser.extract_json(response.content)
            
            if data and isinstance(data.get("summary"), list):
                cluster.summary_3_bullets = data["summary"][:3]
            else:
                cluster.summary_3_bullets = ["(No summary generated)"]
                
        except Exception as e:
            logger.error(f"Summarization AI Failure: {str(e)}")
            cluster.summary_3_bullets = ["Analysis timed out or failed."]
