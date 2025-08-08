"""Domain entities - compatibility module."""

# Import all entities from their new locations for backward compatibility
from .entities.document import Document
from .entities.processed_chunk import ProcessedChunk
from .entities.processing_session import ProcessingSession
from .entities.formatting_context import FormattingContext

__all__ = [
    'Document',
    'ProcessedChunk',
    'ProcessingSession',
    'FormattingContext'
]