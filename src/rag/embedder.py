"""
Embedding Generation Module

This module provides abstract and concrete implementations for generating
text embeddings, with primary support for Gemini embeddings and mock
embeddings for testing.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
import numpy as np


class Embedder(ABC):
    """Abstract base class for text embedding generation."""
    
    @abstractmethod
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text to embed
            
        Returns:
            Embedding vector as numpy array
        """
        pass
    
    @abstractmethod
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a batch of texts.
        
        Args:
            texts: List of input texts
            
        Returns:
            2D numpy array of embeddings (n_texts, embedding_dim)
        """
        pass
    
    @property
    @abstractmethod
    def embedding_dim(self) -> int:
        """Return the dimensionality of embeddings."""
        pass


class GeminiEmbedder(Embedder):
    """
    Embedder using Google's Gemini API.
    
    This embedder generates high-quality text embeddings using the
    Gemini embedding models.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "models/embedding-001"
    ):
        """
        Initialize Gemini embedder.
        
        Args:
            api_key: Gemini API key (or from environment)
            model: Gemini embedding model name
        """
        self.api_key = api_key
        self.model = model
        # Implementation will be added in Phase 3
        raise NotImplementedError("Will be implemented in Phase 3")
    
    def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for single text."""
        raise NotImplementedError("Will be implemented in Phase 3")
    
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for batch of texts."""
        raise NotImplementedError("Will be implemented in Phase 3")
    
    @property
    def embedding_dim(self) -> int:
        """Return embedding dimension."""
        raise NotImplementedError("Will be implemented in Phase 3")


class MockEmbedder(Embedder):
    """
    Mock embedder for testing.
    
    Generates deterministic random embeddings without external API calls.
    Useful for testing and development without API keys.
    """
    
    def __init__(self, dimension: int = 768, seed: int = 42):
        """
        Initialize mock embedder.
        
        Args:
            dimension: Embedding dimension
            seed: Random seed for reproducibility
        """
        self.dimension = dimension
        self.seed = seed
        self._rng = np.random.RandomState(seed)
    
    def embed_text(self, text: str) -> np.ndarray:
        """Generate mock embedding for single text."""
        # Use hash of text for deterministic generation
        text_hash = hash(text) % (2**32)
        rng = np.random.RandomState(text_hash)
        embedding = rng.randn(self.dimension)
        # Normalize to unit vector
        return embedding / np.linalg.norm(embedding)
    
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Generate mock embeddings for batch of texts."""
        return np.array([self.embed_text(text) for text in texts])
    
    @property
    def embedding_dim(self) -> int:
        """Return embedding dimension."""
        return self.dimension
