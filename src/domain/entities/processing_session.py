"""Processing session entity for tracking document processing."""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import uuid

from ..value_objects import WordCount, SessionId
from .document import Document
from .processed_chunk import ProcessedChunk


@dataclass
class ProcessingSession:
    """Processing session entity with rich behavior."""
    session_id: SessionId
    created_at: datetime
    document: Document
    chunks: List[ProcessedChunk] = field(default_factory=list)
    formatting_prompt: str = ""
    completed_at: Optional[datetime] = None
    
    @classmethod
    def create_new(
        cls,
        document: Document,
        formatting_prompt: str
    ) -> 'ProcessingSession':
        """Factory method to create new session."""
        return cls(
            session_id=SessionId(str(uuid.uuid4())),
            created_at=datetime.now(),
            document=document,
            formatting_prompt=formatting_prompt
        )
    
    def add_chunk(self, chunk: ProcessedChunk) -> None:
        """Add processed chunk to session."""
        self.chunks.append(chunk)
    
    def complete(self) -> None:
        """Mark session as completed."""
        self.completed_at = datetime.now()
    
    @property
    def is_completed(self) -> bool:
        """Check if session is completed."""
        return self.completed_at is not None
    
    @property
    def is_chunked(self) -> bool:
        """Check if document was processed in chunks."""
        return len(self.chunks) > 1
    
    @property
    def total_chunks(self) -> int:
        """Get total number of chunks."""
        return len(self.chunks)
    
    @property
    def total_words_processed(self) -> WordCount:
        """Get total words processed."""
        total = sum(int(chunk.word_count) for chunk in self.chunks)
        return WordCount(total)
    
    @property
    def processing_duration(self) -> Optional[float]:
        """Get processing duration in seconds."""
        if self.completed_at:
            return (self.completed_at - self.created_at).total_seconds()
        return None
    
    def get_summary(self) -> str:
        """Get session summary."""
        source = self.document.source_file or "unknown"
        chunks_info = f" in {self.total_chunks} chunks" if self.is_chunked else ""
        return f"{source}: {self.document.word_count} words{chunks_info}"
    
    def __str__(self) -> str:
        status = "completed" if self.is_completed else "in progress"
        return f"Session {self.session_id.short} ({status})"