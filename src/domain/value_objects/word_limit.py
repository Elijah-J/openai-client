"""Word limit value object."""

from dataclasses import dataclass

from ..constants import MIN_WORD_LIMIT, MAX_WORD_LIMIT


@dataclass(frozen=True)
class WordLimit:
    """Value object for word limit with validation."""
    value: int
    
    def __post_init__(self):
        if not MIN_WORD_LIMIT <= self.value <= MAX_WORD_LIMIT:
            raise ValueError(
                f"Word limit must be between {MIN_WORD_LIMIT} and {MAX_WORD_LIMIT}"
            )
    
    def __int__(self) -> int:
        return self.value