"""
Dataset Loader

Handles loading documents from various sources (directory, JSON files, etc.)
and converting them into the standard Document format.
"""

import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
import logging

from .schema import Document, Metadata, validate_document

logger = logging.getLogger(__name__)


class DatasetLoader:
    """
    Loads documents from various sources and validates them.
    
    Supports loading from:
    - Directory of markdown files
    - JSON files containing document arrays
    - Individual files
    """
    
    def __init__(self, default_metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize the dataset loader.
        
        Args:
            default_metadata: Default metadata to apply to documents that don't have it
        """
        self.default_metadata = default_metadata or {}
        self._loaded_documents: List[Document] = []
    
    def load_from_directory(
        self, 
        directory: str, 
        extensions: Optional[List[str]] = None,
        recursive: bool = False
    ) -> List[Document]:
        """
        Load all documents from a directory.
        
        Args:
            directory: Path to directory containing documents
            extensions: List of file extensions to load (default: ['.md', '.txt'])
            recursive: Whether to search subdirectories
            
        Returns:
            List of loaded Document objects
            
        Raises:
            FileNotFoundError: If directory doesn't exist
            ValueError: If no valid documents found
        """
        dir_path = Path(directory)
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        if not dir_path.is_dir():
            raise ValueError(f"Path is not a directory: {directory}")
        
        if extensions is None:
            extensions = ['.md', '.txt']
        
        documents = []
        pattern = "**/*" if recursive else "*"
        
        for ext in extensions:
            for file_path in dir_path.glob(f"{pattern}{ext}"):
                if file_path.is_file():
                    try:
                        doc = self._load_single_file(file_path)
                        documents.append(doc)
                        logger.info(f"Loaded document from {file_path}")
                    except Exception as e:
                        logger.error(f"Failed to load {file_path}: {e}")
                        continue
        
        if not documents:
            raise ValueError(f"No valid documents found in {directory}")
        
        self._loaded_documents.extend(documents)
        logger.info(f"Loaded {len(documents)} documents from {directory}")
        return documents
    
    def load_from_json(self, json_path: str) -> List[Document]:
        """
        Load documents from a JSON file.
        
        Expected JSON format:
        [
            {
                "id": "optional-id",
                "content": "document text...",
                "metadata": {
                    "title": "Document Title",
                    "tags": ["tag1", "tag2"],
                    "doc_type": "theory"
                },
                "source": "optional-source"
            },
            ...
        ]
        
        Args:
            json_path: Path to JSON file
            
        Returns:
            List of loaded Document objects
            
        Raises:
            FileNotFoundError: If JSON file doesn't exist
            ValueError: If JSON is invalid or documents fail validation
        """
        json_file = Path(json_path)
        if not json_file.exists():
            raise FileNotFoundError(f"JSON file not found: {json_path}")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {json_path}: {e}")
        
        if not isinstance(data, list):
            raise ValueError("JSON must contain an array of documents")
        
        documents = []
        for i, doc_data in enumerate(data):
            try:
                doc = Document.from_dict(doc_data)
                is_valid, error = validate_document(doc)
                if not is_valid:
                    logger.warning(f"Document {i} validation failed: {error}")
                    continue
                documents.append(doc)
            except Exception as e:
                logger.error(f"Failed to parse document {i}: {e}")
                continue
        
        if not documents:
            raise ValueError(f"No valid documents found in {json_path}")
        
        self._loaded_documents.extend(documents)
        logger.info(f"Loaded {len(documents)} documents from {json_path}")
        return documents
    
    def load_single_document(self, file_path: str, metadata: Optional[Dict[str, Any]] = None) -> Document:
        """
        Load a single document from a file.
        
        Args:
            file_path: Path to the document file
            metadata: Optional metadata to override/supplement
            
        Returns:
            Loaded Document object
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If document validation fails
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        doc = self._load_single_file(path, metadata)
        self._loaded_documents.append(doc)
        return doc
    
    def validate_documents(self, documents: List[Document]) -> tuple[List[Document], List[tuple[Document, str]]]:
        """
        Validate a list of documents.
        
        Args:
            documents: List of documents to validate
            
        Returns:
            Tuple of (valid_documents, invalid_documents_with_errors)
        """
        valid = []
        invalid = []
        
        for doc in documents:
            is_valid, error = validate_document(doc)
            if is_valid:
                valid.append(doc)
            else:
                invalid.append((doc, error))
                logger.warning(f"Document {doc.id} validation failed: {error}")
        
        return valid, invalid
    
    def get_loaded_documents(self) -> List[Document]:
        """
        Get all documents loaded by this loader instance.
        
        Returns:
            List of all loaded documents
        """
        return self._loaded_documents.copy()
    
    def clear_cache(self):
        """Clear the internal cache of loaded documents."""
        self._loaded_documents.clear()
    
    def _load_single_file(
        self, 
        file_path: Path, 
        metadata_override: Optional[Dict[str, Any]] = None
    ) -> Document:
        """
        Internal method to load a single file.
        
        Args:
            file_path: Path object pointing to the file
            metadata_override: Optional metadata to override defaults
            
        Returns:
            Document object
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract metadata from file if present (simple frontmatter-style)
        metadata_dict = self.default_metadata.copy()
        
        # Check for YAML-style frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                # Parse simple key: value pairs from frontmatter
                frontmatter = parts[1].strip()
                content = parts[2].strip()
                
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        
                        # Handle tags specially
                        if key == 'tags' and value.startswith('['):
                            value = [t.strip().strip('"').strip("'") for t in value.strip('[]').split(',')]
                        
                        metadata_dict[key] = value
        
        # Apply overrides
        if metadata_override:
            metadata_dict.update(metadata_override)
        
        # Ensure title is set
        if 'title' not in metadata_dict:
            metadata_dict['title'] = file_path.stem
        
        # Set source if not provided
        if 'source' not in metadata_dict:
            metadata_dict['source'] = str(file_path)
        
        metadata = Metadata.from_dict(metadata_dict)
        
        # Create document
        doc = Document(
            id=metadata_dict.get('id', ''),  # Will generate UUID if empty
            content=content,
            metadata=metadata,
            source=str(file_path)
        )
        
        return doc
    
    def export_to_json(self, documents: List[Document], output_path: str):
        """
        Export documents to a JSON file.
        
        Args:
            documents: List of documents to export
            output_path: Path where JSON should be written
        """
        data = [doc.to_dict() for doc in documents]
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {len(documents)} documents to {output_path}")
