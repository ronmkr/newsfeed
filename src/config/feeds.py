import json
import os
from typing import List
from src.utils.logger import project_logger as logger

def load_feeds(json_path: str = "data/rss_feeds.json") -> List[str]:
    """Loads and flattens the list of RSS feeds from JSON."""
    if not os.path.exists(json_path):
        logger.error(f"RSS feeds file not found at {json_path}")
        return []

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Flatten all categories into a single list
            all_feeds = []
            for category, urls in data.items():
                all_feeds.extend(urls)
            
            logger.info(f"Loaded {len(all_feeds)} RSS feeds across {len(data)} categories.")
            return all_feeds
    except Exception as e:
        logger.error(f"Failed to load RSS feeds: {str(e)}")
        return []
