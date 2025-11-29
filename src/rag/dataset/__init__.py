"""
Dataset Package

This package handles document loading, validation, and schema management
for the Higgs-Helper RAG system.
"""

from .schema import Document, Metadata
from .loader import DatasetLoader

__all__ = ["Document", "Metadata", "DatasetLoader"]
