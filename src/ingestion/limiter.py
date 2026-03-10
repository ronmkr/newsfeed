import asyncio
from typing import Dict
from src.utils.logger import project_logger as logger

class PerDomainRateLimiter:
    """Ensures we don't overwhelm a single domain with too many concurrent requests."""
    
    def __init__(self, connections_per_domain: int = 2):
        self.limit = connections_per_domain
        self.semaphores: Dict[str, asyncio.Semaphore] = {}

    def get_semaphore(self, domain: str) -> asyncio.Semaphore:
        """Returns or creates a semaphore for a specific domain."""
        if domain not in self.semaphores:
            self.semaphores[domain] = asyncio.Semaphore(self.limit)
        return self.semaphores[domain]

    async def throttle(self, domain: str):
        """Standard throttle point for any domain-specific I/O."""
        sem = self.get_semaphore(domain)
        async with sem:
            # Add a small polite delay between requests to the same domain
            await asyncio.sleep(1.0)
            yield
