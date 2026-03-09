import json
import os
from typing import Dict, Any, Optional
from pydantic import BaseModel
import tldextract
from src.utils.logger import project_logger as logger

class SourceMetadata(BaseModel):
    name: str
    ownership: str
    funding: str
    ideological_lean: str # Left, Center-Left, Center, Center-Right, Right
    notes: Optional[str] = None

class SourceKBManager:
    """Handles loading and accessing source metadata from JSON."""
    
    def __init__(self, json_path: str = "data/source_kb.json"):
        self.json_path = json_path
        self.kb: Dict[str, SourceMetadata] = {}
        self._load_kb()

    def _load_kb(self):
        """Loads metadata from JSON into Pydantic models."""
        if not os.path.exists(self.json_path):
            logger.warning(f"Source KB file not found at {self.json_path}. Using empty KB.")
            return

        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.kb = {k: SourceMetadata(**v) for k, v in data.items()}
            logger.info(f"Loaded {len(self.kb)} sources from Knowledge Base.")
        except Exception as e:
            logger.error(f"Failed to load Source KB: {str(e)}")

    def get_metadata(self, url_or_domain: str) -> Optional[SourceMetadata]:
        """Robustly extracts registered domain and look up metadata."""
        if not url_or_domain:
            return None
            
        extracted = tldextract.extract(url_or_domain)
        registered_domain = extracted.registered_domain.lower()
        
        return self.kb.get(registered_domain)

# Singleton instance for project-wide use
source_kb_manager = SourceKBManager()

def get_source_metadata(url_or_domain: str) -> Optional[SourceMetadata]:
    """Helper function to maintain backwards compatibility."""
    return source_kb_manager.get_metadata(url_or_domain)
