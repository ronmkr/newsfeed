from typing import List, Dict, Any
from langchain_community.embeddings import HuggingFaceEmbeddings
import numpy as np
from src.config.settings import settings
from src.utils.logger import project_logger as logger

class EmbeddingService:
    """Handles the generation of cross-lingual vector embeddings."""
    
    def __init__(self):
        # Using multilingual-e5-small for efficient local cross-lingual performance
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL_NAME,
            encode_kwargs={'normalize_embeddings': True}
        )

    def generate_embeddings(self, raw_articles: List[Dict[str, Any]]) -> np.ndarray:
        """Generates a numpy array of vectors for the given articles."""
        if not raw_articles:
            return np.array([])

        # Multilingual-E5 requires "passage: " prefix for indexing/clustering
        texts = [f"passage: {a['title']} {a['summary']}" for a in raw_articles]
        
        logger.info(f"Generating cross-lingual embeddings for {len(texts)} articles using {settings.EMBEDDING_MODEL_NAME}...")
        vectors = self.embeddings.embed_documents(texts)
        return np.array(vectors)
