"""Domain value objects - compatibility module."""

# Import all value objects from their new locations for backward compatibility
from .value_objects.word_count import WordCount
from .value_objects.word_limit import WordLimit
from .value_objects.chunk_info import ChunkInfo
from .value_objects.file_path import FilePath
from .value_objects.session_id import SessionId
from .value_objects.processing_result import ProcessingResult
from .value_objects.configuration import Configuration

__all__ = [
    'WordCount',
    'WordLimit', 
    'ChunkInfo',
    'FilePath',
    'SessionId',
    'ProcessingResult',
    'Configuration'
]