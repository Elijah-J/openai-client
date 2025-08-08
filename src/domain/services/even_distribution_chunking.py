"""Even distribution chunking strategy."""

import math
from typing import List

from ..entities import Document
from ..value_objects import WordLimit
from .chunking_strategy import ChunkingStrategy


class EvenDistributionChunking(ChunkingStrategy):
    """Strategy for evenly distributing words across chunks."""
    
    def calculate_chunks_needed(self, document: Document, word_limit: WordLimit) -> int:
        """Calculate optimal number of chunks."""
        word_count = int(document.word_count)
        limit = int(word_limit)
        
        if word_count <= limit:
            return 1
        
        return math.ceil(word_count / limit)
    
    def chunk(self, document: Document, word_limit: WordLimit) -> List[str]:
        """Split document into evenly distributed chunks."""
        if not document.requires_chunking(int(word_limit)):
            return [document.content]
        
        words = document.content.split()
        num_chunks = self.calculate_chunks_needed(document, word_limit)
        words_per_chunk = math.ceil(len(words) / num_chunks)
        
        chunks = []
        for i in range(0, len(words), words_per_chunk):
            chunk_words = words[i:i + words_per_chunk]
            chunks.append(' '.join(chunk_words))
        
        return chunks