import asyncio
import aiohttp
import feedparser
import trafilatura
from typing import List, Dict, Any, Optional
from datetime import datetime

from src.utils.logger import project_logger as logger
from src.ingestion.models import RawArticle
from src.utils.helpers import clean_text, get_registered_domain

class AsyncRSSFetcher:
    """Specialized asynchronous fetcher for RSS feeds."""
    
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.timeout = aiohttp.ClientTimeout(total=15)

    async def fetch(self, feed_url: str) -> Optional[Any]:
        """Fetch raw feed data asynchronously."""
        try:
            logger.debug(f"Fetching RSS: {feed_url}")
            async with self.session.get(feed_url, timeout=self.timeout) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch {feed_url}: HTTP {response.status}")
                    return None
                
                content = await response.text()
                feed = feedparser.parse(content)
                return feed if feed.entries else None
        except Exception as e:
            logger.error(f"Error fetching {feed_url}: {str(e)}")
        return None

class FullTextExtractor:
    """Extracts and sanitizes main content from news URLs."""
    
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.timeout = aiohttp.ClientTimeout(total=20)

    async def extract(self, url: str) -> Optional[str]:
        """Fetches, extracts, and sanitizes full text."""
        try:
            async with self.session.get(url, timeout=self.timeout) as response:
                if response.status != 200:
                    return None
                
                html = await response.text()
                text = trafilatura.extract(html)
                
                if text and self._is_valid(text):
                    return text
                return None
        except Exception:
            return None

    def _is_valid(self, text: str) -> bool:
        """Heuristic check for valid news content."""
        if len(text) < 300:
            return False
        junk_terms = ["javascript is disabled", "enable cookies", "access denied"]
        return not any(term in text.lower() for term in junk_terms)

class IngestionCoordinator:
    """Orchestrates parallel fetching and de-duplication."""
    
    async def fetch_all(self, rss_feeds: List[str]) -> List[RawArticle]:
        """Main entry point for gathering unique, enriched articles."""
        all_raw = []
        
        async with aiohttp.ClientSession() as session:
            # 1. Parallel RSS Poll
            fetcher = AsyncRSSFetcher(session)
            tasks = [fetcher.fetch(url) for url in rss_feeds]
            results = await asyncio.gather(*tasks)
            
            for url, feed in zip(rss_feeds, results):
                if feed:
                    domain = get_registered_domain(url) or "unknown"
                    all_raw.extend(self._parse_entries(feed, domain))
            
            # 2. De-duplicate
            unique = self.deduplicate(all_raw)
            
            # 3. Enrich with Full Text (Parallel)
            extractor = FullTextExtractor(session)
            # Batching to 50 for stability
            await asyncio.gather(*[self._enrich(extractor, a) for a in unique[:50]])
            
        logger.success(f"Ingested {len(unique)} unique articles.")
        return unique

    async def _enrich(self, extractor: FullTextExtractor, article: RawArticle):
        article.full_text = await extractor.extract(article.link)

    def deduplicate(self, articles: List[RawArticle]) -> List[RawArticle]:
        """Removes duplicates using normalized titles and URLs."""
        seen_urls, seen_titles, unique = set(), set(), []
        for art in articles:
            url_key = art.link.strip().lower()
            title_key = clean_text(art.title)
            
            if url_key not in seen_urls and title_key not in seen_titles:
                unique.append(art)
                seen_urls.add(url_key)
                seen_titles.add(title_key)
        return unique

    def _parse_entries(self, feed: Any, source: str) -> List[RawArticle]:
        """Maps raw feed entries to models."""
        return [
            RawArticle(
                title=e.get("title", "N/A"),
                link=e.get("link", "N/A"),
                source=source,
                summary=e.get("summary", ""),
                published_at=e.get("published", datetime.now().isoformat())
            ) for e in feed.entries
        ]
