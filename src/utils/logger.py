import sys
from loguru import logger
from src.config.settings import settings

def setup_logger():
    """Configures loguru to log to both terminal and a file."""
    logger.remove() # Remove default logger

    # Standard output logger
    logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>", level="INFO")

    # Persistent log file
    logger.add(settings.LOG_PATH, rotation="10 MB", retention="10 days", level="DEBUG")

    return logger

# Initialize once for project-wide use
project_logger = setup_logger()
