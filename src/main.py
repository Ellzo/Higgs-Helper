#!/usr/bin/env python3
"""
Higgs-Helper CLI Entry Point

This module provides command-line interface for Higgs-Helper operations including
chunking documents, building search indices, querying the RAG system, and running
physics calculations.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional


def cmd_chunk(args: argparse.Namespace) -> int:
    """
    Execute the chunk command to process documents with physics-aware chunking.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        int: Exit code (0 for success, non-zero for error)
    """
    from src.rag.dataset.loader import DatasetLoader
    from src.rag.chunker import PhysicsAwareChunker
    
    input_dir = Path(args.input_dir)
    output_file = Path(args.output_file)
    
    if not input_dir.exists():
        print(f"Error: Input directory '{input_dir}' does not exist", file=sys.stderr)
        return 1
    
    # Initialize loader and chunker
    loader = DatasetLoader()
    chunker = PhysicsAwareChunker(
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        min_chunk_size=args.min_chunk_size,
    )
    
    # Load documents
    print(f"Loading documents from '{input_dir}'...")
    try:
        documents = loader.load_from_directory(input_dir)
    except Exception as e:
        print(f"Error loading documents: {e}", file=sys.stderr)
        return 1
    
    if not documents:
        print("Warning: No documents found", file=sys.stderr)
        return 1
    
    print(f"Loaded {len(documents)} documents")
    
    # Chunk documents
    all_chunks = []
    for doc in documents:
        print(f"  Chunking: {doc.metadata.title or doc.source}")
        chunks = chunker.chunk_document(doc)
        all_chunks.extend(chunks)
    
    print(f"Created {len(all_chunks)} chunks")
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Write chunks to JSONL
    with open(output_file, "w", encoding="utf-8") as f:
        for chunk in all_chunks:
            chunk_dict = {
                "id": chunk.id,
                "text": chunk.text,
                "metadata": {
                    "source": chunk.metadata.source,
                    "source_id": chunk.metadata.source_id,
                    "section": chunk.metadata.section,
                    "chunk_index": chunk.metadata.chunk_index,
                    "chunk_type": chunk.metadata.chunk_type,
                    "tags": chunk.metadata.tags,
                    "start_char": chunk.metadata.start_char,
                    "end_char": chunk.metadata.end_char,
                    "has_latex": chunk.metadata.has_latex,
                    "has_code": chunk.metadata.has_code,
                    "code_language": chunk.metadata.code_language,
                    "physics_terms": chunk.metadata.physics_terms,
                    "detector_mentions": chunk.metadata.detector_mentions,
                    "particle_mentions": chunk.metadata.particle_mentions,
                },
            }
            f.write(json.dumps(chunk_dict, ensure_ascii=False) + "\n")
    
    print(f"Wrote chunks to '{output_file}'")
    
    # Print summary statistics
    print("\n--- Chunk Statistics ---")
    chunk_types = {}
    latex_count = 0
    code_count = 0
    
    for chunk in all_chunks:
        ct = chunk.metadata.chunk_type
        chunk_types[ct] = chunk_types.get(ct, 0) + 1
        if chunk.metadata.has_latex:
            latex_count += 1
        if chunk.metadata.has_code:
            code_count += 1
    
    for ct, count in sorted(chunk_types.items()):
        print(f"  {ct}: {count}")
    print(f"  Chunks with LaTeX: {latex_count}")
    print(f"  Chunks with code: {code_count}")
    
    return 0


def main() -> int:
    """
    Main CLI entry point for Higgs-Helper.
    
    Returns:
        int: Exit code (0 for success, non-zero for error)
    """
    parser = argparse.ArgumentParser(
        prog="higgs-helper",
        description="Higgs-Helper - Particle Physics RAG Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Chunk command
    chunk_parser = subparsers.add_parser(
        "chunk",
        help="Chunk documents with physics-aware processing"
    )
    chunk_parser.add_argument(
        "--input-dir",
        type=str,
        required=True,
        help="Directory containing documents to chunk"
    )
    chunk_parser.add_argument(
        "--output-file",
        type=str,
        required=True,
        help="Output JSONL file for chunked documents"
    )
    chunk_parser.add_argument(
        "--chunk-size",
        type=int,
        default=512,
        help="Target chunk size in characters (default: 512)"
    )
    chunk_parser.add_argument(
        "--overlap",
        type=int,
        default=50,
        help="Overlap between chunks in characters (default: 50)"
    )
    chunk_parser.add_argument(
        "--min-chunk-size",
        type=int,
        default=100,
        help="Minimum chunk size in characters (default: 100)"
    )
    chunk_parser.set_defaults(func=cmd_chunk)
    
    # Build-index command
    index_parser = subparsers.add_parser(
        "build-index",
        help="Build FAISS search index from chunked documents"
    )
    index_parser.add_argument(
        "--corpus-path",
        type=str,
        required=True,
        help="Path to corpus directory or JSONL file"
    )
    index_parser.add_argument(
        "--output-path",
        type=str,
        required=True,
        help="Output directory for index files"
    )
    
    # Query command
    query_parser = subparsers.add_parser(
        "query",
        help="Query the RAG system"
    )
    query_parser.add_argument(
        "--question",
        type=str,
        required=True,
        help="Question to ask the system"
    )
    query_parser.add_argument(
        "--index-path",
        type=str,
        required=True,
        help="Path to FAISS index directory"
    )
    query_parser.add_argument(
        "--k",
        type=int,
        default=5,
        help="Number of chunks to retrieve (default: 5)"
    )
    
    # Calculate-mass command
    mass_parser = subparsers.add_parser(
        "calculate-mass",
        help="Calculate invariant mass from 4-vectors"
    )
    mass_parser.add_argument(
        "--input",
        type=str,
        help="Code snippet or file containing 4-vectors"
    )
    
    # Explain-code command
    explain_parser = subparsers.add_parser(
        "explain-code",
        help="Explain ROOT/physics code"
    )
    explain_parser.add_argument(
        "--code",
        type=str,
        required=True,
        help="Code snippet to explain"
    )
    explain_parser.add_argument(
        "--language",
        type=str,
        choices=["cpp", "python"],
        default="cpp",
        help="Code language (default: cpp)"
    )
    
    # Translate-code command
    translate_parser = subparsers.add_parser(
        "translate-code",
        help="Translate ROOT C++ to Python"
    )
    translate_parser.add_argument(
        "--code",
        type=str,
        required=True,
        help="ROOT C++ code to translate"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute the command
    if args.command == "chunk":
        return cmd_chunk(args)
    else:
        # Placeholder for commands to be implemented in later phases
        print(f"Command '{args.command}' will be implemented in later phases")
        return 0


if __name__ == "__main__":
    sys.exit(main())
