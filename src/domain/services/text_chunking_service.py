"""Text chunking service with strategy pattern."""

from typing import List, Optional

from ..entities import Document
from ..value_objects import WordLimit
from .chunking_strategy import ChunkingStrategy
from .even_distribution_chunking import EvenDistributionChunking


class TextChunkingService:
    """Service for chunking text documents with strategy pattern."""
    
    def __init__(self, strategy: Optional[ChunkingStrategy] = None):
        """Initialize with chunking strategy."""
        self.strategy = strategy or EvenDistributionChunking()
    
    def set_strategy(self, strategy: ChunkingStrategy) -> None:
        """Change chunking strategy at runtime."""
        self.strategy = strategy
    
    def calculate_chunks_needed(self, document: Document, word_limit: WordLimit) -> int:
        """Delegate to strategy."""
        return self.strategy.calculate_chunks_needed(document, word_limit)
    
    def chunk_document(self, document: Document, word_limit: WordLimit) -> List[str]:
        """Delegate to strategy."""
        return self.strategy.chunk(document, word_limit)