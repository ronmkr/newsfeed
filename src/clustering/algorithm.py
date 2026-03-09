from typing import List, Dict, Any, DefaultDict
from collections import defaultdict
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
from src.agents.state import Article, NewsCluster
from src.utils.logger import project_logger as logger

class SemanticClusterer:
    """Executes mathematical grouping of articles based on vector proximity."""
    
    def __init__(self, similarity_threshold: float = 0.82):
        """
        Args:
            similarity_threshold: Cosine similarity score (0-1) above which 
                                articles are considered the same story.
        """
        self.similarity_threshold = similarity_threshold

    def cluster(self, raw_articles: List[Dict[str, Any]], vectors: np.ndarray) -> List[NewsCluster]:
        """
        Performs distance-based agglomerative clustering.
        
        Args:
            raw_articles: List of raw article metadata.
            vectors: Precomputed embeddings for the articles.
        Returns:
            List of NewsCluster objects containing grouped articles.
        """
        if not raw_articles or vectors.size == 0:
            return []

        # Convert similarity to distance (1.0 similarity = 0.0 distance)
        distance_matrix = 1 - cosine_similarity(vectors)
        
        # Link articles that fall within the distance threshold
        model = AgglomerativeClustering(
            n_clusters=None, 
            distance_threshold=1 - self.similarity_threshold,
            metric="precomputed",
            linkage="average"
        )
        labels = model.fit_predict(distance_matrix)
        
        # Group indices by cluster label
        clusters_map: DefaultDict[int, List[Article]] = defaultdict(list)
        for idx, label in enumerate(labels):
            data = raw_articles[idx]
            clusters_map[label].append(Article(
                title=data.get("title", "Untitled"),
                link=data.get("link", ""),
                source=data.get("source", "unknown"),
                summary=data.get("summary", ""),
                full_text=data.get("full_text"),
                published_at=data.get("published_at", "")
            ))

        # Convert map to final cluster objects
        final_clusters = [
            NewsCluster(
                cluster_id=f"cluster_{label}",
                main_event=articles[0].title, # Use first article as lead
                articles=articles
            ) for label, articles in clusters_map.items()
        ]

        logger.success(f"Algorithm generated {len(final_clusters)} story threads.")
        return final_clusters
