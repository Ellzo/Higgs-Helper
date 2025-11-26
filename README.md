# ⚛️ Higgs-Helper

**Particle Physics Research Assistant with RAG and PyHEP Integration**

Higgs-Helper is an intelligent assistant designed specifically for particle physics research. It combines Retrieval-Augmented Generation (RAG) with physics-aware document processing, providing contextual answers about particle physics, detector systems, and analysis techniques. The tool also includes specialized features for ROOT C++ code explanation and translation to modern PyHEP libraries.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## ✨ Features

### 🤖 Physics-Aware RAG System
- **Smart Document Chunking**: Preserves LaTeX mathematical expressions and code blocks
- **FAISS Vector Search**: Efficient similarity search with metadata filtering
- **Physics-Specific Re-ranking**: Boosts relevance for detector terms, formulas, and code
- **Gemini 2.0 Integration**: Powered by Google's latest LLM for accurate responses
- **Citation Tracking**: All answers include source references

### 🔬 Physics Tools
- **4-Vector Parser**: Extract momentum vectors from ROOT C++ or Python code
- **Kinematic Calculations**: Invariant mass, ΔR, pT, η, φ, and more
- **ROOT Code Explainer**: Natural language explanations of ROOT idioms
- **Python Translation**: Convert ROOT C++ to modern PyHEP (uproot/awkward/coffea)

### 🖥️ Interactive UI
- **Chat Interface**: Conversational queries about physics topics
- **Code Explainer Tool**: Paste ROOT code, get explanations and Python translations
- **Physics Calculator**: Interactive invariant mass and kinematics calculator
- **Document Viewer**: Inspect retrieved chunks and their relevance scores
- **Configuration Panel**: Customize model settings and retrieval parameters

### 🧪 PyHEP Integration
- Compatible with the PyHEP stack: `uproot`, `awkward`, `vector`, `coffea`
- Example notebooks demonstrating modern Python-based HEP analysis
- Helps bridge the gap between ROOT and Python ecosystems

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Higgs-Helper.git
cd Higgs-Helper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make install
# Or: pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Build Search Index

```bash
# Build index from sample corpus
make build-index

# Or with custom paths:
python src/main.py build-index \
    --corpus-path ./path/to/documents \
    --output-path ./data/index
```

### Launch UI

```bash
# Start Streamlit app
make run-ui

# Or directly:
streamlit run src/ui/streamlit_app.py
```

The UI will be available at `http://localhost:8501`

### CLI Usage

```bash
# Query the RAG system
python src/main.py query \
    --question "How was the Higgs boson discovered?" \
    --index-path ./data/index

# Calculate invariant mass
python src/main.py calculate-mass \
    --input "px=45.0, py=30.0, pz=20.0, E=100.0"

# Explain ROOT code
python src/main.py explain-code \
    --code "TLorentzVector p1; p1.SetPtEtaPhiM(25, 0.5, 1.2, 0.105);" \
    --language cpp

# Translate to Python
python src/main.py translate-code \
    --code "TFile* f = TFile::Open(\"data.root\");"
```

## 📖 Architecture

Higgs-Helper is built with a modular architecture:

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit UI                         │
├─────────────────────────────────────────────────────────┤
│              RAG Pipeline + Safety Filter               │
├──────────────┬──────────────────┬──────────────────────┤
│   Retriever  │   LLM Client     │   Physics Modules    │
│   + Reranker │   (Gemini 2.0)   │   - Parser           │
│              │                  │   - Calculations     │
│              │                  │   - Code Explainer   │
├──────────────┴──────────────────┴──────────────────────┤
│         FAISS Vector Store + Metadata Store             │
├─────────────────────────────────────────────────────────┤
│         Embedder (Gemini) + Physics-Aware Chunker       │
└─────────────────────────────────────────────────────────┘
```

For detailed architecture documentation, see [`docs/architecture.md`](docs/architecture.md).

### Key Components

- **Chunker** ([`src/rag/chunker.py`](src/rag/chunker.py)): Physics-aware document splitting
- **Vector Store** ([`src/rag/vector_store.py`](src/rag/vector_store.py)): FAISS-based similarity search
- **Retriever** ([`src/rag/retriever.py`](src/rag/retriever.py)): Retrieval with physics re-ranking
- **RAG Pipeline** ([`src/rag/rag_pipeline.py`](src/rag/rag_pipeline.py)): End-to-end query processing
- **Physics Modules** ([`src/physics/`](src/physics/)): 4-vector parsing and calculations

## 🐳 Docker

```bash
# Build image
make docker-build

# Run container
make docker-run

# Or with docker-compose
docker-compose up
```

## 🧪 Testing

```bash
# Run test suite
make test

# Run with coverage
make coverage

# Lint code
make lint

# Format code
make format
```

## 📚 Documentation

- [Architecture Overview](docs/architecture.md)
- [Chunking Strategy](docs/chunking_strategy.md)
- [Retrieval Scoring](docs/retrieval_scoring.md)
- [API Reference](docs/api_reference.md) *(coming soon)*
- [Example Notebooks](examples/)

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PyHEP Community**: For developing the modern Python HEP ecosystem
- **Google Gemini**: For providing powerful LLM and embedding APIs
- **FAISS**: For efficient vector similarity search
- **Streamlit**: For the intuitive UI framework
- **CERN**: For ROOT and decades of particle physics software development

## 📧 Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/Higgs-Helper/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/Higgs-Helper/discussions)

## 🗺️ Roadmap

- [ ] Support for additional LLM backends (Claude, GPT-4)
- [ ] Integration with CERN Open Data Portal
- [ ] Advanced plotting with mplhep templates
- [ ] Collaborative features for research teams
- [ ] REST API for programmatic access
- [ ] Support for custom physics corpus ingestion

---

**Built with ⚛️ for the particle physics community**