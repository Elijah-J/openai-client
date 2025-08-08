"""Word count value object."""

from dataclasses import dataclass

from ..constants import MIN_WORD_COUNT


@dataclass(frozen=True)
class WordCount:
    """Value object for word count with validation."""
    value: int
    
    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Word count cannot be negative")
    
    def __str__(self) -> str:
        return f"{self.value:,}"
    
    def __int__(self) -> int:
        return self.value
    
    def exceeds_limit(self, limit: int) -> bool:
        """Check if word count exceeds given limit."""
        return self.value > limit