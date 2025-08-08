"""Processing result value object."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ProcessingResult:
    """Value object for processing results."""
    success: bool
    message: str
    preview: Optional[str] = None
    error: Optional[str] = None
    
    @classmethod
    def success_result(cls, message: str, preview: Optional[str] = None) -> 'ProcessingResult':
        """Create successful result."""
        return cls(success=True, message=message, preview=preview)
    
    @classmethod
    def error_result(cls, error: str) -> 'ProcessingResult':
        """Create error result."""
        return cls(success=False, message="Processing failed", error=error)