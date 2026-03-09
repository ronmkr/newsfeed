import asyncio
import re
from typing import List, Any, Callable, Coroutine, Optional, TypeVar
import tldextract
from src.utils.logger import project_logger as logger

T = TypeVar("T")

def clean_text(text: Optional[str]) -> str:
    """
    Standardizes text by removing extra whitespace and special characters.
    
    Args:
        text: The raw string to clean.
    Returns:
        A lowercase, normalized string.
    """
    if not text:
        return ""
    # Remove non-alphanumeric except basic punctuation
    text = re.sub(r'[^\w\s\-\.]', '', text)
    # Collapse multiple spaces and trim
    return re.sub(r'\s+', ' ', text).strip().lower()

def get_registered_domain(url: str) -> Optional[str]:
    """
    Extracts the registered domain (e.g., indiatimes.com) from a URL.
    
    Args:
        url: The URL or domain string.
    Returns:
        The registered domain or None if invalid.
    """
    if not url:
        return None
    try:
        ext = tldextract.extract(url)
        if ext.domain and ext.suffix:
            return f"{ext.domain}.{ext.suffix}".lower()
    except Exception as e:
        logger.debug(f"Domain extraction failed for {url}: {e}")
    return None

async def run_parallel(tasks: List[Coroutine[Any, Any, T]]) -> List[T]:
    """
    Executes a list of coroutines in parallel and returns results.
    
    Args:
        tasks: List of coroutines to execute.
    Returns:
        List of results in order.
    """
    if not tasks:
        return []
    return list(await asyncio.gather(*tasks))

def parse_json_safely(parser_func: Callable[[str], Optional[dict]], raw_text: str) -> Optional[dict]:
    """
    Safely executes a JSON parser function with standardized logging.
    
    Args:
        parser_func: The function to use for parsing.
        raw_text: The string to parse.
    Returns:
        A dictionary or None if parsing fails.
    """
    try:
        return parser_func(raw_text)
    except Exception as e:
        logger.error(f"Structured Parsing Error: {str(e)}")
        return None
