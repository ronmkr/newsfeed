import yaml
import os
from typing import List
from src.utils.logger import project_logger as logger

def load_feeds() -> List[str]:
    """Loads and flattens RSS feeds from the central YAML config path."""
    config_path = os.getenv("CONFIG_PATH", "config.yaml")
    if not os.path.exists(config_path):
        logger.error(f"Config file not found at {config_path}")
        return []

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            # Combine both verified and unverified sections
            feeds_data = config.get("feeds", {})
            verified_data = config.get("verified_feeds", {})
            
            # Extract all URLs from all categories in both sections
            all_urls = []
            for data in [feeds_data, verified_data]:
                if data:
                    for category_urls in data.values():
                        all_urls.extend(category_urls)
            
            logger.info(f"Loaded {len(all_urls)} RSS feeds (including verified) from YAML.")
            return all_urls
    except Exception as e:
        logger.error(f"Failed to load feeds from YAML: {str(e)}")
        return []
