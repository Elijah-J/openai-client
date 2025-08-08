"""Chunk information value object."""

from dataclasses import dataclass
from typing import Tuple

from ..constants import MIN_CHUNK_NUMBER, MIN_TOTAL_CHUNKS


@dataclass(frozen=True)
class ChunkInfo:
    """Value object for chunk information."""
    current: int
    total: int
    
    def __post_init__(self):
        if self.current < MIN_CHUNK_NUMBER:
            raise ValueError(f"Current chunk must be at least {MIN_CHUNK_NUMBER}")
        if self.current > self.total:
            raise ValueError("Current chunk cannot exceed total chunks")
        if self.total < MIN_TOTAL_CHUNKS:
            raise ValueError(f"Total chunks must be at least {MIN_TOTAL_CHUNKS}")
    
    @property
    def is_first(self) -> bool:
        """Check if this is the first chunk."""
        return self.current == MIN_CHUNK_NUMBER
    
    @property
    def is_last(self) -> bool:
        """Check if this is the last chunk."""
        return self.current == self.total
    
    @property
    def is_single(self) -> bool:
        """Check if there's only one chunk."""
        return self.total == MIN_TOTAL_CHUNKS
    
    @property
    def needs_continuation_header(self) -> bool:
        """Check if this chunk needs a continuation header."""
        return not self.is_first and not self.is_single
    
    def as_tuple(self) -> Tuple[int, int]:
        """Convert to tuple for compatibility."""
        return (self.current, self.total)
    
    def __str__(self) -> str:
        return f"{self.current}/{self.total}"