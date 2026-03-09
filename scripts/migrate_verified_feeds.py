import asyncio
import yaml
import os
from src.ingestion.verifier import FeedVerifier
from src.utils.logger import project_logger as logger

async def migrate_feeds():
    """
    Reads config.yaml, tests all feeds, and moves working ones to verified_feeds.
    """
    config_path = "config.yaml"
    if not os.path.exists(config_path):
        logger.error(f"Config not found at {config_path}")
        return

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    original_feeds = config.get("feeds", {})
    verified_section = config.get("verified_feeds", {})
    
    verifier = FeedVerifier()
    
    # Flatten all categories from the 'feeds' (candidate) section
    all_candidate_urls = []
    category_map = {} # To remember which category a URL belongs to
    
    for category, urls in original_feeds.items():
        all_candidate_urls.extend(urls)
        for url in urls:
            category_map[url] = category

    if not all_candidate_urls:
        logger.info("No candidate feeds found to verify.")
        return

    # 1. Test the feeds
    working, broken = await verifier.verify_list(all_candidate_urls)
    
    # 2. Update config structure
    # Initialize categories in verified_section if they don't exist
    for category in original_feeds.keys():
        if category not in verified_section:
            verified_section[category] = []

    # Move working ones
    for url in working:
        category = category_map[url]
        if url not in verified_section[category]:
            verified_section[category].append(url)
        # Remove from original
        if url in original_feeds[category]:
            original_feeds[category].remove(url)

    # 3. Save back to YAML
    config["feeds"] = original_feeds
    config["verified_feeds"] = verified_section
    
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    logger.success(f"Migration complete! {len(working)} moved to verified_feeds. {len(broken)} remain in feeds (broken/pending).")

if __name__ == "__main__":
    asyncio.run(migrate_feeds())
