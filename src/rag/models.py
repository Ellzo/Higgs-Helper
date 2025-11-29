"""
RAG Data Models

Defines the core data structures for chunks and their metadata used in
the Higgs-Helper RAG system.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any
import hashlib
import uuid


class ChunkType(Enum):
    """Enumeration of chunk content types."""
    THEORY = "theory"
    CODE = "code"
    EQUATION = "equation"
    CALCULATION = "calculation"
    DETECTOR = "detector"
    ANALYSIS = "analysis"
    TUTORIAL = "tutorial"
    REFERENCE = "reference"
    MIXED = "mixed"
    GENERAL = "general"


@dataclass
class ChunkMetadata:
    """
    Metadata associated with a text chunk.
    
    Attributes:
        source: Original document source path or identifier
        source_id: ID of the source document
        section: Section heading within the source document
        chunk_index: Index of this chunk within the source document
        chunk_type: Type of content ('theory', 'code', 'equation', 'mixed', 'general')
        tags: List of physics-related tags detected in the chunk
        has_latex: Whether the chunk contains LaTeX equations
        has_code: Whether the chunk contains code blocks
        code_language: Programming language of code blocks if present
        start_char: Character offset where this chunk starts in the source
        end_char: Character offset where this chunk ends in the source
        physics_terms: List of physics terms detected in the chunk
        detector_mentions: List of detector names mentioned (ATLAS, CMS, etc.)
        particle_mentions: List of particle names mentioned
    """
    
    source: str
    source_id: str = ""
    section: str = ""
    chunk_index: int = 0
    chunk_type: str = "general"
    tags: List[str] = field(default_factory=list)
    has_latex: bool = False
    has_code: bool = False
    code_language: Optional[str] = None
    start_char: int = 0
    end_char: int = 0
    physics_terms: List[str] = field(default_factory=list)
    detector_mentions: List[str] = field(default_factory=list)
    particle_mentions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        return {
            "source": self.source,
            "source_id": self.source_id,
            "section": self.section,
            "chunk_index": self.chunk_index,
            "chunk_type": self.chunk_type,
            "tags": self.tags,
            "has_latex": self.has_latex,
            "has_code": self.has_code,
            "code_language": self.code_language,
            "start_char": self.start_char,
            "end_char": self.end_char,
            "physics_terms": self.physics_terms,
            "detector_mentions": self.detector_mentions,
            "particle_mentions": self.particle_mentions
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChunkMetadata":
        """Create ChunkMetadata from dictionary."""
        return cls(
            source=data.get("source", ""),
            source_id=data.get("source_id", ""),
            section=data.get("section", ""),
            chunk_index=data.get("chunk_index", 0),
            chunk_type=data.get("chunk_type", "general"),
            tags=data.get("tags", []),
            has_latex=data.get("has_latex", False),
            has_code=data.get("has_code", False),
            code_language=data.get("code_language"),
            start_char=data.get("start_char", 0),
            end_char=data.get("end_char", 0),
            physics_terms=data.get("physics_terms", []),
            detector_mentions=data.get("detector_mentions", []),
            particle_mentions=data.get("particle_mentions", [])
        )


@dataclass
class Chunk:
    """
    Represents a text chunk for the RAG system.
    
    Attributes:
        id: Unique identifier for the chunk
        text: The actual text content of the chunk
        metadata: Associated metadata
        embedding: Optional embedding vector (populated during indexing)
        score: Optional relevance score (populated during retrieval)
    """
    
    id: str
    text: str
    metadata: ChunkMetadata
    embedding: Optional[List[float]] = None
    score: Optional[float] = None
    
    def __post_init__(self):
        """Validate and generate ID if needed."""
        if not self.id:
            self.id = generate_chunk_id(self.text, self.metadata.source)
        
        if not self.text:
            raise ValueError("Chunk text cannot be empty")
        
        if not isinstance(self.metadata, ChunkMetadata):
            raise TypeError("metadata must be a ChunkMetadata instance")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert chunk to dictionary."""
        result = {
            "id": self.id,
            "text": self.text,
            "metadata": self.metadata.to_dict()
        }
        
        if self.embedding is not None:
            result["embedding"] = self.embedding
        
        if self.score is not None:
            result["score"] = self.score
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Chunk":
        """Create Chunk from dictionary."""
        metadata = ChunkMetadata.from_dict(data.get("metadata", {}))
        return cls(
            id=data.get("id", ""),
            text=data["text"],
            metadata=metadata,
            embedding=data.get("embedding"),
            score=data.get("score")
        )
    
    def __len__(self) -> int:
        """Return length of chunk text."""
        return len(self.text)
    
    def __repr__(self) -> str:
        """String representation of chunk."""
        preview = self.text[:50] + "..." if len(self.text) > 50 else self.text
        preview = preview.replace("\n", " ")
        return f"Chunk(id='{self.id[:12]}...', len={len(self.text)}, type='{self.metadata.chunk_type}')"


def generate_chunk_id(text: str, source: str, method: str = "hash") -> str:
    """
    Generate a unique ID for a chunk.
    
    Args:
        text: The chunk text content
        source: Source document identifier
        method: ID generation method ('hash' or 'uuid')
        
    Returns:
        Unique chunk identifier
    """
    if method == "uuid":
        return str(uuid.uuid4())
    
    # Hash-based ID (default)
    content = f"{source}:{text[:100]}"
    hash_obj = hashlib.sha256(content.encode('utf-8'))
    return hash_obj.hexdigest()[:16]


def validate_chunk(chunk: Chunk) -> tuple[bool, Optional[str]]:
    """
    Validate a chunk for required fields and content.
    
    Args:
        chunk: Chunk to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(chunk, Chunk):
        return False, "Not a Chunk instance"
    
    if not chunk.id:
        return False, "Chunk ID is required"
    
    if not chunk.text or not chunk.text.strip():
        return False, "Chunk text is empty"
    
    if len(chunk.text) < 10:
        return False, "Chunk text is too short (minimum 10 characters)"
    
    valid_types = ["theory", "code", "equation", "mixed", "general", "tutorial", "reference"]
    if chunk.metadata.chunk_type not in valid_types:
        return False, f"Invalid chunk_type: {chunk.metadata.chunk_type}"
    
    return True, None
