"""
Physics-Aware Document Chunker

This module implements intelligent document chunking that preserves the integrity
of LaTeX mathematical expressions, code blocks, and physics-specific content.
"""

import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field

from .models import Chunk, ChunkMetadata, generate_chunk_id

logger = logging.getLogger(__name__)


# Physics terminology database
PHYSICS_TERMS = {
    # Particles
    "particles": [
        "higgs", "boson", "quark", "lepton", "muon", "electron", "photon",
        "neutrino", "gluon", "proton", "neutron", "meson", "pion", "kaon",
        "tau", "charm", "bottom", "top", "strange", "up", "down",
        "W boson", "Z boson", "fermion", "hadron", "baryon", "antiparticle"
    ],
    # Detectors
    "detectors": [
        "ATLAS", "CMS", "LHCb", "ALICE", "LHC", "CERN", "calorimeter",
        "tracker", "muon spectrometer", "ECAL", "HCAL", "pixel detector",
        "silicon strip", "drift tube", "trigger", "DAQ"
    ],
    # Concepts
    "concepts": [
        "invariant mass", "transverse momentum", "pseudorapidity", "rapidity",
        "cross section", "luminosity", "branching ratio", "decay width",
        "coupling", "vertex", "jet", "missing energy", "pile-up",
        "standard model", "supersymmetry", "dark matter", "CP violation",
        "electroweak", "QCD", "QED", "Feynman diagram", "amplitude"
    ],
    # Variables
    "variables": [
        "p_T", "pT", "η", "eta", "φ", "phi", "ΔR", "deltaR", "M_inv",
        "√s", "σ", "Γ", "α_s", "sin²θ_W", "E_T", "m_H"
    ]
}


@dataclass
class ProtectedBlock:
    """Represents a protected region that should not be split."""
    start: int
    end: int
    block_type: str  # 'latex_inline', 'latex_display', 'code', 'header'
    content: str


class PhysicsAwareChunker:
    """
    Chunks documents while preserving LaTeX expressions and code blocks.
    
    This chunker implements physics-aware splitting that respects:
    - LaTeX inline ($...$) and display ($$...$$) math
    - Markdown code blocks (```...```)
    - Section boundaries
    - Semantic coherence
    """
    
    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int = 100,
        min_chunk_size: int = 200,
        respect_sections: bool = True
    ):
        """
        Initialize the chunker.
        
        Args:
            chunk_size: Target size for each chunk in characters
            overlap: Number of overlapping characters between chunks
            min_chunk_size: Minimum acceptable chunk size
            respect_sections: Whether to prefer breaking at section boundaries
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.min_chunk_size = min_chunk_size
        self.respect_sections = respect_sections
        
        # Regex patterns for extraction
        self._latex_display_pattern = re.compile(r'\$\$([^$]+)\$\$', re.DOTALL)
        self._latex_inline_pattern = re.compile(r'(?<!\$)\$([^$\n]+)\$(?!\$)')
        self._code_block_pattern = re.compile(r'```(\w*)\n(.*?)```', re.DOTALL)
        self._header_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    
    def chunk_document(self, document: Any) -> List[Chunk]:
        """
        Chunk a document into smaller pieces.
        
        Args:
            document: Document object with 'content', 'metadata', 'id', 'source' attributes
                     or a dictionary with those keys
            
        Returns:
            List of Chunk objects
        """
        # Handle both Document objects and dictionaries
        if hasattr(document, 'content'):
            content = document.content
            source = document.source
            source_id = document.id
        else:
            content = document.get('content', '')
            source = document.get('source', 'unknown')
            source_id = document.get('id', '')
        
        if not content.strip():
            logger.warning(f"Empty document: {source}")
            return []
        
        # Extract protected blocks
        protected_blocks = self._find_protected_blocks(content)
        
        # Split by sections if enabled
        if self.respect_sections:
            sections = self._split_by_sections(content)
        else:
            sections = [("", content, 0)]
        
        chunks = []
        chunk_index = 0
        
        for section_title, section_text, section_start in sections:
            # Create chunks within this section
            section_chunks = self._create_chunks(
                text=section_text,
                section=section_title,
                source=source,
                source_id=source_id,
                offset=section_start,
                protected_blocks=protected_blocks,
                start_index=chunk_index
            )
            chunks.extend(section_chunks)
            chunk_index += len(section_chunks)
        
        logger.info(f"Created {len(chunks)} chunks from {source}")
        return chunks
    
    def chunk_documents(self, documents: List[Any]) -> List[Chunk]:
        """
        Chunk multiple documents.
        
        Args:
            documents: List of Document objects or dictionaries
            
        Returns:
            List of all chunks from all documents
        """
        all_chunks = []
        for doc in documents:
            chunks = self.chunk_document(doc)
            all_chunks.extend(chunks)
        return all_chunks
    
    def _find_protected_blocks(self, text: str) -> List[ProtectedBlock]:
        """
        Find all protected blocks (LaTeX, code) that should not be split.
        
        Args:
            text: Full document text
            
        Returns:
            List of ProtectedBlock objects sorted by start position
        """
        blocks = []
        
        # Find display LaTeX ($$...$$)
        for match in self._latex_display_pattern.finditer(text):
            blocks.append(ProtectedBlock(
                start=match.start(),
                end=match.end(),
                block_type='latex_display',
                content=match.group(0)
            ))
        
        # Find inline LaTeX ($...$)
        for match in self._latex_inline_pattern.finditer(text):
            blocks.append(ProtectedBlock(
                start=match.start(),
                end=match.end(),
                block_type='latex_inline',
                content=match.group(0)
            ))
        
        # Find code blocks (```...```)
        for match in self._code_block_pattern.finditer(text):
            blocks.append(ProtectedBlock(
                start=match.start(),
                end=match.end(),
                block_type='code',
                content=match.group(0)
            ))
        
        # Sort by start position
        blocks.sort(key=lambda b: b.start)
        return blocks
    
    def _split_by_sections(self, text: str) -> List[Tuple[str, str, int]]:
        """
        Split text by markdown headers.
        
        Args:
            text: Document text
            
        Returns:
            List of tuples (section_title, section_text, start_offset)
        """
        sections = []
        header_matches = list(self._header_pattern.finditer(text))
        
        if not header_matches:
            return [("", text, 0)]
        
        # Handle text before first header
        if header_matches[0].start() > 0:
            pre_text = text[:header_matches[0].start()].strip()
            if pre_text:
                sections.append(("", pre_text, 0))
        
        # Process each header and its content
        for i, match in enumerate(header_matches):
            title = match.group(2).strip()
            start = match.start()
            
            # End is either next header or end of text
            if i + 1 < len(header_matches):
                end = header_matches[i + 1].start()
            else:
                end = len(text)
            
            section_text = text[start:end].strip()
            if section_text:
                sections.append((title, section_text, start))
        
        return sections
    
    def _create_chunks(
        self,
        text: str,
        section: str,
        source: str,
        source_id: str,
        offset: int,
        protected_blocks: List[ProtectedBlock],
        start_index: int
    ) -> List[Chunk]:
        """
        Create chunks from text with protected block awareness.
        
        Args:
            text: Text to chunk
            section: Section title for metadata
            source: Source document path
            source_id: Source document ID
            offset: Character offset in original document
            protected_blocks: List of protected blocks
            start_index: Starting chunk index
            
        Returns:
            List of Chunk objects
        """
        if len(text) <= self.chunk_size:
            # Text fits in single chunk
            return [self._make_chunk(
                text=text,
                section=section,
                source=source,
                source_id=source_id,
                start_char=offset,
                end_char=offset + len(text),
                chunk_index=start_index
            )]
        
        chunks = []
        pos = 0
        chunk_index = start_index
        
        while pos < len(text):
            # Calculate end position for this chunk
            end_pos = min(pos + self.chunk_size, len(text))
            
            # Find safe boundary
            if end_pos < len(text):
                end_pos = self._find_safe_boundary(
                    text=text,
                    start=pos,
                    target_end=end_pos,
                    protected_blocks=protected_blocks,
                    offset=offset
                )
            
            chunk_text = text[pos:end_pos].strip()
            
            if len(chunk_text) >= self.min_chunk_size or not chunks:
                chunk = self._make_chunk(
                    text=chunk_text,
                    section=section,
                    source=source,
                    source_id=source_id,
                    start_char=offset + pos,
                    end_char=offset + end_pos,
                    chunk_index=chunk_index
                )
                chunks.append(chunk)
                chunk_index += 1
            elif chunks:
                # Append small remainder to previous chunk
                last_chunk = chunks[-1]
                combined_text = last_chunk.text + "\n\n" + chunk_text
                chunks[-1] = self._make_chunk(
                    text=combined_text,
                    section=section,
                    source=source,
                    source_id=source_id,
                    start_char=last_chunk.metadata.start_char,
                    end_char=offset + end_pos,
                    chunk_index=last_chunk.metadata.chunk_index
                )
            
            # Move position with overlap
            pos = end_pos - self.overlap if end_pos < len(text) else len(text)
            
            # Don't go backwards
            if chunks and pos <= chunks[-1].metadata.start_char - offset:
                pos = end_pos
        
        return chunks
    
    def _find_safe_boundary(
        self,
        text: str,
        start: int,
        target_end: int,
        protected_blocks: List[ProtectedBlock],
        offset: int
    ) -> int:
        """
        Find a safe position to break the text that doesn't split protected blocks.
        
        Args:
            text: Full text
            start: Start position
            target_end: Target end position
            protected_blocks: Protected blocks
            offset: Offset in original document
            
        Returns:
            Safe end position
        """
        actual_start = offset + start
        actual_end = offset + target_end
        
        # Check if we're inside a protected block
        for block in protected_blocks:
            if block.start < actual_end < block.end:
                # We're inside a block, move to end of block
                new_end = block.end - offset
                if new_end <= len(text):
                    target_end = new_end
                    break
        
        # Prefer breaking at paragraph boundaries
        search_start = max(start, target_end - 200)
        search_text = text[search_start:target_end]
        
        # Try to find a paragraph break
        para_break = search_text.rfind('\n\n')
        if para_break != -1 and para_break > len(search_text) // 2:
            return search_start + para_break + 2
        
        # Try sentence break
        for punct in ['. ', '.\n', '? ', '?\n', '! ', '!\n']:
            sent_break = search_text.rfind(punct)
            if sent_break != -1 and sent_break > len(search_text) // 3:
                return search_start + sent_break + len(punct)
        
        # Try line break
        line_break = search_text.rfind('\n')
        if line_break != -1 and line_break > len(search_text) // 3:
            return search_start + line_break + 1
        
        return target_end
    
    def _make_chunk(
        self,
        text: str,
        section: str,
        source: str,
        source_id: str,
        start_char: int,
        end_char: int,
        chunk_index: int
    ) -> Chunk:
        """
        Create a Chunk with enriched metadata.
        
        Args:
            text: Chunk text
            section: Section title
            source: Source document
            source_id: Source document ID
            start_char: Start character position
            end_char: End character position
            chunk_index: Index of this chunk
            
        Returns:
            Chunk object with metadata
        """
        # Analyze content
        has_latex = self._has_latex(text)
        has_code, code_lang = self._has_code(text)
        physics_terms = self._detect_physics_terms(text)
        detectors = self._detect_detectors(text)
        particles = self._detect_particles(text)
        chunk_type = self._classify_chunk_type(text, has_latex, has_code)
        tags = self._generate_tags(physics_terms, detectors, particles, has_latex, has_code)
        
        metadata = ChunkMetadata(
            source=source,
            source_id=source_id,
            section=section,
            chunk_index=chunk_index,
            chunk_type=chunk_type,
            tags=tags,
            has_latex=has_latex,
            has_code=has_code,
            code_language=code_lang,
            start_char=start_char,
            end_char=end_char,
            physics_terms=physics_terms,
            detector_mentions=detectors,
            particle_mentions=particles
        )
        
        chunk_id = generate_chunk_id(text, source)
        
        return Chunk(
            id=chunk_id,
            text=text,
            metadata=metadata
        )
    
    def _has_latex(self, text: str) -> bool:
        """Check if text contains LaTeX."""
        return bool(self._latex_display_pattern.search(text) or 
                   self._latex_inline_pattern.search(text))
    
    def _has_code(self, text: str) -> Tuple[bool, Optional[str]]:
        """Check if text contains code blocks and detect language."""
        match = self._code_block_pattern.search(text)
        if match:
            lang = match.group(1) if match.group(1) else None
            return True, lang
        return False, None
    
    def _detect_physics_terms(self, text: str) -> List[str]:
        """
        Detect physics terminology in text.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of detected physics terms
        """
        text_lower = text.lower()
        found = set()
        
        for term in PHYSICS_TERMS["concepts"]:
            if term.lower() in text_lower:
                found.add(term)
        
        for term in PHYSICS_TERMS["variables"]:
            if term.lower() in text_lower or term in text:
                found.add(term)
        
        return list(found)[:10]  # Limit to 10 terms
    
    def _detect_detectors(self, text: str) -> List[str]:
        """Detect detector mentions in text."""
        text_upper = text.upper()
        found = []
        
        for detector in PHYSICS_TERMS["detectors"][:8]:  # Main detectors
            if detector.upper() in text_upper:
                found.append(detector)
        
        return found
    
    def _detect_particles(self, text: str) -> List[str]:
        """Detect particle mentions in text."""
        text_lower = text.lower()
        found = []
        
        for particle in PHYSICS_TERMS["particles"]:
            if particle.lower() in text_lower:
                found.append(particle)
        
        return list(set(found))[:10]  # Limit and dedupe
    
    def _classify_chunk_type(self, text: str, has_latex: bool, has_code: bool) -> str:
        """
        Classify chunk by content type.
        
        Args:
            text: Chunk text
            has_latex: Whether chunk has LaTeX
            has_code: Whether chunk has code
            
        Returns:
            Chunk type string
        """
        text_lower = text.lower()
        
        if has_code and has_latex:
            return "mixed"
        elif has_code:
            return "code"
        elif has_latex:
            # Check if mostly equations
            latex_count = len(self._latex_display_pattern.findall(text)) + \
                         len(self._latex_inline_pattern.findall(text))
            if latex_count > 3:
                return "equation"
            return "theory"
        elif any(kw in text_lower for kw in ["tutorial", "example", "step", "how to"]):
            return "tutorial"
        elif any(kw in text_lower for kw in ["detector", "atlas", "cms", "tracker", "calorimeter"]):
            return "reference"
        else:
            return "theory"
    
    def _generate_tags(
        self,
        physics_terms: List[str],
        detectors: List[str],
        particles: List[str],
        has_latex: bool,
        has_code: bool
    ) -> List[str]:
        """Generate tags for the chunk."""
        tags = []
        
        if has_latex:
            tags.append("equations")
        if has_code:
            tags.append("code-example")
        
        # Add top physics terms
        tags.extend(physics_terms[:3])
        
        # Add detectors
        tags.extend(detectors[:2])
        
        # Add particles
        if particles:
            tags.append("particles")
            if "higgs" in [p.lower() for p in particles]:
                tags.append("higgs")
        
        return list(set(tags))[:8]  # Limit tags
    
    def extract_latex_blocks(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract all LaTeX blocks from text (public utility method).
        
        Args:
            text: Text to analyze
            
        Returns:
            List of dictionaries with 'type', 'content', 'start', 'end'
        """
        blocks = []
        
        for match in self._latex_display_pattern.finditer(text):
            blocks.append({
                "type": "display",
                "content": match.group(0),
                "inner": match.group(1),
                "start": match.start(),
                "end": match.end()
            })
        
        for match in self._latex_inline_pattern.finditer(text):
            blocks.append({
                "type": "inline",
                "content": match.group(0),
                "inner": match.group(1),
                "start": match.start(),
                "end": match.end()
            })
        
        blocks.sort(key=lambda b: b["start"])
        return blocks
    
    def extract_code_blocks(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract all code blocks from text (public utility method).
        
        Args:
            text: Text to analyze
            
        Returns:
            List of dictionaries with 'language', 'content', 'start', 'end'
        """
        blocks = []
        
        for match in self._code_block_pattern.finditer(text):
            blocks.append({
                "language": match.group(1) if match.group(1) else "unknown",
                "content": match.group(2),
                "full": match.group(0),
                "start": match.start(),
                "end": match.end()
            })
        
        return blocks
    
    def get_statistics(self, chunks: List[Chunk]) -> Dict[str, Any]:
        """
        Get statistics about a list of chunks.
        
        Args:
            chunks: List of chunks
            
        Returns:
            Dictionary of statistics
        """
        if not chunks:
            return {"count": 0}
        
        lengths = [len(c.text) for c in chunks]
        types = {}
        tags = {}
        latex_count = 0
        code_count = 0
        
        for chunk in chunks:
            # Count types
            ctype = chunk.metadata.chunk_type
            types[ctype] = types.get(ctype, 0) + 1
            
            # Count tags
            for tag in chunk.metadata.tags:
                tags[tag] = tags.get(tag, 0) + 1
            
            # Count features
            if chunk.metadata.has_latex:
                latex_count += 1
            if chunk.metadata.has_code:
                code_count += 1
        
        return {
            "count": len(chunks),
            "total_characters": sum(lengths),
            "avg_length": sum(lengths) / len(lengths),
            "min_length": min(lengths),
            "max_length": max(lengths),
            "types": types,
            "top_tags": dict(sorted(tags.items(), key=lambda x: -x[1])[:10]),
            "with_latex": latex_count,
            "with_code": code_count
        }
