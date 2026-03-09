from typing import List, Dict, Any, Optional
import feedparser
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config.settings import settings
from src.utils.logger import project_logger as logger
from src.ingestion.models import RawArticle

class RSSFetcher:
    """Specialized fetcher for RSS feeds."""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        before_sleep=lambda retry_state: logger.warning(f"Retrying RSS fetch (Attempt {retry_state.attempt_number})...")
    )
    def fetch(self, feed_url: str) -> Optional[Any]:
        """Fetch raw feed data."""
        logger.info(f"Fetching RSS: {feed_url}")
        feed = feedparser.parse(feed_url)

        if hasattr(feed, 'status') and feed.status != 200:
            logger.error(f"Failed to fetch {feed_url}: HTTP Status {feed.status}")
            return None

        if not feed.entries:
            logger.warning(f"No entries found for {feed_url}")
            return None

        return feed

class IngestionCoordinator:
    """Orchestrates different fetchers to gather raw articles."""

    def __init__(self):
        self.rss_fetcher = RSSFetcher()

    def fetch_all(self, rss_feeds: List[str]) -> List[RawArticle]:
        """Coordinatest the fetching of articles from all sources."""
        all_raw_articles = []

        for url in rss_feeds:
            try:
                # Normalize source domain
                from src.config.sources import get_source_metadata
                source_domain = url.split("//")[-1].split("/")[0]

                feed_data = self.rss_fetcher.fetch(url)
                if feed_data:
                    processed = self._process_rss_entries(feed_data, source_domain)
                    all_raw_articles.extend(processed)

            except Exception as e:
                logger.exception(f"Unexpected error fetching from {url}: {str(e)}")

        logger.success(f"Ingestion complete. Total raw articles: {len(all_raw_articles)}")
        return all_raw_articles

    def _process_rss_entries(self, feed: Any, source_name: str) -> List[RawArticle]:
        """Standardizes feed entries into RawArticle models."""
        from datetime import datetime
        articles = []
        for entry in feed.entries:
            try:
                article = RawArticle(
                    title=entry.get("title", "N/A"),
                    link=entry.get("link", "N/A"),
                    source=source_name,
                    summary=entry.get("summary", ""),
                    published_at=entry.get("published", datetime.now().isoformat())
                )
                articles.append(article)
            except Exception as e:
                logger.error(f"Error processing entry: {str(e)}")
        return articles
