"""Ports (interfaces) for external dependencies."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from ..domain.entities import Document, FormattingContext


class TextFormatterPort(ABC):
    """Port for text formatting services."""
    
    @abstractmethod
    def format_text(self, prompt: str) -> str:
        """Format text according to prompt."""
        pass


class FileSystemPort(ABC):
    """Port for file system operations."""
    
    @abstractmethod
    def read_file(self, path: str) -> Optional[str]:
        """Read file content."""
        pass
    
    @abstractmethod
    def write_file(self, path: str, content: str, append: bool = False) -> None:
        """Write content to file."""
        pass
    
    @abstractmethod
    def clear_file(self, path: str) -> None:
        """Clear file content."""
        pass


class ContextPersistencePort(ABC):
    """Port for context persistence."""
    
    @abstractmethod
    def load_context(self) -> Optional[FormattingContext]:
        """Load saved context."""
        pass
    
    @abstractmethod
    def save_context(self, context: FormattingContext) -> None:
        """Save context."""
        pass


class UserInterfacePort(ABC):
    """Port for user interface operations."""
    
    @abstractmethod
    def show_progress(self, message: str, details: Dict[str, Any] = None) -> None:
        """Show progress to user."""
        pass
    
    @abstractmethod
    def show_result(self, message: str, preview: str = None) -> None:
        """Show result to user."""
        pass
    
    @abstractmethod
    def show_error(self, error: str) -> None:
        """Show error to user."""
        pass


class ConfigurationPort(ABC):
    """Port for configuration access."""
    
    @abstractmethod
    def get_word_limit(self) -> int:
        """Get word limit per chunk."""
        pass
    
    @abstractmethod
    def get_output_file(self) -> str:
        """Get output file path."""
        pass
    
    @abstractmethod
    def get_prompt_file(self) -> str:
        """Get prompt file path."""
        pass
    
    @abstractmethod
    def get_message_file(self) -> str:
        """Get message file path."""
        pass
    
    @abstractmethod
    def is_context_enabled(self) -> bool:
        """Check if context persistence is enabled."""
        pass