"""Refactored dependency injection with cleaner design."""

import os
from typing import Optional, Dict, Any

from ..application.use_cases import FormatDocumentUseCase
from .adapters import (
    OpenAIAdapter, FileSystemAdapter, JsonContextPersistence,
    ConsoleUI, Settings
)


class DependencyContainer:
    """Clean dependency injection container."""
    
    def __init__(self, config_overrides: Optional[Dict[str, Any]] = None):
        """Initialize with optional configuration overrides."""
        self.config = config_overrides or {}
        self._singletons = {}
    
    def get_use_case(self) -> FormatDocumentUseCase:
        """Get fully configured use case."""
        return FormatDocumentUseCase(
            text_formatter=self._get_text_formatter(),
            file_system=self._get_file_system(),
            context_persistence=self._get_context_persistence(),
            user_interface=self._get_user_interface(),
            configuration=self._get_configuration()
        )
    
    def _get_text_formatter(self) -> OpenAIAdapter:
        """Get or create text formatter singleton."""
        if 'text_formatter' not in self._singletons:
            from ..domain.constants import API_TIMEOUT_SECONDS
            model = os.getenv('OPENAI_MODEL', self.config.get('model', 'gpt-4'))
            timeout = self.config.get('api_timeout', API_TIMEOUT_SECONDS)
            self._singletons['text_formatter'] = OpenAIAdapter(model, timeout)
        return self._singletons['text_formatter']
    
    def _get_file_system(self) -> FileSystemAdapter:
        """Get or create file system singleton."""
        if 'file_system' not in self._singletons:
            self._singletons['file_system'] = FileSystemAdapter()
        return self._singletons['file_system']
    
    def _get_context_persistence(self) -> JsonContextPersistence:
        """Get or create context persistence singleton."""
        if 'context_persistence' not in self._singletons:
            context_file = self.config.get('context_file', 'data/context.json')
            self._singletons['context_persistence'] = JsonContextPersistence(context_file)
        return self._singletons['context_persistence']
    
    def _get_user_interface(self) -> ConsoleUI:
        """Get or create UI singleton."""
        if 'user_interface' not in self._singletons:
            verbose = self.config.get('verbose', True)
            use_color = self.config.get('use_color', True)
            self._singletons['user_interface'] = ConsoleUI(verbose, use_color)
        return self._singletons['user_interface']
    
    def _get_configuration(self) -> Settings:
        """Get or create configuration singleton."""
        if 'configuration' not in self._singletons:
            self._singletons['configuration'] = Settings(
                word_limit=self.config.get('word_limit', 2000),
                output_file=self.config.get('output_file', 'data/output.md'),
                prompt_file=self.config.get('prompt_file', 'data/prompt.md'),
                message_file=self.config.get('message_file', 'data/message.md'),
                context_enabled=self.config.get('context_enabled', True)
            )
        return self._singletons['configuration']


class ApplicationFactory:
    """Factory for creating application with different configurations."""
    
    @staticmethod
    def create_default() -> FormatDocumentUseCase:
        """Create application with default configuration."""
        container = DependencyContainer()
        return container.get_use_case()
    
    @staticmethod
    def create_with_config(config: Dict[str, Any]) -> FormatDocumentUseCase:
        """Create application with custom configuration."""
        container = DependencyContainer(config)
        return container.get_use_case()
    
    @staticmethod
    def create_for_testing() -> FormatDocumentUseCase:
        """Create application configured for testing."""
        test_config = {
            'verbose': False,
            'use_color': False,
            'context_enabled': False,
            'word_limit': 100
        }
        container = DependencyContainer(test_config)
        return container.get_use_case()