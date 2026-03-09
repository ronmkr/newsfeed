from typing import List
from src.storage.connection import DatabaseConnection
from src.storage.models import ClusterDB, ArticleDB
from src.agents.state import NewsCluster
from src.utils.logger import project_logger as logger

class ClusterRepository:
    """Handles the persistence logic for NewsCluster objects."""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def save_clusters(self, clusters: List[NewsCluster]):
        """Maps and saves NewsCluster objects (and their articles) to the database."""
        if not clusters:
            return

        with self.db_connection.get_session() as session:
            try:
                for cluster in clusters:
                    # Map Pydantic -> SQLAlchemy
                    db_cluster = ClusterDB(
                        cluster_id=cluster.cluster_id,
                        main_event=cluster.main_event,
                        summary_3_bullets=cluster.summary_3_bullets,
                        overall_bias=cluster.overall_bias,
                        reasoning_trace=cluster.reasoning_trace, # Added for transparency
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
                            full_text=art.full_text, # Added for deeper analysis
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
