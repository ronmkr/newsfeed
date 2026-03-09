from typing import List, Dict, Any
from src.agents.state import NewsCluster
from src.clustering.embeddings import EmbeddingService
from src.clustering.algorithm import SemanticClusterer

class ClusteringEngine:
    """Orchestrates embedding generation and semantic clustering."""
    
    def __init__(self, similarity_threshold: float = 0.82):
        self.embedding_service = EmbeddingService()
        self.clusterer = SemanticClusterer(similarity_threshold=similarity_threshold)

    def group_articles(self, raw_articles: List[Dict[str, Any]]) -> List[NewsCluster]:
        """Coordinates semantic clustering on raw articles across multiple languages."""
        if not raw_articles:
            return []

        # 1. Generate Vectors
        vectors = self.embedding_service.generate_embeddings(raw_articles)
        
        # 2. Cluster using vectors
        clusters = self.clusterer.cluster(raw_articles, vectors)
        
        return clusters

