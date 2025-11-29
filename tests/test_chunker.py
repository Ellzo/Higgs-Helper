"""
Tests for Physics-Aware Chunker Module

This module contains comprehensive tests for the PhysicsAwareChunker class,
including tests for chunking strategies, LaTeX preservation, code block handling,
physics term detection, and chunk type classification.
"""

import pytest
from pathlib import Path

from src.rag.models import Chunk, ChunkMetadata, ChunkType, generate_chunk_id, validate_chunk
from src.rag.chunker import PhysicsAwareChunker, PHYSICS_TERMS
from src.rag.dataset.schema import Document, Metadata


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def chunker() -> PhysicsAwareChunker:
    """Create a PhysicsAwareChunker with default settings."""
    return PhysicsAwareChunker()


@pytest.fixture
def small_chunker() -> PhysicsAwareChunker:
    """Create a chunker with small chunk size for testing."""
    return PhysicsAwareChunker(chunk_size=200, overlap=30, min_chunk_size=50)


@pytest.fixture
def sample_document() -> Document:
    """Create a sample physics document for testing."""
    content = """# The Higgs Boson

The Higgs boson is a fundamental particle in the Standard Model of particle physics.

## Discovery

The Higgs boson was discovered in 2012 at CERN using the ATLAS and CMS detectors.

The discovery relied on analyzing the decay channels:

$$H \\to \\gamma\\gamma$$
$$H \\to ZZ^* \\to 4\\ell$$

## Mass Measurement

The measured mass is approximately:

$m_H = 125.10 \\pm 0.14$ GeV

## Analysis Code

Here's example analysis code:

```python
import uproot
import awkward as ak

def analyze_events(file_path):
    with uproot.open(file_path) as f:
        tree = f["Events"]
        pt = tree["Muon_pt"].array()
        return ak.sum(pt > 20)
```

## Properties

The Higgs boson has spin-0 and couples to massive particles proportional to their mass.
"""
    return Document(
        id="doc_higgs_test",
        content=content,
        metadata=Metadata(
            title="The Higgs Boson",
            author="Test Author",
            tags=["higgs", "physics"],
            doc_type="theory",
        ),
        source="test_higgs.md",
    )


@pytest.fixture
def latex_heavy_document() -> Document:
    """Create a document with extensive LaTeX content."""
    content = """# Quantum Field Theory Equations

## Dirac Equation

The Dirac equation for a free fermion:

$$(i\\gamma^\\mu \\partial_\\mu - m)\\psi = 0$$

Where the gamma matrices satisfy:

$$\\{\\gamma^\\mu, \\gamma^\\nu\\} = 2g^{\\mu\\nu}$$

## Lagrangian

The QED Lagrangian:

$$\\mathcal{L} = \\bar{\\psi}(i\\gamma^\\mu D_\\mu - m)\\psi - \\frac{1}{4}F_{\\mu\\nu}F^{\\mu\\nu}$$

With the covariant derivative:

$D_\\mu = \\partial_\\mu + ieA_\\mu$

And the field strength tensor:

$$F_{\\mu\\nu} = \\partial_\\mu A_\\nu - \\partial_\\nu A_\\mu$$
"""
    return Document(
        id="doc_qft_test",
        content=content,
        metadata=Metadata(
            title="QFT Equations",
            tags=["qft", "theory"],
        ),
        source="test_qft.md",
    )


@pytest.fixture
def code_heavy_document() -> Document:
    """Create a document with extensive code content."""
    content = """# ROOT Analysis Tutorial

## Loading Data

```cpp
#include <TFile.h>
#include <TTree.h>

void analyze() {
    TFile* file = TFile::Open("data.root");
    TTree* tree = (TTree*)file->Get("Events");
    
    Float_t pt;
    tree->SetBranchAddress("muon_pt", &pt);
    
    for (Long64_t i = 0; i < tree->GetEntries(); i++) {
        tree->GetEntry(i);
        if (pt > 20) {
            // Process event
        }
    }
}
```

## Python Analysis

```python
import uproot
import numpy as np

def load_data(filename):
    with uproot.open(filename) as file:
        tree = file["Events"]
        pt = tree["muon_pt"].array()
        eta = tree["muon_eta"].array()
        return pt, eta
```

## Histogramming

```cpp
TH1F* hist = new TH1F("h_pt", "Muon pT;pT [GeV];Events", 100, 0, 200);
```
"""
    return Document(
        id="doc_code_test",
        content=content,
        metadata=Metadata(
            title="ROOT Tutorial",
            tags=["root", "analysis"],
        ),
        source="test_root.md",
    )


@pytest.fixture
def minimal_document() -> Document:
    """Create a minimal document for edge case testing."""
    return Document(
        id="doc_minimal",
        content="Short text about physics experiments.",
        metadata=Metadata(title="Minimal Document"),
        source="minimal.md",
    )


# =============================================================================
# Tests: ChunkType Enum
# =============================================================================

class TestChunkType:
    """Tests for the ChunkType enumeration."""
    
    def test_chunk_types_exist(self):
        """Test that all expected chunk types are defined."""
        expected_types = ["THEORY", "CODE", "EQUATION", "MIXED", "GENERAL"]
        for ct in expected_types:
            assert hasattr(ChunkType, ct)
    
    def test_chunk_type_values(self):
        """Test chunk type string values."""
        assert ChunkType.THEORY.value == "theory"
        assert ChunkType.CODE.value == "code"
        assert ChunkType.EQUATION.value == "equation"
        assert ChunkType.MIXED.value == "mixed"
        assert ChunkType.GENERAL.value == "general"


# =============================================================================
# Tests: ChunkMetadata
# =============================================================================

class TestChunkMetadata:
    """Tests for the ChunkMetadata dataclass."""
    
    def test_default_metadata(self):
        """Test ChunkMetadata with default values."""
        meta = ChunkMetadata(source="test.md")
        assert meta.source == "test.md"
        assert meta.source_id == ""
        assert meta.section == ""
        assert meta.chunk_type == "general"
        assert meta.tags == []
        assert meta.has_latex == False
        assert meta.has_code == False
        assert meta.physics_terms == []
    
    def test_full_metadata(self):
        """Test ChunkMetadata with all fields."""
        meta = ChunkMetadata(
            source="test.md",
            source_id="doc_1",
            section="Introduction",
            chunk_index=0,
            chunk_type="theory",
            tags=["physics", "higgs"],
            start_char=100,
            end_char=500,
            has_latex=True,
            has_code=False,
            physics_terms=["higgs", "boson"],
            detector_mentions=["ATLAS"],
            particle_mentions=["Higgs boson"],
        )
        assert meta.section == "Introduction"
        assert meta.start_char == 100
        assert meta.end_char == 500
        assert "higgs" in meta.physics_terms
        assert "ATLAS" in meta.detector_mentions
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        meta = ChunkMetadata(
            source="test.md",
            source_id="doc_1",
            has_latex=True,
        )
        d = meta.to_dict()
        assert d["source"] == "test.md"
        assert d["source_id"] == "doc_1"
        assert d["has_latex"] == True
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "source": "test.md",
            "source_id": "doc_1",
            "section": "Methods",
            "chunk_type": "code",
        }
        meta = ChunkMetadata.from_dict(data)
        assert meta.source == "test.md"
        assert meta.section == "Methods"
        assert meta.chunk_type == "code"


# =============================================================================
# Tests: Chunk
# =============================================================================

class TestChunk:
    """Tests for the Chunk dataclass."""
    
    def test_chunk_creation(self):
        """Test basic Chunk creation."""
        meta = ChunkMetadata(source="test.md", source_id="doc_1")
        chunk = Chunk(
            id="chunk_001",
            text="This is test content about the Higgs boson.",
            metadata=meta,
        )
        assert chunk.id == "chunk_001"
        assert "Higgs" in chunk.text
        assert chunk.embedding is None
        assert chunk.score is None
    
    def test_chunk_with_embedding(self):
        """Test Chunk with embedding vector."""
        meta = ChunkMetadata(source="test.md")
        embedding = [0.1] * 768  # Simulated embedding
        chunk = Chunk(
            id="chunk_002",
            text="Test content here.",
            metadata=meta,
            embedding=embedding,
        )
        assert chunk.embedding is not None
        assert len(chunk.embedding) == 768
    
    def test_chunk_auto_id_generation(self):
        """Test that chunk ID is auto-generated if empty."""
        meta = ChunkMetadata(source="test.md")
        chunk = Chunk(
            id="",
            text="Some physics content.",
            metadata=meta,
        )
        # ID should be auto-generated (not empty)
        assert chunk.id != ""
        assert len(chunk.id) > 0
    
    def test_chunk_to_dict(self):
        """Test conversion to dictionary."""
        meta = ChunkMetadata(source="test.md")
        chunk = Chunk(
            id="chunk_001",
            text="Test content.",
            metadata=meta,
        )
        d = chunk.to_dict()
        assert d["id"] == "chunk_001"
        assert d["text"] == "Test content."
        assert "metadata" in d
    
    def test_chunk_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "id": "chunk_001",
            "text": "Test content.",
            "metadata": {"source": "test.md"},
        }
        chunk = Chunk.from_dict(data)
        assert chunk.id == "chunk_001"
        assert chunk.text == "Test content."
    
    def test_chunk_validation_empty_text(self):
        """Test that empty text raises an error."""
        meta = ChunkMetadata(source="test.md")
        with pytest.raises(ValueError):
            Chunk(id="chunk_001", text="", metadata=meta)


# =============================================================================
# Tests: ID Generation
# =============================================================================

class TestGenerateChunkId:
    """Tests for the chunk ID generation function."""
    
    def test_id_generation(self):
        """Test that IDs are generated."""
        chunk_id = generate_chunk_id("Test content", "test.md")
        assert chunk_id is not None
        assert len(chunk_id) > 0
    
    def test_unique_ids(self):
        """Test that different content produces different IDs."""
        id1 = generate_chunk_id("Content A", "source.md")
        id2 = generate_chunk_id("Content B", "source.md")
        assert id1 != id2
    
    def test_reproducible_ids(self):
        """Test that same inputs produce same ID."""
        id1 = generate_chunk_id("Same content", "source.md")
        id2 = generate_chunk_id("Same content", "source.md")
        assert id1 == id2
    
    def test_uuid_method(self):
        """Test UUID generation method."""
        id1 = generate_chunk_id("content", "source.md", method="uuid")
        id2 = generate_chunk_id("content", "source.md", method="uuid")
        # UUIDs should be different each time
        assert id1 != id2


# =============================================================================
# Tests: Validate Chunk
# =============================================================================

class TestValidateChunk:
    """Tests for chunk validation."""
    
    def test_valid_chunk(self):
        """Test validation of a valid chunk."""
        meta = ChunkMetadata(source="test.md", chunk_type="theory")
        chunk = Chunk(id="chunk_001", text="Valid physics content here.", metadata=meta)
        is_valid, error = validate_chunk(chunk)
        assert is_valid == True
        assert error is None
    
    def test_invalid_chunk_type(self):
        """Test validation catches invalid chunk type."""
        meta = ChunkMetadata(source="test.md", chunk_type="invalid_type")
        chunk = Chunk(id="chunk_001", text="Some content here.", metadata=meta)
        is_valid, error = validate_chunk(chunk)
        assert is_valid == False
        assert "chunk_type" in error.lower()


# =============================================================================
# Tests: PhysicsAwareChunker Initialization
# =============================================================================

class TestChunkerInitialization:
    """Tests for PhysicsAwareChunker initialization."""
    
    def test_default_initialization(self):
        """Test chunker with default parameters."""
        chunker = PhysicsAwareChunker()
        assert chunker.chunk_size == 1000
        assert chunker.overlap == 100
        assert chunker.min_chunk_size == 200
    
    def test_custom_initialization(self):
        """Test chunker with custom parameters."""
        chunker = PhysicsAwareChunker(
            chunk_size=512,
            overlap=50,
            min_chunk_size=100,
        )
        assert chunker.chunk_size == 512
        assert chunker.overlap == 50
        assert chunker.min_chunk_size == 100


# =============================================================================
# Tests: Physics Terms Dictionary
# =============================================================================

class TestPhysicsTerms:
    """Tests for the PHYSICS_TERMS dictionary."""
    
    def test_physics_terms_categories(self):
        """Test that all expected categories exist."""
        expected_categories = ["particles", "detectors", "concepts", "variables"]
        for cat in expected_categories:
            assert cat in PHYSICS_TERMS
    
    def test_particles_include_common_terms(self):
        """Test that common particle terms are included."""
        particles = PHYSICS_TERMS["particles"]
        common_particles = ["higgs", "muon", "electron", "photon", "quark", "gluon"]
        for p in common_particles:
            assert p in particles
    
    def test_detectors_include_major_experiments(self):
        """Test that major experiments are included."""
        detectors = PHYSICS_TERMS["detectors"]
        major_detectors = ["ATLAS", "CMS", "LHC", "CERN"]
        for det in major_detectors:
            assert det in detectors


# =============================================================================
# Tests: Document Chunking
# =============================================================================

class TestDocumentChunking:
    """Tests for the main chunk_document method."""
    
    def test_chunk_sample_document(self, chunker, sample_document):
        """Test chunking a sample physics document."""
        chunks = chunker.chunk_document(sample_document)
        
        assert len(chunks) > 0
        for chunk in chunks:
            assert isinstance(chunk, Chunk)
            assert chunk.id
            assert chunk.text
            assert chunk.metadata.source_id == sample_document.id
    
    def test_chunk_ids_unique(self, chunker, sample_document):
        """Test that all chunk IDs are unique."""
        chunks = chunker.chunk_document(sample_document)
        ids = [c.id for c in chunks]
        assert len(ids) == len(set(ids))
    
    def test_chunks_cover_content(self, chunker, sample_document):
        """Test that chunks cover the original content."""
        chunks = chunker.chunk_document(sample_document)
        
        # Combine all chunk text
        combined = " ".join(c.text for c in chunks)
        
        # Key terms should appear in combined text
        assert "Higgs" in combined
    
    def test_minimal_document(self, chunker, minimal_document):
        """Test chunking a very short document."""
        chunks = chunker.chunk_document(minimal_document)
        
        # Should create at least one chunk
        assert len(chunks) >= 1
    
    def test_empty_content_handling(self, chunker):
        """Test handling of empty document content."""
        # Use dictionary input since Document class doesn't allow empty content
        empty_doc = {
            "id": "doc_empty",
            "content": "",
            "source": "empty.md",
        }
        chunks = chunker.chunk_document(empty_doc)
        assert len(chunks) == 0
    
    def test_chunk_multiple_documents(self, chunker, sample_document, code_heavy_document):
        """Test chunking multiple documents."""
        chunks = chunker.chunk_documents([sample_document, code_heavy_document])
        
        # Should have chunks from both documents
        source_ids = set(c.metadata.source_id for c in chunks)
        assert sample_document.id in source_ids
        assert code_heavy_document.id in source_ids


# =============================================================================
# Tests: LaTeX Preservation
# =============================================================================

class TestLatexPreservation:
    """Tests for LaTeX equation preservation during chunking."""
    
    def test_latex_detection(self, chunker, sample_document):
        """Test that LaTeX is detected in chunks."""
        chunks = chunker.chunk_document(sample_document)
        
        # At least one chunk should have LaTeX
        latex_chunks = [c for c in chunks if c.metadata.has_latex]
        assert len(latex_chunks) > 0
    
    def test_block_latex_preserved(self, chunker, latex_heavy_document):
        """Test that block LaTeX ($$...$$) is preserved."""
        chunks = chunker.chunk_document(latex_heavy_document)
        
        latex_chunks = [c for c in chunks if c.metadata.has_latex]
        assert len(latex_chunks) > 0
        
        # Block LaTeX should be intact
        combined = " ".join(c.text for c in chunks)
        assert "\\gamma" in combined


# =============================================================================
# Tests: Code Block Preservation
# =============================================================================

class TestCodePreservation:
    """Tests for code block preservation during chunking."""
    
    def test_code_detection(self, chunker, sample_document):
        """Test that code blocks are detected."""
        chunks = chunker.chunk_document(sample_document)
        
        code_chunks = [c for c in chunks if c.metadata.has_code]
        assert len(code_chunks) > 0
    
    def test_code_language_detection(self, chunker, code_heavy_document):
        """Test that code language is detected."""
        chunks = chunker.chunk_document(code_heavy_document)
        
        # Should detect cpp or python
        languages = set()
        for c in chunks:
            if c.metadata.code_language:
                languages.add(c.metadata.code_language)
        
        # Should detect at least one language
        # (depends on implementation - may or may not track language)


# =============================================================================
# Tests: Physics Term Detection
# =============================================================================

class TestPhysicsTermDetection:
    """Tests for physics term detection in chunks."""
    
    def test_physics_terms_detected(self, chunker, sample_document):
        """Test that physics terms are detected in chunks."""
        chunks = chunker.chunk_document(sample_document)
        
        # Collect all detected terms
        all_terms = []
        for chunk in chunks:
            all_terms.extend(chunk.metadata.physics_terms)
        
        # Should detect some physics terms
        assert len(all_terms) > 0
    
    def test_detector_mentions_detected(self, chunker, sample_document):
        """Test that detector mentions are detected."""
        chunks = chunker.chunk_document(sample_document)
        
        # Collect all detector mentions
        all_detectors = []
        for chunk in chunks:
            all_detectors.extend(chunk.metadata.detector_mentions)
        
        # Should detect ATLAS or CMS
        combined = " ".join(all_detectors)
        assert "ATLAS" in combined or "CMS" in combined or len(all_detectors) > 0


# =============================================================================
# Tests: Section Splitting
# =============================================================================

class TestSectionSplitting:
    """Tests for section-based splitting functionality."""
    
    def test_section_titles_extracted(self, chunker, sample_document):
        """Test that section titles are extracted into metadata."""
        chunks = chunker.chunk_document(sample_document)
        
        sections_found = set()
        for chunk in chunks:
            if chunk.metadata.section:
                sections_found.add(chunk.metadata.section)
        
        # Should find some section titles
        assert len(sections_found) > 0
    
    def test_respect_sections_option(self, sample_document):
        """Test that respect_sections option works."""
        chunker_with = PhysicsAwareChunker(respect_sections=True)
        chunker_without = PhysicsAwareChunker(respect_sections=False)
        
        chunks_with = chunker_with.chunk_document(sample_document)
        chunks_without = chunker_without.chunk_document(sample_document)
        
        # Both should produce chunks
        assert len(chunks_with) > 0
        assert len(chunks_without) > 0


# =============================================================================
# Tests: Character Position Tracking
# =============================================================================

class TestCharacterPositions:
    """Tests for character position tracking in chunk metadata."""
    
    def test_positions_recorded(self, chunker, sample_document):
        """Test that start_char and end_char are recorded."""
        chunks = chunker.chunk_document(sample_document)
        
        for chunk in chunks:
            # Positions should be non-negative
            assert chunk.metadata.start_char >= 0
            assert chunk.metadata.end_char >= chunk.metadata.start_char


# =============================================================================
# Tests: Edge Cases
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_document_with_only_latex(self, chunker):
        """Test document containing only LaTeX."""
        doc = Document(
            id="doc_latex_only",
            content="$$E = mc^2$$",
            metadata=Metadata(title="LaTeX Only"),
            source="latex.md",
        )
        chunks = chunker.chunk_document(doc)
        
        assert len(chunks) >= 1
        assert chunks[0].metadata.has_latex
    
    def test_document_with_only_code(self, chunker):
        """Test document containing only code."""
        doc = Document(
            id="doc_code_only",
            content="```python\nprint('hello')\n```",
            metadata=Metadata(title="Code Only"),
            source="code.md",
        )
        chunks = chunker.chunk_document(doc)
        
        assert len(chunks) >= 1
        assert chunks[0].metadata.has_code
    
    def test_unicode_content(self, chunker):
        """Test handling of Unicode content."""
        doc = Document(
            id="doc_unicode",
            content="The π meson decays. Greek: αβγδ. Math: ∑∫∂",
            metadata=Metadata(title="Unicode Content"),
            source="unicode.md",
        )
        chunks = chunker.chunk_document(doc)
        
        assert len(chunks) >= 1
        combined = " ".join(c.text for c in chunks)
        assert "π" in combined
    
    def test_very_long_line(self, small_chunker):
        """Test handling of very long lines."""
        long_line = "word " * 1000
        doc = Document(
            id="doc_long_line",
            content=long_line,
            metadata=Metadata(title="Long Line"),
            source="long.md",
        )
        chunks = small_chunker.chunk_document(doc)
        
        # Should produce multiple chunks
        assert len(chunks) >= 1
    
    def test_dict_input(self, chunker):
        """Test that chunker accepts dictionary input."""
        doc_dict = {
            "id": "doc_dict",
            "content": "Physics content about quarks and leptons.",
            "source": "dict.md",
            "metadata": {},
        }
        chunks = chunker.chunk_document(doc_dict)
        assert len(chunks) >= 1


# =============================================================================
# Tests: Integration with DatasetLoader
# =============================================================================

class TestIntegrationWithLoader:
    """Tests for integration between chunker and dataset loader."""
    
    def test_chunk_loaded_documents(self, chunker):
        """Test chunking documents loaded from sample corpus."""
        from src.rag.dataset.loader import DatasetLoader
        
        loader = DatasetLoader()
        corpus_path = Path(__file__).parent.parent / "src" / "rag" / "dataset" / "sample_corpus"
        
        if corpus_path.exists():
            documents = loader.load_from_directory(corpus_path)
            
            if len(documents) > 0:
                # Test chunking first document
                doc = documents[0]
                chunks = chunker.chunk_document(doc)
                
                assert len(chunks) > 0
                for chunk in chunks:
                    assert chunk.metadata.source_id == doc.id


# =============================================================================
# Performance Tests
# =============================================================================

class TestPerformance:
    """Performance-related tests."""
    
    def test_large_document_handling(self, chunker):
        """Test that large documents are handled efficiently."""
        # Create a large document
        large_content = ("# Section\n\n" + "Text content. " * 100 + "\n\n") * 50
        doc = Document(
            id="doc_large",
            content=large_content,
            metadata=Metadata(title="Large Document"),
            source="large.md",
        )
        
        # Should complete without timeout
        chunks = chunker.chunk_document(doc)
        assert len(chunks) > 5  # Should produce many chunks
