import asyncio
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver # Added for persistence
from langchain_google_genai import ChatGoogleGenerativeAI

from src.agents.state import AgentState
from src.clustering.engine import ClusteringEngine
from src.config.settings import settings
from src.agents.nodes.scout import ScoutNode
from src.agents.nodes.summarizer import SummarizerNode
from src.agents.nodes.auditor import AuditorNode
from src.agents.nodes.editor import EditorNode

class PipelineGraph:
    """Orchestrates the modular agentic workflow."""
    
    def __init__(self):
        # LLM Instances
        self.llm_heavy = ChatGoogleGenerativeAI(
            model=settings.MODEL_HEAVY,
            google_api_key=settings.OPENAI_API_KEY
        )
        self.llm_light = ChatGoogleGenerativeAI(
            model=settings.MODEL_LIGHT,
            google_api_key=settings.OPENAI_API_KEY
        )
        
        # Rate Limiting: Max 3 concurrent LLM calls
        self.semaphore = asyncio.Semaphore(3)
        
        # Engine
        self.clustering_engine = ClusteringEngine()
        
        # Initialize Graph
        self.workflow = StateGraph(AgentState)
        self._build_graph()

    def _should_continue(self, state: AgentState) -> str:
        """Determines the next step or forces termination after 3 loops."""
        if state.get("loop_count", 0) >= 3:
            return END
        return state.get("next_step", END)

    def _build_graph(self):
        """Builds the graph using modular nodes."""
        
        # Instantiate nodes
        scout = ScoutNode(self.clustering_engine)
        summarizer = SummarizerNode(self.llm_light, self.semaphore)
        auditor = AuditorNode(self.llm_heavy, self.semaphore)
        editor = EditorNode()

        # Add Nodes
        self.workflow.add_node("scout", scout)
        self.workflow.add_node("summarizer", summarizer)
        self.workflow.add_node("auditor", auditor)
        self.workflow.add_node("editor", editor)

        # Entry Point
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
