import asyncio
import os
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache

from src.agents.state import AgentState
from src.clustering.engine import ClusteringEngine
from src.config.settings import settings
from src.agents.nodes.scout import ScoutNode
from src.agents.nodes.summarizer import SummarizerNode
from src.agents.nodes.auditor import AuditorNode
from src.agents.nodes.editor import EditorNode

class PipelineGraph:
    """Orchestrates the modular agentic workflow with caching and rate limiting."""
    
    def __init__(self):
        # 1. Enable LLM Caching to save API costs and improve speed
        cache_path = "data/cache/llm_cache.db"
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        set_llm_cache(SQLiteCache(database_path=cache_path))
        
        # 2. Initialize LLM Instances
        self.llm_heavy = ChatGoogleGenerativeAI(
            model=settings.MODEL_HEAVY,
            google_api_key=settings.GOOGLE_API_KEY
        )
        self.llm_light = ChatGoogleGenerativeAI(
            model=settings.MODEL_LIGHT,
            google_api_key=settings.GOOGLE_API_KEY
        )
        
        # 3. Rate Limiting: Max 3 concurrent LLM calls
        self.semaphore = asyncio.Semaphore(settings.CONCURRENCY_LIMIT)
        
        # 4. Initialize Engines and State Graph
        self.clustering_engine = ClusteringEngine()
        self.workflow = StateGraph(AgentState)
        self._build_graph()

    def _should_continue(self, state: AgentState) -> str:
        """Determines next state or forces termination after loop limit."""
        if state.get("loop_count", 0) >= settings.MAX_LOOPS:
            return END
        return state.get("next_step", END)

    def _build_graph(self):
        """Builds the graph nodes and wiring."""
        scout = ScoutNode(self.clustering_engine)
        summarizer = SummarizerNode(self.llm_light, self.semaphore)
        auditor = AuditorNode(self.llm_heavy, self.semaphore)
        editor = EditorNode()

        self.workflow.add_node("scout", scout)
        self.workflow.add_node("summarizer", summarizer)
        self.workflow.add_node("auditor", auditor)
        self.workflow.add_node("editor", editor)

        self.workflow.set_entry_point("scout")

        # Edges
        self.workflow.add_conditional_edges("scout", self._should_continue, {"summarizer": "summarizer", END: END})
        self.workflow.add_edge("summarizer", "auditor")
        self.workflow.add_edge("auditor", "editor")
        self.workflow.add_conditional_edges("editor", self._should_continue, {"scout": "scout", END: END})

    def compile(self, checkpointer=None):
        return self.workflow.compile(checkpointer=checkpointer)

def create_pipeline(checkpointer=None):
    return PipelineGraph().compile(checkpointer=checkpointer)
