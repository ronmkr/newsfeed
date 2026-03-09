import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

import feedparser
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config.settings import settings
from src.utils.logger import project_logger as logger

class NewsCollector:
    """Class to fetch and ingest news from various RSS feeds."""
    def __init__(self):
        self.raw_data_dir = settings.RAW_DATA_PATH
        os.makedirs(self.raw_data_dir, exist_ok=True)
        logger.info(f"Initialized NewsCollector at {self.raw_data_dir}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        before_sleep=lambda retry_state: logger.warning(f"Retrying fetch (Attempt {retry_state.attempt_number})...")
    )
    def fetch_feed(self, feed_url: str) -> Optional[Dict[str, Any]]:
        """Fetch news from a single RSS feed URL."""
        logger.info(f"Fetching from feed: {feed_url}")
        feed = feedparser.parse(feed_url)

        if hasattr(feed, 'status') and feed.status != 200:
            logger.error(f"Failed to fetch {feed_url}: HTTP Status {feed.status}")
            return None

        if not feed.entries:
            logger.warning(f"No entries found for feed: {feed_url}")
            return None

        logger.success(f"Fetched {len(feed.entries)} articles from {feed_url}")
        return feed

    def process_entries(self, feed: Any, source_name: str) -> List[Dict[str, Any]]:
        """Standardize raw feed entries into a cleaner format."""
        articles = []
        for entry in feed.entries:
            article = {
                "title": entry.get("title", "N/A"),
                "link": entry.get("link", "N/A"),
                "published_at": entry.get("published", datetime.now().isoformat()),
                "summary": entry.get("summary", ""),
                "source": source_name,
                "ingested_at": datetime.now().isoformat()
            }
            articles.append(article)
        return articles

    def run_ingestion(self):
        """Main execution loop for the daily ingestion run."""
        logger.info("Starting Daily Ingestion Batch Run...")
        all_articles = []

        for feed_url in settings.RSS_FEEDS:
            try:
                # Basic source name extraction
                source_domain = feed_url.split("//")[-1].split("/")[0]
                feed_data = self.fetch_feed(feed_url)

                if feed_data:
                    processed = self.process_entries(feed_data, source_domain)
                    all_articles.extend(processed)

            except Exception as e:
                logger.exception(f"Unexpected error during ingestion from {feed_url}: {str(e)}")

        # Save raw articles for the day
        if all_articles:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.raw_data_dir, f"raw_news_{timestamp}.json")

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_articles, f, indent=4, ensure_ascii=False)

            logger.success(f"Batch ingestion complete. Total articles stored: {len(all_articles)}")
            logger.info(f"Data saved to {output_file}")
        else:
            logger.warning("No articles fetched in this run.")

if __name__ == "__main__":
    collector = NewsCollector()
    collector.run_ingestion()
