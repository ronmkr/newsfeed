import os
import yaml
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

def load_yaml_config():
    """Loads configuration from YAML file path specified in ENV or default."""
    path = os.getenv("CONFIG_PATH", "config.yaml")
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except Exception:
        return {}

yaml_data = load_yaml_config()
project_cfg = yaml_data.get("project", {})
models_cfg = yaml_data.get("models", {})
agents_cfg = yaml_data.get("agents", {})

class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = project_cfg.get("name", "Unbiased India News")
    DEBUG: bool = project_cfg.get("debug", False)
    
    # Storage
    RAW_DATA_PATH: str = project_cfg.get("storage", {}).get("raw_data_path", "data/raw")
    LOG_PATH: str = project_cfg.get("storage", {}).get("log_path", "logs/pipeline.log")
    DATABASE_URL: str = project_cfg.get("storage", {}).get("database_url", "sqlite:///data/newsfeed.db")
    CHECKPOINTS_PATH: str = project_cfg.get("storage", {}).get("checkpoints_path", "data/checkpoints/agent_checkpoints.db")
    
    # Models
    MODEL_HEAVY: str = models_cfg.get("heavy", "gemini-1.5-pro")
    MODEL_LIGHT: str = models_cfg.get("light", "gemini-1.5-flash")
    EMBEDDING_MODEL_NAME: str = models_cfg.get("embedding", "intfloat/multilingual-e5-small")
    
    # Agents
    MAX_LOOPS: int = agents_cfg.get("max_loops", 3)
    CONCURRENCY_LIMIT: int = agents_cfg.get("concurrency_limit", 3)
    
    # Credentials
    GOOGLE_API_KEY: Optional[str] = None
    HF_TOKEN: Optional[str] = None
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
