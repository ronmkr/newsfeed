import asyncio
import aiohttp
from typing import List, Dict, Tuple
from src.utils.logger import project_logger as logger
from src.ingestion.fetchers import AsyncRSSFetcher

class FeedVerifier:
    """Utility to test and categorize news feeds by their health status."""
    
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}

    async def verify_list(self, urls: List[str]) -> Tuple[List[str], List[str]]:
        """
        Tests a list of URLs and returns (working_urls, broken_urls).
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            fetcher = AsyncRSSFetcher(session)
            tasks = [fetcher.fetch(url) for url in urls]
            
            logger.info(f"Verifying {len(urls)} feeds...")
            results = await asyncio.gather(*tasks)
            
            working = []
            broken = []
            
            for url, result in zip(urls, results):
                if result:
                    working.append(url)
                else:
                    broken.append(url)
                    
            return working, broken
