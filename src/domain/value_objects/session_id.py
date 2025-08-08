"""Session ID value object."""

from dataclasses import dataclass

from ..constants import MIN_API_KEY_DISPLAY_LENGTH


@dataclass(frozen=True)
class SessionId:
    """Value object for session ID."""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("Session ID cannot be empty")
        if len(self.value) < MIN_API_KEY_DISPLAY_LENGTH:
            raise ValueError("Session ID too short")
    
    @property
    def short(self) -> str:
        """Get shortened version for display."""
        return f"{self.value[:MIN_API_KEY_DISPLAY_LENGTH]}..."
    
    def __str__(self) -> str:
        return self.value