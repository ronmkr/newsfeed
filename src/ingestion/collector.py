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

class IngestionCoordinator:
    """Orchestrates triple-track ingestion with ethical compliance (robots.txt)."""
    
    def __init__(self):
        self.robots_cache = {}
        self.discovery_sites = [
            "https://theprint.in", 
            "https://thewire.in", 
            "https://scroll.in", 
            "https://www.thequint.com"
        ]
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
                rp.read() # Sync read but cached for the batch run
                self.robots_cache[domain] = rp
            except Exception:
                return True # Assume allowed if robots.txt unreachable
        
        return self.robots_cache[domain].can_fetch("*", url)

    async def fetch_all(self, rss_feeds: List[str]) -> List[RawArticle]:
        """Triple-track ingestion with parallel execution and compliance filtering."""
        
        # 1. Filter discovery and sitemaps by robots.txt
        allowed_discovery = [url for url in self.discovery_sites if self._is_allowed(url)]
        allowed_sitemaps = [url for url in self.sitemap_urls if self._is_allowed(url)]

        async with aiohttp.ClientSession() as session:
            rss_fetcher = AsyncRSSFetcher(session)
            sitemap_engine = SitemapDiscoveryEngine(session)
            spider = NewsDiscoverySpider(session)
            extractor = FullTextExtractor(session)

            logger.info(f"Ingesting from {len(rss_feeds)} RSS, {len(allowed_sitemaps)} Sitemaps, {len(allowed_discovery)} Spiders.")
            
            results = await run_parallel([
                run_parallel([rss_fetcher.fetch(url) for url in rss_feeds]),
                run_parallel([sitemap_engine.get_links_from_sitemap(url) for url in allowed_sitemaps]),
                run_parallel([spider.discover_links(url) for url in allowed_discovery])
            ])
            
            rss_results, sitemap_links, spider_links = results

            all_raw = []
            # Process RSS
            for url, feed in zip(rss_feeds, rss_results):
                if feed: 
                    all_raw.extend(self._map_feed_to_articles(feed, get_registered_domain(url) or "unknown"))
            
            # Process Discovered (Combine Sitemaps + Spiders)
            discovered = [link for sublist in (sitemap_links + spider_links) for link in sublist]
            all_raw.extend([
                RawArticle(
                    title="Discovered Article", 
                    link=l, 
                    source=get_registered_domain(l) or "unknown", 
                    summary="", 
                    published_at=datetime.now().isoformat()
                ) for l in discovered
            ])

            # 2. Deduplicate
            unique = self.deduplicate(all_raw)
            
            # 3. Parallel Enrichment with Concurrency Limit
            sem = asyncio.Semaphore(15)
            async def bounded_enrich(article):
                async with sem:
                    await self._enrich(extractor, article)
                    
            await run_parallel([bounded_enrich(a) for a in unique])
            
        final = [a for a in unique if a.full_text]
        logger.success(f"Ingestion complete: {len(final)} unique articles enriched.")
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
        return [
            RawArticle(
                title=e.get("title", "N/A"), 
                link=e.get("link", "N/A"), 
                source=source, 
                summary=e.get("summary", ""), 
                published_at=e.get("published", datetime.now().isoformat())
            ) for e in feed.entries
        ]
