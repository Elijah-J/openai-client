"""Document entity for text processing."""

from dataclasses import dataclass
from typing import Optional

from ..value_objects import WordCount, FilePath


@dataclass(frozen=True)
class Document:
    """Immutable document entity."""
    content: str
    word_count: WordCount
    source_file: Optional[FilePath] = None
    
    @classmethod
    def from_content(cls, content: str, source_file: Optional[str] = None) -> 'Document':
        """Factory method to create document from content."""
        if not content:
            raise ValueError("Document content cannot be empty")
        
        word_count = WordCount(len(content.split()))
        file_path = FilePath(source_file) if source_file else None
        
        return cls(content=content, word_count=word_count, source_file=file_path)
    
    def requires_chunking(self, word_limit: int) -> bool:
        """Check if document needs to be chunked."""
        return self.word_count.exceeds_limit(word_limit)
    
    def __str__(self) -> str:
        source = f" from {self.source_file}" if self.source_file else ""
        return f"Document({self.word_count} words{source})"