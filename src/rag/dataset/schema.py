"""
Dataset Schema Definition

Defines the data structures for documents and metadata in the Higgs-Helper system.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid


@dataclass
class Metadata:
    """
    Metadata associated with a document.
    
    Attributes:
        title: Document title
        section: Section within larger document (optional)
        tags: List of descriptive tags
        doc_type: Type of document ('theory', 'tutorial', 'reference', 'code')
        created_at: Timestamp of document creation
        author: Document author (optional)
        source: Source URL or file path (optional)
        language: Primary language (default: 'en')
    """
    
    title: str
    section: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    doc_type: str = "general"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    author: Optional[str] = None
    source: Optional[str] = None
    language: str = "en"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        return {
            "title": self.title,
            "section": self.section,
            "tags": self.tags,
            "doc_type": self.doc_type,
            "created_at": self.created_at,
            "author": self.author,
            "source": self.source,
            "language": self.language
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Metadata":
        """Create Metadata from dictionary."""
        return cls(
            title=data.get("title", "Untitled"),
            section=data.get("section"),
            tags=data.get("tags", []),
            doc_type=data.get("doc_type", "general"),
            created_at=data.get("created_at", datetime.utcnow().isoformat()),
            author=data.get("author"),
            source=data.get("source"),
            language=data.get("language", "en")
        )


@dataclass
class Document:
    """
    Represents a document in the corpus.
    
    Attributes:
        id: Unique document identifier
        content: Full text content of the document
        metadata: Associated metadata
        source: Original file path or source identifier
    """
    
    id: str
    content: str
    metadata: Metadata
    source: str
    
    def __post_init__(self):
        """Validate document after initialization."""
        if not self.id:
            self.id = str(uuid.uuid4())
        
        if not self.content:
            raise ValueError("Document content cannot be empty")
        
        if not isinstance(self.metadata, Metadata):
            raise TypeError("metadata must be a Metadata instance")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert document to dictionary."""
        return {
            "id": self.id,
            "content": self.content,
            "metadata": self.metadata.to_dict(),
            "source": self.source
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Document":
        """Create Document from dictionary."""
        metadata = Metadata.from_dict(data.get("metadata", {}))
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            content=data["content"],
            metadata=metadata,
            source=data.get("source", "unknown")
        )
    
    def __len__(self) -> int:
        """Return length of document content."""
        return len(self.content)
    
    def __repr__(self) -> str:
        """String representation of document."""
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"Document(id='{self.id[:8]}...', title='{self.metadata.title}', len={len(self.content)})"


def validate_document(doc: Document) -> tuple[bool, Optional[str]]:
    """
    Validate a document for required fields and content.
    
    Args:
        doc: Document to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(doc, Document):
        return False, "Not a Document instance"
    
    if not doc.id:
        return False, "Document ID is required"
    
    if not doc.content or not doc.content.strip():
        return False, "Document content is empty"
    
    if len(doc.content) < 10:
        return False, "Document content is too short (minimum 10 characters)"
    
    if not doc.metadata.title:
        return False, "Document title is required in metadata"
    
    # Check for valid document type
    valid_types = ["theory", "tutorial", "reference", "code", "general", "detector"]
    if doc.metadata.doc_type not in valid_types:
        return False, f"Invalid doc_type: {doc.metadata.doc_type}. Must be one of {valid_types}"
    
    return True, None


def validate_metadata(metadata: Metadata) -> tuple[bool, Optional[str]]:
    """
    Validate metadata for required fields.
    
    Args:
        metadata: Metadata to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(metadata, Metadata):
        return False, "Not a Metadata instance"
    
    if not metadata.title or not metadata.title.strip():
        return False, "Title is required"
    
    if not isinstance(metadata.tags, list):
        return False, "Tags must be a list"
    
    return True, None
