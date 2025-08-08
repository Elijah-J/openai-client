"""File path value object."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FilePath:
    """Value object for file paths with validation."""
    value: str
    must_exist: bool = False
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("File path cannot be empty")
        
        path = Path(self.value)
        if self.must_exist and not path.exists():
            raise ValueError(f"File does not exist: {self.value}")
    
    @property
    def path(self) -> Path:
        """Get Path object."""
        return Path(self.value)
    
    @property
    def exists(self) -> bool:
        """Check if file exists."""
        return self.path.exists()
    
    @property
    def name(self) -> str:
        """Get file name."""
        return self.path.name
    
    def __str__(self) -> str:
        return self.value