"""Shared pytest fixtures and test configuration."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_text_short():
    """Provide short sample text for testing."""
    return "This is a short sample text for testing purposes."


@pytest.fixture
def sample_text_long():
    """Provide long sample text for testing."""
    return " ".join(["word"] * 3000)  # 3000 words


@pytest.fixture
def sample_markdown():
    """Provide sample markdown content."""
    return """# Sample Document

This is a **sample** markdown document with:
- Bullet points
- *Italic text*
- [Links](https://example.com)

## Section 2
More content here."""


@pytest.fixture
def mock_api_response():
    """Create mock API response object."""
    response = MagicMock()
    response.output_text = "Formatted text from API"
    return response


@pytest.fixture
def mock_config():
    """Create mock configuration object."""
    config = MagicMock()
    config.model = "gpt-4"
    config.prompt_file = "prompt.md"
    config.message_file = "message.md"
    config.output_file = "output.md"
    config.context_file = "context.json"
    config.word_limit = 2000
    config.preview_length = 300
    config.separator_width = 60
    config.maintain_context = True
    config.max_context_length = 2000
    return config


@pytest.fixture
def sample_context():
    """Provide sample context data."""
    return {
        "session_id": "test-session-123",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T12:00:00",
        "total_chunks_processed": 5,
        "total_words_processed": 2500,
        "processing_history": [
            {
                "timestamp": "2024-01-01T10:00:00",
                "message_file": "test1.md",
                "word_count": 1000,
                "chunks_processed": 2,
                "summary": "First test"
            },
            {
                "timestamp": "2024-01-01T11:00:00",
                "message_file": "test2.md",
                "word_count": 1500,
                "chunks_processed": 3,
                "summary": "Second test"
            }
        ],
        "last_prompt_used": "Format this text",
        "custom_instructions": "Use formal tone",
        "conversation_summary": "Previous formatting session"
    }


@pytest.fixture
def mock_openai_client():
    """Create mock OpenAI client."""
    client = MagicMock()
    client.responses.create.return_value = MagicMock(output_text="Mocked API response")
    return client


# Removed problematic fixture that was causing test errors