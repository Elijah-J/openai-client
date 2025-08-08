"""Sentence boundary chunking strategy."""

import re
from typing import List

from ..entities import Document
from ..value_objects import WordLimit
from .chunking_strategy import ChunkingStrategy
from .even_distribution_chunking import EvenDistributionChunking


class SentenceBoundaryChunking(ChunkingStrategy):
    """Strategy for chunking at sentence boundaries."""
    
    def calculate_chunks_needed(self, document: Document, word_limit: WordLimit) -> int:
        """Calculate chunks needed based on sentence boundaries."""
        # Simplified implementation - in practice would be more sophisticated
        return EvenDistributionChunking().calculate_chunks_needed(document, word_limit)
    
    def chunk(self, document: Document, word_limit: WordLimit) -> List[str]:
        """Split document at sentence boundaries."""
        # Simplified implementation - would normally respect sentence boundaries
        
        if not document.requires_chunking(int(word_limit)):
            return [document.content]
        
        # Split by sentences (simple regex, could be improved)
        sentences = re.split(r'(?<=[.!?])\s+', document.content)
        
        chunks = []
        current_chunk = []
        current_word_count = 0
        limit = int(word_limit)
        
        for sentence in sentences:
            sentence_words = len(sentence.split())
            
            if current_word_count + sentence_words > limit and current_chunk:
                # Save current chunk and start new one
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_word_count = sentence_words
            else:
                current_chunk.append(sentence)
                current_word_count += sentence_words
        
        # Add remaining sentences
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks if chunks else [document.content]