# Development Guidelines for Claude Code

This file provides comprehensive guidance to Claude Code (claude.ai/code) and other AI assistants when working with this repository.

## 🎯 Project Overview

**OpenAI Text Formatter** - A production-ready Python application that processes and formats text using OpenAI's API, built with Clean Architecture principles for maintainability and scalability.

### Key Characteristics
- Clean Architecture implementation with strict separation of concerns
- Domain-driven design with clear business logic isolation
- Comprehensive error handling and logging
- Full test coverage with pytest
- Type-safe with complete type hints
- Extensible design supporting multiple AI providers

## 🏗️ Architecture Guidelines

### Follow Clean Architecture Principles
- **Domain Layer**: Keep pure Python, no external dependencies
- **Application Layer**: Orchestrate domain and infrastructure, define ports
- **Infrastructure Layer**: Implement adapters for external services

### Dependency Rules
- Dependencies must point inward (Infrastructure → Application → Domain)
- Domain layer must never import from other layers
- Use dependency injection for loose coupling

### File Organization
```
src/
├── domain/          # Business logic ONLY
├── application/     # Use cases and ports
└── infrastructure/  # External integrations
```

## 💻 Development Workflow

### Before Making Changes

1. **Understand the Context**
   ```bash
   # Review the architecture
   cat docs/README_ARCHITECTURE.md
   
   # Check existing tests
   python -m pytest tests/ -v
   
   # Verify current functionality
   python main.py
   ```

2. **Check Environment**
   ```bash
   # Ensure .env file exists
   test -f .env || echo "Create .env file first!"
   
   # Verify dependencies
   pip list | grep -E "openai|pytest|python-dotenv"
   ```

### When Adding Features

1. **Start with Domain Layer**
   - Define entities and value objects first
   - Implement domain services with business rules
   - Write domain tests immediately

2. **Define Ports in Application Layer**
   ```python
   # src/application/ports.py
   class NewFeaturePort(ABC):
       @abstractmethod
       def do_something(self, param: str) -> Result:
           pass
   ```

3. **Implement Adapters in Infrastructure**
   ```python
   # src/infrastructure/adapters.py
   class NewFeatureAdapter(NewFeaturePort):
       def do_something(self, param: str) -> Result:
           # Implementation
           pass
   ```

4. **Wire Dependencies**
   ```python
   # src/infrastructure/dependency_injection.py
   container.register('new_feature', NewFeatureAdapter())
   ```

### When Modifying Code

1. **Run Tests First**
   ```bash
   python -m pytest tests/ -v
   ```

2. **Follow Existing Patterns**
   - Match the code style in surrounding files
   - Use similar naming conventions
   - Maintain consistent error handling

3. **Update Tests**
   - Add unit tests for new functionality
   - Update integration tests if interfaces change
   - Maintain > 90% coverage for domain layer

4. **Validate Changes**
   ```bash
   # Run all tests
   python -m pytest
   
   # Check coverage
   python -m pytest --cov=src --cov-report=term-missing
   
   # Run the application
   python main.py
   ```

## 🧪 Testing Guidelines

### Test Structure
```python
# tests/test_domain_services.py
def test_service_behavior():
    # Arrange
    service = DomainService()
    
    # Act
    result = service.process(input_data)
    
    # Assert
    assert result.is_valid()
```

### Test Categories
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Domain Tests**: Pure logic tests without dependencies

### Running Tests
```bash
# All tests
python -m pytest

# Specific file
python -m pytest tests/test_domain_entities.py

# With coverage
python -m pytest --cov=src --cov-report=html

# Verbose output
python -m pytest -v

# Stop on first failure
python -m pytest -x
```

## 📝 Code Style Guidelines

### Python Standards
- Follow PEP 8
- Use type hints for all functions
- Docstrings for public methods
- Keep functions under 20 lines
- Maximum line length: 100 characters

### Naming Conventions
- **Classes**: PascalCase (e.g., `TextProcessor`)
- **Functions**: snake_case (e.g., `process_text`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_CHUNK_SIZE`)
- **Private**: Leading underscore (e.g., `_internal_method`)

### Import Organization
```python
# Standard library
import os
import sys
from typing import List, Optional

# Third-party
import pytest
from openai import OpenAI

# Local - Domain
from src.domain.entities import Document
from src.domain.services import TextChunkingService

# Local - Application
from src.application.ports import TextProcessorPort

# Local - Infrastructure
from src.infrastructure.adapters import OpenAIAdapter
```

## 🔒 Security Guidelines

### API Keys
- Never commit API keys
- Use environment variables
- Document required keys in README
- Provide .env.example template

### Error Messages
- Don't expose sensitive information
- Log detailed errors internally
- Return generic messages to users

### Input Validation
- Validate all external inputs
- Sanitize file paths
- Check file sizes before processing

## 🚀 Common Tasks

### Add New AI Provider
```python
# 1. Create adapter in src/infrastructure/adapters.py
class AnthropicAdapter(TextProcessorPort):
    def process_text(self, prompt: str, text: str) -> ProcessingResult:
        # Implementation
        pass

# 2. Register in dependency injection
container.register('text_processor', AnthropicAdapter())

# 3. Add tests
def test_anthropic_adapter():
    adapter = AnthropicAdapter()
    result = adapter.process_text("prompt", "text")
    assert result.success
```

### Add New Storage Backend
```python
# 1. Implement StoragePort
class S3Adapter(StoragePort):
    def save(self, key: str, data: Any) -> None:
        # S3 implementation
        pass

# 2. Wire in container
container.register('storage', S3Adapter())
```

### Debug Issues
```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use breakpoints
import pdb; pdb.set_trace()

# Check environment
print(f"API Key present: {'OPENAI_API_KEY' in os.environ}")
```

## 🔧 Troubleshooting

### Common Issues

1. **Missing API Key**
   ```bash
   # Check if set
   echo $OPENAI_API_KEY
   
   # Set temporarily
   export OPENAI_API_KEY=sk-...
   ```

2. **Import Errors**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt
   
   # Check Python path
   python -c "import sys; print(sys.path)"
   ```

3. **Test Failures**
   ```bash
   # Run specific test with verbose output
   python -m pytest tests/test_file.py::test_name -vv
   
   # Check test fixtures
   python -m pytest --fixtures
   ```

## 📊 Performance Considerations

### Optimization Guidelines
- Chunk large texts efficiently
- Cache API responses when appropriate
- Use async operations for I/O bound tasks
- Profile before optimizing

### Monitoring
```python
# Time operations
import time
start = time.time()
# operation
print(f"Took {time.time() - start:.2f}s")

# Memory usage
import tracemalloc
tracemalloc.start()
# operation
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory: {current / 10**6:.1f} MB")
```

## 🌟 Best Practices

### Do's
- ✅ Write tests first (TDD)
- ✅ Keep domain logic pure
- ✅ Use dependency injection
- ✅ Handle errors gracefully
- ✅ Document complex logic
- ✅ Follow SOLID principles

### Don'ts
- ❌ Put business logic in adapters
- ❌ Import infrastructure in domain
- ❌ Use global state
- ❌ Ignore test failures
- ❌ Commit without testing
- ❌ Mix concerns in single class

## 📚 Resources

### Documentation
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Pytest Documentation](https://docs.pytest.org/)

### Project Files
- `README.md` - User documentation
- `docs/README_ARCHITECTURE.md` - Architecture details
- `tests/README.md` - Testing documentation
- `requirements.txt` - Dependencies

## 🎯 Quick Reference

### File Paths
```python
# Data files
PROMPT_FILE = "data/prompt.md"
MESSAGE_FILE = "data/message.md"
OUTPUT_FILE = "data/output.md"
CONTEXT_FILE = "data/context.json"

# Test fixtures
FIXTURES_DIR = "tests/fixtures/"
```

### Environment Variables
```bash
OPENAI_API_KEY=sk-...        # Required
OPENAI_MODEL=gpt-4           # Optional (default: gpt-4)
MAX_CHUNK_SIZE=3000          # Optional (default: 3000)
CHUNK_OVERLAP=200            # Optional (default: 200)
```

### Commands
```bash
# Run application
python main.py

# Run tests
python -m pytest

# Check coverage
python -m pytest --cov=src

# Format code (if black installed)
black src/ tests/

# Type checking (if mypy installed)
mypy src/
```

## 🤝 Contributing Checklist

Before submitting changes:
- [ ] All tests pass
- [ ] Coverage maintained/improved
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No hardcoded values
- [ ] Error handling in place
- [ ] Type hints added
- [ ] Commits are atomic and descriptive