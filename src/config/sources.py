from typing import Dict, Any, Optional
from pydantic import BaseModel
import tldextract

class SourceMetadata(BaseModel):
    name: str
    ownership: str
    funding: str
    ideological_lean: str # Left, Center-Left, Center, Center-Right, Right
    notes: Optional[str] = None

# A foundational "Source Knowledge Base" for Indian Media
# Keys are now 'registered_domain' (domain.suffix) for robust matching
SOURCE_KB: Dict[str, SourceMetadata] = {
    "thehindu.com": SourceMetadata(
        name="The Hindu",
        ownership="Kasturi & Sons Ltd (Family-owned)",
        funding="Advertising & Subscriptions",
        ideological_lean="Center-Left",
        notes="Known for traditional, sober reporting; often critical of government policy."
    ),
    "ndtv.com": SourceMetadata(
        name="NDTV",
        ownership="AMG Media Networks (Adani Group)",
        funding="Corporate-owned",
        ideological_lean="Center to Center-Right",
        notes="Shifted from Center-Left to Center/Center-Right after Adani acquisition."
    ),
    "republicworld.com": SourceMetadata(
        name="Republic TV",
        ownership="Arnab Goswami (Arg Outlier Media)",
        funding="Advertising",
        ideological_lean="Right",
        notes="Known for high-decibel, nationalist framing; strongly pro-government."
    ),
    "indianexpress.com": SourceMetadata(
        name="The Indian Express",
        ownership="Viveck Goenka (Indian Express Group)",
        funding="Advertising & Subscriptions",
        ideological_lean="Center",
        notes="Strong focus on investigative journalism; maintains a 'neutral' but critical stance."
    ),
    "thewire.in": SourceMetadata(
        name="The Wire",
        ownership="Foundation for Independent Journalism (Non-profit)",
        funding="Grants & Individual Donations",
        ideological_lean="Left",
        notes="Aggressively critical of the establishment; focuses on civil liberties."
    ),
    "opindia.com": SourceMetadata(
        name="OpIndia",
        ownership="Aasthi Media",
        funding="Advertising & Donations",
        ideological_lean="Right",
        notes="Digital-first outlet; often focuses on 'fact-checking' mainstream media from a right-wing lens."
    ),
    "indiatimes.com": SourceMetadata(
        name="The Times of India",
        ownership="Bennett, Coleman and Co. Ltd (Jain Family)",
        funding="Advertising (High volume)",
        ideological_lean="Center-Right",
        notes="World's largest-circulated English daily; often pragmatic and pro-business."
    ),
    "sakal.com": SourceMetadata(
        name="Sakal",
        ownership="Sakal Media Group (Pawar Family)",
        funding="Advertising",
        ideological_lean="Center",
        notes="Major Marathi daily with deep regional influence."
    )
}

def get_source_metadata(url_or_domain: str) -> Optional[SourceMetadata]:
    """
    Robustly extracts the registered domain (e.g., indiatimes.com) 
    and looks it up in the Source Knowledge Base.
    """
    if not url_or_domain:
        return None
        
    extracted = tldextract.extract(url_or_domain)
    registered_domain = extracted.registered_domain.lower()
    
    return SOURCE_KB.get(registered_domain)
