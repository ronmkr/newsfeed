import asyncio
import aiohttp
import feedparser
import trafilatura
from typing import Any, Optional
from src.utils.logger import project_logger as logger

class AsyncRSSFetcher:
    """Specialized asynchronous fetcher for RSS feeds."""
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.timeout = aiohttp.ClientTimeout(total=15)

    async def fetch(self, feed_url: str) -> Optional[Any]:
        try:
            async with self.session.get(feed_url, timeout=self.timeout) as response:
                if response.status != 200: return None
                content = await response.text()
                feed = feedparser.parse(content)
                return feed if feed.entries else None
        except Exception as e:
            logger.debug(f"RSS Fetch Error {feed_url}: {str(e)}")
            return None

class FullTextExtractor:
    """Extracts and sanitizes main content from news URLs."""
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.timeout = aiohttp.ClientTimeout(total=20)

    async def extract(self, url: str) -> Optional[str]:
        try:
            async with self.session.get(url, timeout=self.timeout) as response:
                if response.status != 200: return None
                html = await response.text()
                text = trafilatura.extract(html)
                return text if (text and self._is_valid(text)) else None
        except Exception:
            return None

    def _is_valid(self, text: str) -> bool:
        if len(text) < 300: return False
        return not any(term in text.lower() for term in ["javascript is disabled", "enable cookies", "access denied"])
