# Higgs-Helper Architecture

## Overview

Higgs-Helper is designed as a modular, extensible system for particle physics research assistance. The architecture follows a layered approach with clear separation of concerns.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interfaces                         │
│  ┌──────────────────────┐  ┌─────────────────────────────┐ │
│  │   Streamlit Web UI   │  │   Command-Line Interface    │ │
│  └──────────────────────┘  └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              RAG Pipeline Orchestrator               │  │
│  │  - Query Processing  - Safety Filtering              │  │
│  │  - Response Generation  - Citation Management        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Core Services Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │  Retriever   │  │  LLM Client  │  │ Physics Modules │  │
│  │  + Reranker  │  │  (Gemini)    │  │ - 4-Vec Parser  │  │
│  │              │  │              │  │ - Calculations  │  │
│  │              │  │              │  │ - Code Explainer│  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                               │
│  ┌──────────────────────┐  ┌───────────────────────────┐  │
│  │  FAISS Vector Store  │  │    Metadata Store         │  │
│  │  - Similarity Search │  │    - Chunk Metadata       │  │
│  │  - Index Persistence │  │    - JSONL Storage        │  │
│  └──────────────────────┘  └───────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                  Ingestion Layer                            │
│  ┌──────────────────────┐  ┌───────────────────────────┐  │
│  │  Document Loader     │  │  Physics-Aware Chunker    │  │
│  │  - Multiple Formats  │  │  - LaTeX Preservation     │  │
│  │  - Validation        │  │  - Code Block Handling    │  │
│  └──────────────────────┘  └───────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────┐  │
│  │            Gemini Embedding Service                 │  │
│  │  - Text Embeddings  - Batch Processing              │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. User Interfaces

#### Streamlit Web UI
- Interactive chat interface for physics queries
- Code explanation and translation tool
- Physics calculator with 4-vector input
- Retrieved documents viewer
- Configuration management

#### CLI
- Batch processing capabilities
- Scriptable operations
- Direct access to all core functions

### 2. Application Layer

#### RAG Pipeline
- **Query Processing**: Parses and normalizes user queries
- **Safety Filtering**: Blocks harmful or inappropriate requests
- **Context Retrieval**: Fetches relevant document chunks
- **Response Generation**: Generates answers using LLM
- **Citation Management**: Tracks and includes source references

### 3. Core Services

#### Retriever + Reranker
- **Vector Similarity**: Initial retrieval using FAISS
- **Physics-Aware Reranking**: Boosts chunks with:
  - LaTeX mathematical content
  - Code blocks (especially ROOT)
  - Detector terminology
  - Physics processes and particles

#### LLM Client (Gemini)
- Pluggable architecture for multiple LLM backends
- Streaming and batch generation
- Token management and rate limiting
- Error handling and retries

#### Physics Modules
- **4-Vector Parser**: Extracts momentum vectors from code
- **Calculations**: Invariant mass, ΔR, kinematic variables
- **Code Explainer**: ROOT idiom explanations
- **Python Translator**: ROOT C++ → PyHEP conversion

### 4. Data Layer

#### FAISS Vector Store
- CPU-optimized similarity search
- Multiple index types (Flat, IVF)
- Efficient nearest neighbor retrieval
- Persistence and loading

#### Metadata Store
- JSONL-based storage for inspection
- Chunk metadata (source, type, tags)
- Synchronization with vector indices

### 5. Ingestion Layer

#### Document Loader
- Supports text, Markdown, PDF formats
- Schema validation
- Error handling

#### Physics-Aware Chunker
- Preserves LaTeX expressions
- Keeps code blocks intact
- Respects section boundaries
- Configurable chunk sizes
- Metadata enrichment

#### Embedding Service
- Gemini API integration
- Batch processing for efficiency
- Rate limiting and error handling

## Data Flow

### Index Building Flow

```
Documents → Loader → Validator → Chunker → Embedder → Vector Store
                                    ↓
                              Metadata Store
```

1. Documents loaded from corpus directory
2. Validated against schema
3. Split into physics-aware chunks
4. Chunks embedded using Gemini
5. Vectors stored in FAISS index
6. Metadata stored in parallel JSONL

### Query Flow

```
User Query → Safety Filter → Embedder → Retriever → Reranker → LLM → Response
                                            ↓
                                      Vector Store
                                            ↓
                                     Metadata Store
```

1. User submits query via UI or CLI
2. Safety filter checks for harmful content
3. Query embedded using same embedder
4. Top-k chunks retrieved from FAISS
5. Chunks reranked using physics heuristics
6. Context formatted with chunks
7. LLM generates response with citations
8. Response returned to user

## Design Decisions

### Why FAISS?
- Proven efficiency for large-scale similarity search
- CPU-only version avoids GPU dependency
- Mature library with active development
- Easy persistence and loading

### Why Gemini?
- State-of-the-art language understanding
- Native embedding generation
- Competitive pricing
- Good handling of technical content

### Why Physics-Aware Chunking?
- LaTeX expressions lose meaning if split
- Code blocks must remain syntactically complete
- Physics terminology provides important context
- Improves retrieval relevance

### Why Pluggable Architecture?
- Easy to swap LLM backends
- Testing without API calls (mock components)
- Future support for local models
- Flexibility for different use cases

## Extension Points

### Adding New LLM Backends
Implement the `LLMClient` abstract class:
```python
class CustomLLMClient(LLMClient):
    def generate(self, prompt, system_instruction):
        # Your implementation
```

### Adding New Embedders
Implement the `Embedder` abstract class:
```python
class CustomEmbedder(Embedder):
    def embed_text(self, text):
        # Your implementation
```

### Adding New Vector Stores
Implement the same interface as `FAISSVectorStore`:
```python
class CustomVectorStore:
    def add_vectors(self, ids, vectors, metadata):
        # Your implementation
    
    def search(self, query_vector, k):
        # Your implementation
```

## Security Considerations

### Safety Filter
- Blocks requests for dangerous physics experiments
- Prevents extraction of training data
- Refuses illegal content requests

### API Key Management
- Keys stored in `.env` (not committed)
- Environment variable support
- Secure transmission to APIs

### Data Privacy
- No user queries stored by default
- Optional logging for debugging
- Local vector store (no cloud storage required)

## Performance Characteristics

### Chunking
- **Speed**: ~1000 chunks/second
- **Memory**: O(n) with document size

### Embedding
- **Speed**: Limited by API rate limits
- **Batch Size**: Configurable (default 100)

### Retrieval
- **Speed**: <100ms for top-10 from 10k chunks
- **Memory**: O(n*d) with index size

### Generation
- **Speed**: ~20 tokens/second (Gemini)
- **Context**: Up to 30k tokens

## Technology Stack Summary

- **Language**: Python 3.10+
- **Vector DB**: FAISS (CPU)
- **LLM**: Google Gemini 2.0
- **UI**: Streamlit
- **Physics**: uproot, awkward, vector, coffea
- **Testing**: pytest
- **Formatting**: black, flake8, mypy

## Future Enhancements

1. **Multi-modal Support**: Images, plots, diagrams
2. **Collaborative Features**: Shared workspaces
3. **Advanced Filtering**: By experiment, energy, detector
4. **REST API**: Programmatic access
5. **Local Models**: Support for offline operation
6. **Custom Corpus**: User-provided documents

---

*This document will be updated as the architecture evolves.*
