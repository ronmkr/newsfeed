from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from src.agents.state import AgentState, NewsCluster, Article
from src.clustering.engine import ClusteringEngine
from src.utils.logger import project_logger as logger
from src.config.settings import settings
from src.config.sources import get_source_metadata

class PipelineGraph:
    """Defines the agentic workflow for the daily news pipeline."""
    
    def __init__(self):
        # Heavy Model: Gemini 1.5 Pro (Bias, Framing, Deep Context)
        self.llm_heavy = ChatGoogleGenerativeAI(
            model=settings.MODEL_HEAVY,
            google_api_key=settings.OPENAI_API_KEY
        )
        # Light Model: Gemini 1.5 Flash (Summarization, Extraction, Clean-up)
        self.llm_light = ChatGoogleGenerativeAI(
            model=settings.MODEL_LIGHT,
            google_api_key=settings.OPENAI_API_KEY
        )
        self.clustering_engine = ClusteringEngine()
        self.workflow = StateGraph(AgentState)
        self._build_graph()

    def scout_node(self, state: AgentState) -> Dict[str, Any]:
        """The Scout: Logic to process raw ingestion data into clusters and enrich with metadata."""
        logger.info("Scout Node: Identifying Story Threads and Enriching Metadata...")
        
        # Increment loop count or initialize it
        loop_count = state.get("loop_count", 0) + 1
        
        if not state.get("raw_data"):
            logger.warning("Scout Node: No raw data provided to analyze.")
            return {"next_step": END, "errors": ["No raw data found."], "loop_count": loop_count}
        
        # Use ClusteringEngine to group articles
        clusters = self.clustering_engine.group_articles(state["raw_data"])
        
        # Enrich articles with Source Metadata
        for cluster in clusters:
            for article in cluster.articles:
                article.source_metadata = get_source_metadata(article.source)
        
        return {
            "clusters": clusters,
            "next_step": "summarizer" if clusters else END,
            "loop_count": loop_count
        }

    def summarizer_node(self, state: AgentState) -> Dict[str, Any]:
        """The Summarizer: Uses Gemini 1.5 Flash (Light Model) for efficient summaries."""
        logger.info(f"Summarizer Node: Generating 3-Bullet Points (using {settings.MODEL_LIGHT})...")
        
        for cluster in state["clusters"]:
            # Prompt for a neutral, 3-bullet summary
            article_content = [f"- {a.title}: {a.summary}" for a in cluster.articles]
            prompt = f"Summarize the following articles into 3 neutral bullet points:\n\n{chr(10).join(article_content)}"
            
            # Using Light Model for speed and cost efficiency
            # response = self.llm_light.invoke(prompt)
            # Simulated for now
            cluster.summary_3_bullets = [f"Neutral summary point {i+1} for {cluster.main_event}" for i in range(3)]
        
        return {"next_step": "auditor"}

    def auditor_node(self, state: AgentState) -> Dict[str, Any]:
        """The Auditor: Logic to analyze ideological leaning with Ownership Context using Heavy Model."""
        logger.info(f"Auditor Node: Analyzing Ideological Leaning (using {settings.MODEL_HEAVY})...")
        
        updated_clusters = []
        for cluster in state["clusters"]:
            # Detailed prompt for heavy model analysis
            article_details = []
            for a in cluster.articles:
                m = a.source_metadata
                meta_str = f"Ownership: {m.ownership}, Lean: {m.ideological_lean}" if m else "Unknown Ownership"
                article_details.append(f"- {a.title} ({a.source})\n  [{meta_str}]")
            
            prompt = f"Analyze ideological framing for this cluster:\n\n{chr(10).join(article_details)}"
            
            # Using Heavy Model for nuanced bias detection
            # response = self.llm_heavy.invoke(prompt)
            # Simulated analysis logic...
            updated_clusters.append(cluster)
        
        return {
            "clusters": updated_clusters,
            "next_step": "editor"
        }

    def editor_node(self, state: AgentState) -> Dict[str, Any]:
        """The Editor-in-Chief: Final Quality Control and Blindspot Detection."""
        logger.info("Editor-in-Chief Node: Finalizing Quality Control and Detecting Blindspots...")
        
        updated_clusters = []
        for cluster in state["clusters"]:
            # Logic: Check if major ideological perspectives are missing
            leans = [a.source_metadata.ideological_lean for a in cluster.articles if a.source_metadata]
            
            has_left = any("Left" in l for l in leans)
            has_right = any("Right" in l for l in leans)
            
            # A "Blindspot" is when a story is ONLY covered by one side
            if (has_left and not has_right) or (has_right and not has_left):
                cluster.is_blindspot = True
                logger.warning(f"BLINDSPOT DETECTED: {cluster.main_event}")
            
            updated_clusters.append(cluster)
            
        # Loop back to Scout if deep blindspot detected, but only if loop_count < 3
        if state.get("loop_count", 0) >= 3:
            logger.warning("Max loop count (3) reached. Forcing termination.")
            return {"clusters": updated_clusters, "next_step": END}
            
        return {"clusters": updated_clusters, "next_step": END}

    def _should_continue(self, state: AgentState) -> str:
        """Logic to decide the next node based on state['next_step'] and loop_count."""
        if state.get("loop_count", 0) >= 3:
            return END
        return state.get("next_step", END)

    def _build_graph(self):
        """Constructs the state machine graph."""
        self.workflow.add_node("scout", self.scout_node)
        self.workflow.add_node("summarizer", self.summarizer_node)
        self.workflow.add_node("auditor", self.auditor_node)
        self.workflow.add_node("editor", self.editor_node)

        # Set Entry Point
        self.workflow.set_entry_point("scout")

        # Define Edges with Conditional Logic and Loop Protection
        self.workflow.add_conditional_edges("scout", self._should_continue, {"summarizer": "summarizer", END: END})
        self.workflow.add_edge("summarizer", "auditor")
        self.workflow.add_edge("auditor", "editor")
        self.workflow.add_conditional_edges("editor", self._should_continue, {"scout": "scout", END: END})

    def compile(self):
        return self.workflow.compile()

# Factory function for easy instantiation
def create_pipeline():
    return PipelineGraph().compile()
