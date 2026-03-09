from typing import List, Dict, Any, TypedDict, Optional, Annotated
from pydantic import BaseModel, Field
import operator

class SourceMetadata(BaseModel):
    name: str
    ownership: str
    funding: str
    ideological_lean: str
    notes: Optional[str] = None

class Article(BaseModel):
    title: str
    link: str
    source: str
    summary: str
    full_text: Optional[str] = None # Added for deeper analysis
    content: Optional[str] = None
    bias_score: Optional[float] = None
    published_at: str
    source_metadata: Optional[SourceMetadata] = None

class NewsCluster(BaseModel):
    cluster_id: str
    main_event: str
    articles: List[Article]
    summary_3_bullets: List[str] = Field(default_factory=list)
    overall_bias: float = 0.0
    reasoning_trace: Optional[str] = None # Added for transparency
    is_blindspot: bool = False

class AgentState(TypedDict):
    # This is the shared state between all agents
    # Use Annotated with operator.add to allow list merging if needed
    clusters: Annotated[List[NewsCluster], operator.add]
    current_cluster_index: int
    raw_data: List[Dict[str, Any]]
    errors: List[str]
    next_step: str
    loop_count: int # Max 3 loops
