import asyncio
import re
from typing import List, Any, Callable, Coroutine, Optional
import tldextract
from src.utils.logger import project_logger as logger

def clean_text(text: str) -> str:
    """Standardizes text by removing extra whitespace and special characters."""
    if not text: return ""
    text = re.sub(r'[^\w\s\-\.]', '', text)
    return re.sub(r'\s+', ' ', text).strip().lower()

def get_registered_domain(url: str) -> Optional[str]:
    """Extracts registered domain (e.g., indiatimes.com) from a URL."""
    if not url: return None
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}".lower() if ext.domain and ext.suffix else None

async def run_parallel(tasks: List[Coroutine]) -> List[Any]:
    """Uniformly executes a list of coroutines in parallel."""
    if not tasks: return []
    return await asyncio.gather(*tasks)

def parse_json_safely(parser_func: Callable, raw_text: str) -> Optional[dict]:
    """Wrapper for robust parsing with standardized error logging."""
    try:
        return parser_func(raw_text)
    except Exception as e:
        logger.error(f"Parsing Error: {str(e)}")
        return None
