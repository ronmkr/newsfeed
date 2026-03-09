from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.settings import settings
from src.storage.models import Base
from src.utils.logger import project_logger as logger

class DatabaseConnection:
    """Manages the database connection and session creation."""
    
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        logger.info(f"Database initialized at {settings.DATABASE_URL}")

    def get_session(self):
        """Returns a new database session."""
        return self.Session()
