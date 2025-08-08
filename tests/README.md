# Unit Tests for OpenAI Text Formatter

## Installation

Install test dependencies:
```bash
pip install -r requirements-test.txt
```

## Running Tests

### Basic test run:
```bash
python -m pytest
```

### Run with verbose output:
```bash
python -m pytest -v
```

### Run with coverage report:
```bash
python -m pytest --cov=. --cov-report=term-missing
```

### Run specific test file:
```bash
python -m pytest tests/test_config.py
```

### Run specific test:
```bash
python -m pytest tests/test_config.py::TestConfig::test_default_values
```

## Test Structure

- `test_config.py` - Tests for configuration management
- `test_file_manager.py` - Tests for file I/O operations
- `test_text_processor.py` - Tests for text processing and chunking
- `test_display_manager.py` - Tests for console output formatting
- `test_context_manager.py` - Tests for context persistence
- `test_api_client.py` - Tests for OpenAI API interaction
- `test_app.py` - Integration tests for main application
- `conftest.py` - Shared fixtures and test utilities

## Coverage

Current test coverage: 70 tests covering all public methods

To generate HTML coverage report:
```bash
python -m pytest --cov=. --cov-report=html
```
Then open `htmlcov/index.html` in your browser.