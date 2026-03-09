from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from src.agents.state import AgentState
from src.utils.logger import project_logger as logger
from src.config.settings import settings
from src.agents.prompts import AUDITOR_PROMPT

class AuditorNode:
    """The Auditor Node: Analyzes ideological bias using Heavy Model."""
    
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm

    def __call__(self, state: AgentState) -> Dict[str, Any]:
        logger.info(f"Auditor Node: Analyzing Ideological Leaning (using {settings.MODEL_HEAVY})...")
        
        clusters = state.get("clusters", [])
        updated_clusters = []
        
        for cluster in clusters:
            article_details = []
            for a in cluster.articles:
                m = a.source_metadata
                meta_str = f"Ownership: {m.ownership}, Lean: {m.ideological_lean}" if m else "Unknown Ownership"
                article_details.append(f"- {a.title} ({a.source})\n  [{meta_str}]")
            
            formatted_details = chr(10).join(article_details)
            prompt = AUDITOR_PROMPT.format(article_details=formatted_details)
            
            # TODO: Activate LLM and parse JSON
            # response = self.llm.invoke(prompt)
            # Simulated analysis logic...
            
            updated_clusters.append(cluster)
        
        return {
            "clusters": updated_clusters,
            "next_step": "editor"
        }
