from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    # Project Settings
    PROJECT_NAME: str = "Unbiased India News"
    DEBUG: bool = False
    
    # News Sources (RSS Feeds)
    RSS_FEEDS: List[str] = [
        # English
        "https://www.thehindu.com/news/national/feeder/default.rss",
        "https://www.ndtv.com/feeds/india-news",
        "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
        "https://www.republicworld.com/rss/india-news.xml",
        
        # Hindi
        "https://navbharattimes.indiatimes.com/india/rssfeeds/1554836.cms",
        
        # Marathi
        "https://www.sakal.com/rss/national.xml",
        
        # Tamil
        "https://feeds.feedburner.com/dinamalar/national",
        
        # Bengali
        "https://www.anandabazar.com/rss-feed/india-news-1.2599.xml"
    ]
    
    # Storage Settings
    RAW_DATA_PATH: str = "data/raw"
    LOG_PATH: str = "logs/pipeline.log"
    DATABASE_URL: str = "sqlite:///data/newsfeed.db"
    
    # Embedding Config (Multilingual-e5-small is good for local Mac CPU)
    EMBEDDING_MODEL_NAME: str = "intfloat/multilingual-e5-small"
    
    # LLM & Agentic Config
    MODEL_HEAVY: str = "gemini-1.5-pro"
    MODEL_LIGHT: str = "gemini-1.5-flash"
    OPENAI_API_KEY: Optional[str] = None
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
