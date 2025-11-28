"""
RAG Package

This package contains all components for the RAG (Retrieval-Augmented Generation)
pipeline including chunking, embedding, vector storage, retrieval, and generation.
"""

__version__ = "0.1.0"

# Core data models
from src.rag.models import (
    Chunk,
    ChunkMetadata,
    ChunkType,
    generate_chunk_id,
    validate_chunk,
)

# Dataset components
from src.rag.dataset.schema import (
    Document,
    Metadata,
    validate_document,
    validate_metadata,
)
from src.rag.dataset.loader import DatasetLoader

# Chunking components
from src.rag.chunker import (
    PhysicsAwareChunker,
    PHYSICS_TERMS,
)

__all__ = [
    # Version
    "__version__",
    # Models
    "Chunk",
    "ChunkMetadata",
    "ChunkType",
    "generate_chunk_id",
    "validate_chunk",
    # Dataset
    "Document",
    "Metadata",
    "validate_document",
    "validate_metadata",
    "DatasetLoader",
    # Chunking
    "PhysicsAwareChunker",
    "PHYSICS_TERMS",
]
