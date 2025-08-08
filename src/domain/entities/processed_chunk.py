"""Processed chunk entity for chunked text processing."""

from dataclasses import dataclass

from ..value_objects import WordCount, ChunkInfo


@dataclass(frozen=True)
class ProcessedChunk:
    """Immutable processed chunk entity."""
    content: str
    chunk_info: ChunkInfo
    word_count: WordCount
    
    @classmethod
    def create(
        cls,
        content: str,
        chunk_number: int,
        total_chunks: int
    ) -> 'ProcessedChunk':
        """Factory method to create processed chunk."""
        return cls(
            content=content,
            chunk_info=ChunkInfo(chunk_number, total_chunks),
            word_count=WordCount(len(content.split()))
        )
    
    @property
    def needs_continuation_header(self) -> bool:
        """Check if chunk needs continuation header."""
        return not self.chunk_info.is_first
    
    def __str__(self) -> str:
        return f"Chunk {self.chunk_info} ({self.word_count} words)"