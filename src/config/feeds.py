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
            feeds_data = config.get("feeds", {})
            
            # Flatten categories
            all_feeds = [url for category in feeds_data.values() for url in category]
            logger.info(f"Loaded {len(all_feeds)} RSS feeds from YAML.")
            return all_feeds
    except Exception as e:
        logger.error(f"Failed to load feeds from YAML: {str(e)}")
        return []
