import asyncio
import aiohttp
import feedparser
import trafilatura
from typing import Any, Optional
from src.utils.logger import project_logger as logger

class AsyncRSSFetcher:
    """Asynchronously fetches and parses RSS feed content."""
    
    def __init__(self, session: aiohttp.ClientSession, timeout: int = 15):
        self.session = session
        self.timeout = aiohttp.ClientTimeout(total=timeout)

    async def fetch(self, feed_url: str) -> Optional[Any]:
        """
        Fetches RSS content and parses it into a feedparser object.
        
        Args:
            feed_url: The URL of the RSS feed.
        Returns:
            Parsed feed object or None if fetch fails.
        """
        try:
            async with self.session.get(feed_url, timeout=self.timeout) as response:
                if response.status != 200:
                    logger.debug(f"HTTP {response.status} for {feed_url}")
                    return None
                
                content = await response.text()
                feed = feedparser.parse(content)
                return feed if feed.entries else None
        except Exception as e:
            logger.debug(f"RSS Fetch Exception {feed_url}: {str(e)}")
            return None

class FullTextExtractor:
    """Extracts and sanitizes clean text from news article URLs."""
    
    def __init__(self, session: aiohttp.ClientSession, timeout: int = 20):
        self.session = session
        self.timeout = aiohttp.ClientTimeout(total=timeout)

    async def extract(self, url: str) -> Optional[str]:
        """
        Fetches HTML and extracts main content via trafilatura.
        
        Args:
            url: The link to the news article.
        Returns:
            Cleaned article body or None if extraction fails or text is invalid.
        """
        try:
            async with self.session.get(url, timeout=self.timeout) as response:
                if response.status != 200:
                    return None
                
                html = await response.text()
                text = trafilatura.extract(html)
                
                return text if (text and self._is_valid(text)) else None
        except Exception:
            return None

    def _is_valid(self, text: str) -> bool:
        """Applies heuristic filters to exclude junk content."""
        if len(text) < 300:
            return False
        
        junk_indicators = [
            "javascript is disabled", 
            "enable cookies", 
            "access denied", 
            "forbidden",
            "please subscribe"
        ]
        text_lower = text.lower()
        return not any(indicator in text_lower for indicator in junk_indicators)
