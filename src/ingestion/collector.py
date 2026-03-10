import asyncio
import aiohttp
import feedparser
from datetime import datetime
from typing import List, Any, Optional
from urllib.robotparser import RobotFileParser

from src.utils.logger import project_logger as logger
from src.ingestion.models import RawArticle
from src.utils.helpers import clean_text, get_registered_domain, run_parallel
from src.ingestion.discovery import NewsDiscoverySpider
from src.ingestion.sitemaps import SitemapDiscoveryEngine
from src.ingestion.fetchers import FullTextExtractor, AsyncRSSFetcher
from src.ingestion.limiter import PerDomainRateLimiter

class IngestionCoordinator:
    """Orchestrates triple-track ingestion with ethical compliance and rate limiting."""
    
    def __init__(self):
        self.robots_cache = {}
        self.limiter = PerDomainRateLimiter(connections_per_domain=2)
        self.discovery_sites = ["https://theprint.in", "https://thewire.in", "https://scroll.in", "https://www.thequint.com"]
        self.sitemap_urls = [
            "https://www.thehindu.com/sitemap/googlenews.xml",
            "https://indianexpress.com/news-sitemap.xml",
            "https://thewire.in/sitemap.xml",
            "https://theprint.in/news-sitemap.xml",
            "https://www.ndtv.com/sitemaps/india-news.xml"
        ]

    def _is_allowed(self, url: str) -> bool:
        """Checks robots.txt to ensure ethical scraping compliance."""
        domain = get_registered_domain(url)
        if not domain: return True
        if domain not in self.robots_cache:
            try:
                rp = RobotFileParser()
                rp.set_url(f"https://{domain}/robots.txt")
                rp.read()
                self.robots_cache[domain] = rp
            except Exception:
                return True
        return self.robots_cache[domain].can_fetch("*", url)

    async def fetch_all(self, rss_feeds: List[str]) -> List[RawArticle]:
        allowed_discovery = [url for url in self.discovery_sites if self._is_allowed(url)]
        allowed_sitemaps = [url for url in self.sitemap_urls if self._is_allowed(url)]

        async with aiohttp.ClientSession() as session:
            rss_fetcher = AsyncRSSFetcher(session)
            sitemap_engine = SitemapDiscoveryEngine(session)
            spider = NewsDiscoverySpider(session)
            extractor = FullTextExtractor(session)

            logger.info("Gathering news across triple-tracks...")
            results = await run_parallel([
                run_parallel([rss_fetcher.fetch(url) for url in rss_feeds]),
                run_parallel([sitemap_engine.get_links_from_sitemap(url) for url in allowed_sitemaps]),
                run_parallel([spider.discover_links(url) for url in allowed_discovery])
            ])
            
            rss_res, sitemap_links, spider_links = results
            all_raw = []
            for url, feed in zip(rss_feeds, rss_res):
                if feed: all_raw.extend(self._map_feed_to_articles(feed, get_registered_domain(url) or "unknown"))
            
            discovered = [link for sublist in (sitemap_links + spider_links) for link in sublist]
            all_raw.extend([RawArticle(title="Discovered Article", link=l, source=get_registered_domain(l) or "unknown", summary="", published_at=datetime.now().isoformat()) for l in discovered])

            unique = self.deduplicate(all_raw)
            
            # Enrich with per-domain rate limiting
            await run_parallel([self._enrich(extractor, a) for a in unique])
            
        final = [a for a in unique if a.full_text]
        logger.success(f"Ingestion complete: {len(final)} unique articles enriched.")
        return final

    async def _enrich(self, extractor: FullTextExtractor, article: RawArticle):
        """Fetches full text respecting per-domain rate limits."""
        domain = get_registered_domain(article.link) or "unknown"
        async with self.limiter.get_semaphore(domain):
            # Politeness delay
            await asyncio.sleep(0.5)
            article.full_text = await extractor.extract(article.link)
            
        if (not article.title or article.title == "Discovered Article") and article.full_text:
            article.title = article.full_text.split('\n')[0][:100]

    def deduplicate(self, articles: List[RawArticle]) -> List[RawArticle]:
        seen_urls, seen_titles = set(), set()
        def is_unique(a):
            url, title = a.link.strip().lower(), clean_text(a.title)
            if url in seen_urls or title in seen_titles: return False
            seen_urls.add(url); seen_titles.add(title); return True
        return [a for a in articles if is_unique(a)]

    def _map_feed_to_articles(self, feed: Any, source: str) -> List[RawArticle]:
        return [RawArticle(title=e.get("title", "N/A"), link=e.get("link", "N/A"), source=source, summary=e.get("summary", ""), published_at=e.get("published", datetime.now().isoformat())) for e in feed.entries]
