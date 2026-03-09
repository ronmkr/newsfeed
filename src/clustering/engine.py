from typing import List, Dict, Any
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
from langchain_community.embeddings import HuggingFaceEmbeddings

from src.config.settings import settings
from src.utils.logger import project_logger as logger
from src.agents.state import Article, NewsCluster

class ClusteringEngine:
    """Uses cross-lingual vector embeddings to group articles into story clusters."""
    
    def __init__(self, similarity_threshold: float = 0.82):
        # Using multilingual-e5-small for efficient local cross-lingual performance
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL_NAME,
            encode_kwargs={'normalize_embeddings': True}
        )
        self.similarity_threshold = similarity_threshold

    def group_articles(self, raw_articles: List[Dict[str, Any]]) -> List[NewsCluster]:
        """Performs semantic clustering on raw articles across multiple languages."""
        if not raw_articles:
            return []

        # Multilingual-E5 requires "passage: " prefix for indexing/clustering
        texts = [f"passage: {a['title']} {a['summary']}" for a in raw_articles]
        
        logger.info(f"Generating cross-lingual embeddings for {len(texts)} articles using {settings.EMBEDDING_MODEL_NAME}...")
        vectors = self.embeddings.embed_documents(texts)
        X = np.array(vectors)

        # Distance-based clustering (1 - similarity)
        # We'll use Agglomerative Clustering with a precomputed distance matrix
        distance_matrix = 1 - cosine_similarity(X)
        
        # Link articles based on the similarity threshold
        clustering_model = AgglomerativeClustering(
            n_clusters=None, 
            distance_threshold=1 - self.similarity_threshold,
            metric="precomputed",
            linkage="average"
        )
        labels = clustering_model.fit_predict(distance_matrix)
        
        # Organize into NewsCluster objects
        clusters_dict = {}
        for idx, label in enumerate(labels):
            if label not in clusters_dict:
                clusters_dict[label] = []
            
            # Convert dict -> Article model
            article_data = raw_articles[idx]
            article = Article(
                title=article_data["title"],
                link=article_data["link"],
                source=article_data["source"],
                summary=article_data["summary"],
                published_at=article_data["published_at"]
            )
            clusters_dict[label].append(article)

        final_clusters = []
        for label, articles in clusters_dict.items():
            # Determine "Main Event" (for now, use the title of the first article)
            main_event = articles[0].title
            final_clusters.append(NewsCluster(
                cluster_id=f"cluster_{label}",
                main_event=main_event,
                articles=articles
            ))

        logger.success(f"Formed {len(final_clusters)} clusters from {len(raw_articles)} articles.")
        return final_clusters
