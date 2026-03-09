from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from src.agents.state import AgentState
from src.utils.logger import project_logger as logger
from src.config.settings import settings
from src.agents.prompts import SUMMARIZER_PROMPT

class SummarizerNode:
    """The Summarizer Node: Generates 3-bullet points using Light Model."""
    
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm

    def __call__(self, state: AgentState) -> Dict[str, Any]:
        logger.info(f"Summarizer Node: Generating 3-Bullet Points (using {settings.MODEL_LIGHT})...")
        
        clusters = state.get("clusters", [])
        for cluster in clusters:
            article_content = [f"- {a.title}: {a.summary}" for a in cluster.articles]
            formatted_articles = chr(10).join(article_content)
            
            prompt = SUMMARIZER_PROMPT.format(article_content=formatted_articles)
            
            # TODO: Activate LLM
            # response = self.llm.invoke(prompt)
            # Example parsing...
            cluster.summary_3_bullets = [f"Neutral summary point {i+1} for {cluster.main_event}" for i in range(3)]
        
        return {"clusters": clusters, "next_step": "auditor"}
