from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.config.settings import settings
from src.storage.models import Base
from src.utils.logger import project_logger as logger

class DatabaseConnection:
    """Manages the SQLAlchemy lifecycle and session pool."""
    
    def __init__(self):
        """Initializes the engine and ensures tables exist."""
        try:
            self.engine = create_engine(
                settings.DATABASE_URL, 
                connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
            )
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            logger.info("Database connection established and schema verified.")
        except Exception as e:
            logger.critical(f"Database Initialization Failed: {e}")
            raise e

    def get_session(self) -> Session:
        """
        Creates a new SQLAlchemy session.
        Note: Use as a context manager.
        """
        return self.Session()
