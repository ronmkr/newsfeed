import asyncio
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from src.agents.state import AgentState
from src.utils.logger import project_logger as logger
from src.config.settings import settings
from src.agents.prompts import SUMMARIZER_PROMPT
from src.utils.parser import RobustJSONParser

class SummarizerNode:
    """The Summarizer Node: Generates 3-bullet points asynchronously in parallel."""
    
    def __init__(self, llm: ChatGoogleGenerativeAI, semaphore: asyncio.Semaphore):
        self.llm = llm
        self.semaphore = semaphore

    async def __call__(self, state: AgentState) -> Dict[str, Any]:
        logger.info(f"Summarizer Node: Generating summaries in parallel (using {settings.MODEL_LIGHT})...")
        
        clusters = state.get("clusters", [])
        if not clusters:
            return {"next_step": "auditor"}

        # Create tasks for all clusters to run in parallel
        tasks = [self._summarize_cluster(cluster) for cluster in clusters]
        await asyncio.gather(*tasks)
        
        return {"clusters": clusters, "next_step": "auditor"}

    async def _summarize_cluster(self, cluster: Any):
        """Summarizes a single cluster using the async LLM call with rate limiting."""
        article_content = [f"- {a.title}: {a.summary}" for a in cluster.articles]
        formatted_articles = "\n".join(article_content)
        
        prompt = SUMMARIZER_PROMPT.format(article_content=formatted_articles)
        
        async with self.semaphore: # Apply rate limiting
            try:
                # TODO: Activate LLM
                # response = await self.llm.ainvoke(prompt)
                # data = RobustJSONParser.extract_json(response.content)
                # if data and "summary" in data:
                #     cluster.summary_3_bullets = data["summary"][:3]
                
                # Simulated delay and logic
                await asyncio.sleep(0.1) 
                cluster.summary_3_bullets = [f"Neutral summary point {i+1} for {cluster.main_event}" for i in range(3)]
            except Exception as e:
                logger.error(f"Error summarizing cluster {cluster.cluster_id}: {str(e)}")
