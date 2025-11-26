#!/usr/bin/env python3
"""
Higgs-Helper CLI Entry Point

This module provides command-line interface for Higgs-Helper operations including
chunking documents, building search indices, querying the RAG system, and running
physics calculations.
"""

import argparse
import sys
from typing import Optional


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
        help="Target chunk size in tokens (default: 512)"
    )
    chunk_parser.add_argument(
        "--overlap",
        type=int,
        default=50,
        help="Overlap between chunks (default: 50)"
    )
    
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
    
    # Placeholder implementations will be replaced in later phases
    print(f"Command '{args.command}' will be implemented in Phase 2-5")
    return 0


if __name__ == "__main__":
    sys.exit(main())
