from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.settings import settings
from src.storage.models import Base, ClusterDB, ArticleDB
from src.agents.state import NewsCluster
from src.utils.logger import project_logger as logger

class DatabaseManager:
    """Handles persistence of analyzed clusters and articles."""
    
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        logger.info(f"Database initialized at {settings.DATABASE_URL}")

    def save_clusters(self, clusters: List[NewsCluster]):
        """Saves NewsCluster objects (and their articles) to the database."""
        if not clusters:
            return

        with self.Session() as session:
            try:
                for cluster in clusters:
                    # Map Pydantic -> SQLAlchemy
                    db_cluster = ClusterDB(
                        cluster_id=cluster.cluster_id,
                        main_event=cluster.main_event,
                        summary_3_bullets=cluster.summary_3_bullets,
                        overall_bias=cluster.overall_bias,
                        is_blindspot=cluster.is_blindspot
                    )
                    
                    # Map Articles
                    db_articles = []
                    for art in cluster.articles:
                        db_art = ArticleDB(
                            title=art.title,
                            link=art.link,
                            source=art.source,
                            summary=art.summary,
                            published_at=art.published_at,
                            bias_score=art.bias_score
                        )
                        db_articles.append(db_art)
                    
                    db_cluster.articles = db_articles
                    session.add(db_cluster)
                
                session.commit()
                logger.success(f"Successfully saved {len(clusters)} clusters to database.")
            except Exception as e:
                session.rollback()
                logger.error(f"Failed to save clusters: {str(e)}")
                raise e
