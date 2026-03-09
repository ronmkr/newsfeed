from typing import List, Dict, Any
from langchain_community.embeddings import HuggingFaceEmbeddings
import numpy as np
from src.config.settings import settings
from src.utils.logger import project_logger as logger

class EmbeddingService:
    """Manages the generation of semantic vector embeddings for news articles."""
    
    def __init__(self):
        """Initializes the HuggingFace Multilingual-E5 model."""
        logger.info(f"Initializing EmbeddingService with {settings.EMBEDDING_MODEL_NAME}...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL_NAME,
            encode_kwargs={'normalize_embeddings': True}
        )

    def generate_embeddings(self, raw_articles: List[Dict[str, Any]]) -> np.ndarray:
        """
        Converts article metadata into numerical vector representations.
        
        Args:
            raw_articles: List of article dictionaries (title + summary).
        Returns:
            A numpy array of normalized embeddings.
        """
        if not raw_articles:
            return np.array([])

        # Multilingual-E5 requires "passage: " prefix for indexing/clustering
        texts = [
            f"passage: {a.get('title', '')} {a.get('summary', '')}" 
            for a in raw_articles
        ]
        
        try:
            logger.debug(f"Generating embeddings for {len(texts)} articles...")
            vectors = self.embeddings.embed_documents(texts)
            return np.array(vectors)
        except Exception as e:
            logger.error(f"Embedding Generation Failed: {str(e)}")
            return np.array([])
