"""Domain services - compatibility module."""

# Import all services from their new locations for backward compatibility
from .services.chunking_strategy import ChunkingStrategy
from .services.even_distribution_chunking import EvenDistributionChunking
from .services.sentence_boundary_chunking import SentenceBoundaryChunking
from .services.text_chunking_service import TextChunkingService
from .services.prompt_builder import PromptBuilder
from .services.context_builder import ContextBuilder

__all__ = [
    'ChunkingStrategy',
    'EvenDistributionChunking',
    'SentenceBoundaryChunking',
    'TextChunkingService',
    'PromptBuilder',
    'ContextBuilder'
]