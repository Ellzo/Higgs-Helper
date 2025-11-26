# Dataset Module

This module provides document loading, validation, and schema management for the Higgs-Helper RAG system.

## Components

### Schema (`schema.py`)

Defines the core data structures:

```python
from src.rag.dataset import Document, Metadata

# Create metadata
metadata = Metadata(
    title="Higgs Discovery",
    tags=["higgs", "LHC", "discovery"],
    doc_type="theory"
)

# Create document
doc = Document(
    id="doc-001",
    content="Document text here...",
    metadata=metadata,
    source="higgs_discovery.md"
)

# Validate
from src.rag.dataset.schema import validate_document
is_valid, error = validate_document(doc)
```

### Loader (`loader.py`)

Flexible document loading from various sources:

```python
from src.rag.dataset import DatasetLoader

loader = DatasetLoader()

# Load from directory
docs = loader.load_from_directory("src/rag/dataset/sample_corpus/")

# Load from JSON
docs = loader.load_from_json("documents.json")

# Load single file with custom metadata
doc = loader.load_single_document(
    "document.md",
    metadata={"doc_type": "tutorial"}
)

# Validate documents
valid_docs, invalid_docs = loader.validate_documents(docs)

# Export to JSON
loader.export_to_json(docs, "output.json")
```

### Sample Corpus

Located in `sample_corpus/`, contains 5 comprehensive physics documents:

1. **higgs_discovery.md** - Higgs boson discovery at the LHC
2. **standard_model_basics.md** - Standard Model particles and forces
3. **root_tutorial.md** - ROOT framework tutorial with code examples
4. **4vector_math.md** - Four-vector mathematics and kinematics
5. **detector_systems.md** - ATLAS and CMS detector descriptions

All documents include:
- YAML frontmatter with metadata
- Rich LaTeX equations
- Code examples (C++, Python)
- Physics-authentic content

## Features

- **Flexible Loading**: Supports .md, .txt, and .json files
- **Frontmatter Parsing**: Extracts metadata from YAML frontmatter
- **Validation**: Comprehensive validation with clear error messages
- **Type Safety**: Full type hints throughout
- **Error Handling**: Robust error handling for missing files, corrupt data
- **Extensible**: Easy to add new document types and sources

## Document Types

Supported document types:
- `theory` - Theoretical physics content
- `tutorial` - Tutorial and how-to guides
- `reference` - Reference material
- `code` - Code documentation
- `general` - General content
- `detector` - Detector system descriptions

## Frontmatter Format

Documents can include YAML frontmatter:

```markdown
---
title: Document Title
tags: ["tag1", "tag2"]
doc_type: theory
author: Author Name
---

# Document Content

Starts here...
```

## Testing

Run tests with:

```bash
pytest tests/test_dataset.py -v
```

Test coverage includes:
- Schema validation
- Document creation and serialization
- Loader functionality (directory, JSON, single file)
- Frontmatter parsing
- Error handling
- Sample corpus loading

## Usage Examples

### Load and Validate Sample Corpus

```python
from src.rag.dataset import DatasetLoader

loader = DatasetLoader()
docs = loader.load_from_directory("src/rag/dataset/sample_corpus/")

print(f"Loaded {len(docs)} documents")

for doc in docs:
    print(f"- {doc.metadata.title} ({len(doc)} chars)")
    print(f"  Tags: {', '.join(doc.metadata.tags)}")
```

### Create Custom Document

```python
from src.rag.dataset import Document, Metadata

metadata = Metadata(
    title="My Physics Document",
    tags=["custom", "physics"],
    doc_type="theory",
    author="Your Name"
)

doc = Document(
    id="",  # Will auto-generate UUID
    content="Your physics content here...",
    metadata=metadata,
    source="custom.md"
)

# Validate
from src.rag.dataset.schema import validate_document
is_valid, error = validate_document(doc)

if is_valid:
    print("Document is valid!")
else:
    print(f"Validation error: {error}")
```

### Export to JSON

```python
from src.rag.dataset import DatasetLoader

loader = DatasetLoader()
docs = loader.load_from_directory("src/rag/dataset/sample_corpus/")

# Export all documents
loader.export_to_json(docs, "corpus.json")

# Later, reload from JSON
loader2 = DatasetLoader()
reloaded_docs = loader2.load_from_json("corpus.json")
```

## API Reference

### Metadata

**Fields**:
- `title: str` - Document title (required)
- `section: Optional[str]` - Section within larger document
- `tags: List[str]` - Descriptive tags
- `doc_type: str` - Document type (default: "general")
- `created_at: str` - ISO timestamp (auto-generated)
- `author: Optional[str]` - Author name
- `source: Optional[str]` - Source file/URL
- `language: str` - Language code (default: "en")

**Methods**:
- `to_dict() -> Dict` - Convert to dictionary
- `from_dict(data: Dict) -> Metadata` - Create from dictionary

### Document

**Fields**:
- `id: str` - Unique identifier (auto-generated if empty)
- `content: str` - Document text (required, min 10 chars)
- `metadata: Metadata` - Associated metadata (required)
- `source: str` - Source identifier (required)

**Methods**:
- `to_dict() -> Dict` - Convert to dictionary
- `from_dict(data: Dict) -> Document` - Create from dictionary
- `__len__() -> int` - Get content length

### DatasetLoader

**Methods**:
- `load_from_directory(directory, extensions=['.md', '.txt'], recursive=False) -> List[Document]`
- `load_from_json(json_path) -> List[Document]`
- `load_single_document(file_path, metadata=None) -> Document`
- `validate_documents(documents) -> Tuple[List[Document], List[Tuple[Document, str]]]`
- `export_to_json(documents, output_path)`
- `get_loaded_documents() -> List[Document]`
- `clear_cache()`

## Integration

This module integrates with:

- **Phase 2 (Chunker)**: Provides documents for physics-aware chunking
- **Phase 3 (Embedder)**: Document content for embedding generation
- **Phase 4 (RAG Pipeline)**: Source documents for retrieval

## Future Enhancements

Potential improvements for future versions:
- PDF loading support
- HTML parsing
- Binary format support (ROOT files)
- Streaming for large datasets
- Database backend
- Document versioning
