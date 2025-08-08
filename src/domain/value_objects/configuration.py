"""Configuration value object."""

from dataclasses import dataclass

from ..constants import DEFAULT_WORD_LIMIT
from .word_limit import WordLimit
from .file_path import FilePath


@dataclass(frozen=True)
class Configuration:
    """Value object for application configuration."""
    word_limit: WordLimit
    prompt_file: FilePath
    message_file: FilePath
    output_file: FilePath
    context_file: FilePath
    context_enabled: bool = True
    verbose: bool = True
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> 'Configuration':
        """Create configuration from dictionary."""
        return cls(
            word_limit=WordLimit(config_dict.get('word_limit', DEFAULT_WORD_LIMIT)),
            prompt_file=FilePath(config_dict.get('prompt_file', 'data/prompt.md')),
            message_file=FilePath(config_dict.get('message_file', 'data/message.md')),
            output_file=FilePath(config_dict.get('output_file', 'data/output.md')),
            context_file=FilePath(config_dict.get('context_file', 'data/context.json')),
            context_enabled=config_dict.get('context_enabled', True),
            verbose=config_dict.get('verbose', True)
        )