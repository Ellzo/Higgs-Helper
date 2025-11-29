"""
Tests for Dataset Schema and Loader

Tests cover:
- Document and Metadata creation
- Validation functions
- DatasetLoader with various sources
- Error handling
"""

import pytest
import json
import tempfile
from pathlib import Path
from src.rag.dataset.schema import Document, Metadata, validate_document, validate_metadata
from src.rag.dataset.loader import DatasetLoader


class TestMetadata:
    """Tests for Metadata dataclass."""
    
    def test_metadata_creation(self):
        """Test creating metadata with all fields."""
        metadata = Metadata(
            title="Test Document",
            section="Introduction",
            tags=["test", "physics"],
            doc_type="theory",
            author="Test Author",
            source="test.md"
        )
        
        assert metadata.title == "Test Document"
        assert metadata.section == "Introduction"
        assert metadata.tags == ["test", "physics"]
        assert metadata.doc_type == "theory"
        assert metadata.author == "Test Author"
        assert metadata.source == "test.md"
        assert metadata.language == "en"
    
    def test_metadata_defaults(self):
        """Test metadata with default values."""
        metadata = Metadata(title="Test")
        
        assert metadata.title == "Test"
        assert metadata.section is None
        assert metadata.tags == []
        assert metadata.doc_type == "general"
        assert metadata.language == "en"
        assert metadata.created_at is not None
    
    def test_metadata_to_dict(self):
        """Test converting metadata to dictionary."""
        metadata = Metadata(
            title="Test",
            tags=["a", "b"],
            doc_type="tutorial"
        )
        
        data = metadata.to_dict()
        
        assert data["title"] == "Test"
        assert data["tags"] == ["a", "b"]
        assert data["doc_type"] == "tutorial"
        assert "created_at" in data
    
    def test_metadata_from_dict(self):
        """Test creating metadata from dictionary."""
        data = {
            "title": "Test Doc",
            "section": "Methods",
            "tags": ["physics", "simulation"],
            "doc_type": "reference",
            "author": "John Doe"
        }
        
        metadata = Metadata.from_dict(data)
        
        assert metadata.title == "Test Doc"
        assert metadata.section == "Methods"
        assert metadata.tags == ["physics", "simulation"]
        assert metadata.doc_type == "reference"
        assert metadata.author == "John Doe"
    
    def test_validate_metadata_valid(self):
        """Test validation of valid metadata."""
        metadata = Metadata(title="Valid", tags=["test"])
        is_valid, error = validate_metadata(metadata)
        
        assert is_valid
        assert error is None
    
    def test_validate_metadata_empty_title(self):
        """Test validation fails for empty title."""
        metadata = Metadata(title="")
        is_valid, error = validate_metadata(metadata)
        
        assert not is_valid
        assert "Title is required" in error
    
    def test_validate_metadata_invalid_tags(self):
        """Test validation fails for non-list tags."""
        metadata = Metadata(title="Test")
        metadata.tags = "not a list"
        is_valid, error = validate_metadata(metadata)
        
        assert not is_valid
        assert "Tags must be a list" in error


class TestDocument:
    """Tests for Document dataclass."""
    
    def test_document_creation(self):
        """Test creating a document."""
        metadata = Metadata(title="Test")
        doc = Document(
            id="doc-001",
            content="This is test content.",
            metadata=metadata,
            source="test.txt"
        )
        
        assert doc.id == "doc-001"
        assert doc.content == "This is test content."
        assert doc.metadata.title == "Test"
        assert doc.source == "test.txt"
    
    def test_document_auto_id(self):
        """Test automatic ID generation."""
        metadata = Metadata(title="Test")
        doc = Document(
            id="",
            content="Content",
            metadata=metadata,
            source="test.txt"
        )
        
        # Should have generated a UUID
        assert doc.id != ""
        assert len(doc.id) > 10
    
    def test_document_empty_content_raises(self):
        """Test that empty content raises ValueError."""
        metadata = Metadata(title="Test")
        
        with pytest.raises(ValueError, match="content cannot be empty"):
            Document(
                id="doc-001",
                content="",
                metadata=metadata,
                source="test.txt"
            )
    
    def test_document_invalid_metadata_raises(self):
        """Test that invalid metadata raises TypeError."""
        with pytest.raises(TypeError, match="must be a Metadata instance"):
            Document(
                id="doc-001",
                content="Content",
                metadata="not metadata",
                source="test.txt"
            )
    
    def test_document_to_dict(self):
        """Test converting document to dictionary."""
        metadata = Metadata(title="Test", tags=["a"])
        doc = Document(
            id="doc-001",
            content="Content",
            metadata=metadata,
            source="test.txt"
        )
        
        data = doc.to_dict()
        
        assert data["id"] == "doc-001"
        assert data["content"] == "Content"
        assert data["source"] == "test.txt"
        assert data["metadata"]["title"] == "Test"
    
    def test_document_from_dict(self):
        """Test creating document from dictionary."""
        data = {
            "id": "doc-001",
            "content": "Test content",
            "source": "test.txt",
            "metadata": {
                "title": "Test",
                "tags": ["physics"]
            }
        }
        
        doc = Document.from_dict(data)
        
        assert doc.id == "doc-001"
        assert doc.content == "Test content"
        assert doc.source == "test.txt"
        assert doc.metadata.title == "Test"
    
    def test_document_len(self):
        """Test document length."""
        metadata = Metadata(title="Test")
        doc = Document(
            id="doc-001",
            content="12345",
            metadata=metadata,
            source="test.txt"
        )
        
        assert len(doc) == 5
    
    def test_validate_document_valid(self):
        """Test validation of valid document."""
        metadata = Metadata(title="Test")
        doc = Document(
            id="doc-001",
            content="This is valid content.",
            metadata=metadata,
            source="test.txt"
        )
        
        is_valid, error = validate_document(doc)
        
        assert is_valid
        assert error is None
    
    def test_validate_document_too_short(self):
        """Test validation fails for short content."""
        metadata = Metadata(title="Test")
        doc = Document(
            id="doc-001",
            content="short",
            metadata=metadata,
            source="test.txt"
        )
        
        is_valid, error = validate_document(doc)
        
        assert not is_valid
        assert "too short" in error
    
    def test_validate_document_invalid_type(self):
        """Test validation fails for invalid doc_type."""
        metadata = Metadata(title="Test", doc_type="invalid_type")
        doc = Document(
            id="doc-001",
            content="Valid content here.",
            metadata=metadata,
            source="test.txt"
        )
        
        is_valid, error = validate_document(doc)
        
        assert not is_valid
        assert "Invalid doc_type" in error


class TestDatasetLoader:
    """Tests for DatasetLoader class."""
    
    def test_loader_initialization(self):
        """Test initializing a loader."""
        loader = DatasetLoader()
        assert loader.default_metadata == {}
        assert loader.get_loaded_documents() == []
    
    def test_loader_with_defaults(self):
        """Test loader with default metadata."""
        defaults = {"doc_type": "reference", "author": "Default Author"}
        loader = DatasetLoader(default_metadata=defaults)
        
        assert loader.default_metadata == defaults
    
    def test_load_single_document(self):
        """Test loading a single document."""
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Test Document\n\nThis is test content.")
            temp_path = f.name
        
        try:
            loader = DatasetLoader()
            doc = loader.load_single_document(temp_path, metadata={"title": "Test"})
            
            assert doc.content == "# Test Document\n\nThis is test content."
            assert doc.metadata.title == "Test"
            assert len(loader.get_loaded_documents()) == 1
        finally:
            Path(temp_path).unlink()
    
    def test_load_single_document_not_found(self):
        """Test loading non-existent file raises error."""
        loader = DatasetLoader()
        
        with pytest.raises(FileNotFoundError):
            loader.load_single_document("/nonexistent/file.txt")
    
    def test_load_with_frontmatter(self):
        """Test loading document with YAML frontmatter."""
        content = """---
title: Frontmatter Test
tags: ["test", "yaml"]
doc_type: tutorial
---

# Content

This is the actual content."""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            loader = DatasetLoader()
            doc = loader.load_single_document(temp_path)
            
            assert doc.metadata.title == "Frontmatter Test"
            assert "test" in doc.metadata.tags
            assert doc.metadata.doc_type == "tutorial"
            assert "Content" in doc.content
            assert "---" not in doc.content  # Frontmatter should be stripped
        finally:
            Path(temp_path).unlink()
    
    def test_load_from_directory(self):
        """Test loading all documents from a directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            (Path(tmpdir) / "doc1.md").write_text("Content 1")
            (Path(tmpdir) / "doc2.md").write_text("Content 2")
            (Path(tmpdir) / "doc3.txt").write_text("Content 3")
            (Path(tmpdir) / "ignore.pdf").write_text("Should be ignored")
            
            loader = DatasetLoader()
            docs = loader.load_from_directory(tmpdir)
            
            assert len(docs) == 3  # Only .md and .txt files
            contents = [doc.content for doc in docs]
            assert "Content 1" in contents
            assert "Content 2" in contents
            assert "Content 3" in contents
    
    def test_load_from_directory_not_found(self):
        """Test loading from non-existent directory raises error."""
        loader = DatasetLoader()
        
        with pytest.raises(FileNotFoundError):
            loader.load_from_directory("/nonexistent/directory")
    
    def test_load_from_directory_empty(self):
        """Test loading from empty directory raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            loader = DatasetLoader()
            
            with pytest.raises(ValueError, match="No valid documents found"):
                loader.load_from_directory(tmpdir)
    
    def test_load_from_json(self):
        """Test loading documents from JSON file."""
        docs_data = [
            {
                "id": "doc-1",
                "content": "First document content",
                "source": "source1.txt",
                "metadata": {
                    "title": "Document 1",
                    "tags": ["test"]
                }
            },
            {
                "id": "doc-2",
                "content": "Second document content",
                "source": "source2.txt",
                "metadata": {
                    "title": "Document 2",
                    "doc_type": "theory"
                }
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(docs_data, f)
            temp_path = f.name
        
        try:
            loader = DatasetLoader()
            docs = loader.load_from_json(temp_path)
            
            assert len(docs) == 2
            assert docs[0].id == "doc-1"
            assert docs[0].metadata.title == "Document 1"
            assert docs[1].id == "doc-2"
            assert docs[1].metadata.doc_type == "theory"
        finally:
            Path(temp_path).unlink()
    
    def test_load_from_json_invalid(self):
        """Test loading invalid JSON raises error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json")
            temp_path = f.name
        
        try:
            loader = DatasetLoader()
            
            with pytest.raises(ValueError, match="Invalid JSON"):
                loader.load_from_json(temp_path)
        finally:
            Path(temp_path).unlink()
    
    def test_validate_documents(self):
        """Test document validation."""
        metadata_valid = Metadata(title="Valid")
        metadata_invalid = Metadata(title="Invalid", doc_type="bad_type")
        
        doc_valid = Document(
            id="valid",
            content="This is valid content.",
            metadata=metadata_valid,
            source="valid.txt"
        )
        
        doc_invalid = Document(
            id="invalid",
            content="Also valid content.",
            metadata=metadata_invalid,
            source="invalid.txt"
        )
        
        loader = DatasetLoader()
        valid, invalid = loader.validate_documents([doc_valid, doc_invalid])
        
        assert len(valid) == 1
        assert len(invalid) == 1
        assert valid[0].id == "valid"
        assert invalid[0][0].id == "invalid"
        assert "Invalid doc_type" in invalid[0][1]
    
    def test_export_to_json(self):
        """Test exporting documents to JSON."""
        metadata = Metadata(title="Export Test", tags=["export"])
        doc = Document(
            id="export-1",
            content="Export content",
            metadata=metadata,
            source="export.txt"
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.json"
            
            loader = DatasetLoader()
            loader.export_to_json([doc], str(output_path))
            
            # Load and verify
            with open(output_path, 'r') as f:
                data = json.load(f)
            
            assert len(data) == 1
            assert data[0]["id"] == "export-1"
            assert data[0]["metadata"]["title"] == "Export Test"
    
    def test_clear_cache(self):
        """Test clearing the document cache."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test content")
            temp_path = f.name
        
        try:
            loader = DatasetLoader()
            loader.load_single_document(temp_path, metadata={"title": "Test"})
            
            assert len(loader.get_loaded_documents()) == 1
            
            loader.clear_cache()
            
            assert len(loader.get_loaded_documents()) == 0
        finally:
            Path(temp_path).unlink()
    
    def test_load_sample_corpus(self):
        """Test loading the actual sample corpus."""
        corpus_path = Path(__file__).parent.parent / "src" / "rag" / "dataset" / "sample_corpus"
        
        if not corpus_path.exists():
            pytest.skip("Sample corpus not found")
        
        loader = DatasetLoader()
        docs = loader.load_from_directory(str(corpus_path))
        
        # Should have 5 documents
        assert len(docs) >= 5
        
        # Check that they have physics content
        titles = [doc.metadata.title for doc in docs]
        assert any("Higgs" in title for title in titles)
        assert any("Standard Model" in title or "ROOT" in title for title in titles)
        
        # Check for LaTeX content (should be present in physics docs)
        all_content = " ".join([doc.content for doc in docs])
        assert "$$" in all_content or "$" in all_content
        
        # Validate all documents
        valid, invalid = loader.validate_documents(docs)
        assert len(invalid) == 0, f"Invalid documents found: {invalid}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
