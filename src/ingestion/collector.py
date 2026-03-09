import asyncio
import aiohttp
import feedparser
from datetime import datetime
from typing import List, Any, Optional

from src.utils.logger import project_logger as logger
from src.ingestion.models import RawArticle
from src.utils.helpers import clean_text, get_registered_domain, run_parallel
from src.ingestion.discovery import NewsDiscoverySpider
from src.ingestion.sitemaps import SitemapDiscoveryEngine
from src.ingestion.fetchers import FullTextExtractor, AsyncRSSFetcher # Assuming extracted

class IngestionCoordinator:
    """Orchestrates triple-track ingestion using functional patterns."""
    
    def __init__(self):
        self.discovery_sites = ["https://theprint.in", "https://thewire.in", "https://scroll.in", "https://www.thequint.com"]
        self.sitemap_urls = [
            "https://www.thehindu.com/sitemap/googlenews.xml",
            "https://indianexpress.com/news-sitemap.xml",
            "https://thewire.in/sitemap.xml",
            "https://theprint.in/news-sitemap.xml",
            "https://www.ndtv.com/sitemaps/india-news.xml"
        ]

    async def fetch_all(self, rss_feeds: List[str]) -> List[RawArticle]:
        async with aiohttp.ClientSession() as session:
            # 1. Initialize Engines
            rss_fetcher = AsyncRSSFetcher(session)
            sitemap_engine = SitemapDiscoveryEngine(session)
            spider = NewsDiscoverySpider(session)
            extractor = FullTextExtractor(session)

            # 2. Functional Task Mapping
            logger.info("Gathering news from all tracks...")
            results = await run_parallel([
                run_parallel([rss_fetcher.fetch(url) for url in rss_feeds]),
                run_parallel([sitemap_engine.get_links_from_sitemap(url) for url in self.sitemap_urls]),
                run_parallel([spider.discover_links(url) for url in self.discovery_sites])
            ])
            
            rss_results, sitemap_links, spider_links = results

            # 3. List Comprehensions for Processing
            all_raw = []
            # Process RSS results
            for url, feed in zip(rss_feeds, rss_results):
                if feed: all_raw.extend(self._map_feed_to_articles(feed, get_registered_domain(url) or "unknown"))
            
            # Process Discovered Links (Sitemaps + Spiders)
            discovered = [link for sublist in (sitemap_links + spider_links) for link in sublist]
            all_raw.extend([RawArticle(title="Discovered Article", link=l, source=get_registered_domain(l) or "unknown", summary="", published_at=datetime.now().isoformat()) for l in discovered])

            # 4. Deduplicate and Enrich
            unique = self.deduplicate(all_raw)
            # Use a semaphore to limit concurrent connections during enrichment
            sem = asyncio.Semaphore(15)
            
            async def bounded_enrich(article):
                async with sem:
                    await self._enrich(extractor, article)
                    
            await run_parallel([bounded_enrich(a) for a in unique])
            
        final = [a for a in unique if a.full_text]
        logger.success(f"Ingestion complete: {len(final)} articles ready out of {len(unique)} unique URLs.")
        return final

    def deduplicate(self, articles: List[RawArticle]) -> List[RawArticle]:
        seen_urls, seen_titles = set(), set()
        def is_unique(a):
            url, title = a.link.strip().lower(), clean_text(a.title)
            if url in seen_urls or title in seen_titles: return False
            seen_urls.add(url); seen_titles.add(title); return True
        return [a for a in articles if is_unique(a)]

    async def _enrich(self, extractor: FullTextExtractor, article: RawArticle):
        article.full_text = await extractor.extract(article.link)
        if (not article.title or article.title == "Discovered Article") and article.full_text:
            article.title = article.full_text.split('\n')[0][:100]

    def _map_feed_to_articles(self, feed: Any, source: str) -> List[RawArticle]:
        return [RawArticle(title=e.get("title", "N/A"), link=e.get("link", "N/A"), source=source, summary=e.get("summary", ""), published_at=e.get("published", datetime.now().isoformat())) for e in feed.entries]
