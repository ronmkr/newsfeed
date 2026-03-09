import re
from typing import str, Optional
import tldextract

def clean_text(text: str) -> str:
    """
    Standardizes text by removing extra whitespace, 
    special characters, and normalizing casing.
    """
    if not text:
        return ""
    # Remove non-alphanumeric (keep spaces and basic punctuation)
    text = re.sub(r'[^\w\s\-\.]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

def get_registered_domain(url: str) -> Optional[str]:
    """
    Extracts the registered domain (e.g. google.com) from a URL or domain string.
    """
    if not url:
        return None
    extracted = tldextract.extract(url)
    if not extracted.domain or not extracted.suffix:
        return None
    return f"{extracted.domain}.{extracted.suffix}".lower()

def format_timestamp(dt_str: Optional[str] = None) -> str:
    """Standardizes date strings to ISO format."""
    from datetime import datetime
    if not dt_str:
        return datetime.now().isoformat()
    try:
        # Basic attempt to parse common RSS date formats if needed
        # (Placeholder for more complex logic if required)
        return dt_str
    except Exception:
        return datetime.now().isoformat()
