from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class RawArticle(BaseModel):
    """
    Data model representing a freshly ingested news article.
    
    Attributes:
        title: The headline of the article.
        link: The source URL.
        source: The registered domain of the publisher.
        summary: Short snippet or RSS summary.
        full_text: Extracted article body content.
        published_at: Original publication timestamp string.
        ingested_at: ISO timestamp of when the article entered the pipeline.
    """
    title: str
    link: str
    source: str
    summary: str
    full_text: Optional[str] = None
    published_at: str
    ingested_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Converts model to dictionary for shared agent state."""
        return self.model_dump()
