from typing import List, Dict, Any
from fastembed import TextEmbedding
import numpy as np
from src.utils.logger import project_logger as logger

class EmbeddingService:
    """
    Manages the generation of semantic vector embeddings using FastEmbed (ONNX).
    This is significantly lighter than PyTorch-based implementations.
    """
    
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        """Initializes the FastEmbed model."""
        logger.info(f"Initializing FastEmbed service with {model_name}...")
        self.model = TextEmbedding(model_name=model_name)

    def generate_embeddings(self, raw_articles: List[Dict[str, Any]]) -> np.ndarray:
        """
        Converts article metadata into numerical vector representations.
        """
        if not raw_articles:
            return np.array([])

        texts = [
            f"{a.get('title', '')} {a.get('summary', '')}" 
            for a in raw_articles
        ]
        
        try:
            logger.debug(f"Generating embeddings for {len(texts)} articles...")
            # FastEmbed returns a generator of embeddings
            embeddings_generator = self.model.embed(texts)
            return np.array(list(embeddings_generator))
        except Exception as e:
            logger.error(f"Embedding Generation Failed: {str(e)}")
            return np.array([])
