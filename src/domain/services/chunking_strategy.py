"""Abstract base class for chunking strategies."""

from abc import ABC, abstractmethod
from typing import List

from ..entities import Document
from ..value_objects import WordLimit


class ChunkingStrategy(ABC):
    """Abstract base class for chunking strategies."""
    
    @abstractmethod
    def chunk(self, document: Document, word_limit: WordLimit) -> List[str]:
        """Chunk document according to strategy."""
        pass
    
    @abstractmethod
    def calculate_chunks_needed(self, document: Document, word_limit: WordLimit) -> int:
        """Calculate number of chunks needed."""
        pass