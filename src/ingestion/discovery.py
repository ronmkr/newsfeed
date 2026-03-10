import aiohttp
import asyncio
from bs4 import BeautifulSoup
from typing import List, Set
from src.utils.helpers import get_registered_domain
from src.utils.logger import project_logger as logger
from src.ingestion.fetchers import BOT_HEADERS

class NewsDiscoverySpider:
    """Discovers news links directly from publication homepages."""
    
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def discover_links(self, homepage_url: str) -> List[str]:
        """Scans a homepage for potential news article links."""
        try:
            async with self.session.get(homepage_url, headers=BOT_HEADERS, timeout=15) as response:
                if response.status != 200:
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                domain = get_registered_domain(homepage_url)
                
                links: Set[str] = set()
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    
                    # Convert relative links to absolute
                    if href.startswith('/'):
                        href = f"https://{domain}{href}"
                    
                    # Heuristic: Only pick links that belong to the same domain 
                    # and look like news articles (usually long paths with keywords)
                    if domain in href and len(href.split('/')) > 3:
                        # Basic noise filter (skip categories, tags, social links)
                        noise = ['/category/', '/tag/', '/author/', '/topic/', 'twitter.com', 'facebook.com']
                        if not any(n in href for n in noise):
                            links.add(href)
                
                logger.info(f"Spider found {len(links)} potential links on {homepage_url}")
                return list(links)[:15] # Limit to top 15 per site to avoid bloat
        except Exception as e:
            logger.error(f"Spider failed for {homepage_url}: {str(e)}")
            return []
