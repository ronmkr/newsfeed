import aiohttp
import asyncio
import xml.etree.ElementTree as ET
from typing import List, Set
from src.utils.logger import project_logger as logger

class SitemapDiscoveryEngine:
    """Discovers news links by parsing publisher sitemaps."""
    
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.headers = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}

    async def get_links_from_sitemap(self, sitemap_url: str) -> List[str]:
        """Parses a news sitemap XML and extracts article URLs."""
        try:
            async with self.session.get(sitemap_url, headers=self.headers, timeout=20) as response:
                if response.status != 200:
                    return []
                
                content = await response.read()
                root = ET.fromstring(content)
                
                # Sitemaps use namespaces, we need to handle them
                # Usually {http://www.sitemaps.org/schemas/sitemap/0.9}loc
                links = []
                for url_tag in root.findall('.//{*}loc'):
                    url = url_tag.text
                    if url and self._is_likely_news(url):
                        links.append(url)
                
                logger.info(f"Sitemap Engine discovered {len(links)} links from {sitemap_url}")
                return links[:20] # Limit per source
        except Exception as e:
            logger.error(f"Sitemap parsing failed for {sitemap_url}: {str(e)}")
            return []

    def _is_likely_news(self, url: str) -> bool:
        """Heuristic to ensure the link is an article and not a static page."""
        # Most news URLs have dates or long slugs
        return any(char.isdigit() for char in url) and len(url.split('/')) > 3
