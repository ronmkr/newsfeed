from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class RawArticle(BaseModel):
    title: str
    link: str
    source: str
    summary: str
    published_at: str
    ingested_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
