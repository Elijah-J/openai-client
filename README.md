# OpenAI Text Formatter

A robust Python application for formatting and processing text using OpenAI's API, built with Clean Architecture principles and comprehensive error handling.

## 🚀 Features

- **Clean Architecture**: Domain-driven design with clear separation of concerns
- **Smart Text Processing**: Automatic chunking for large documents with context preservation
- **Session Persistence**: Maintains formatting context across multiple runs
- **Robust Error Handling**: Comprehensive exception handling with detailed error messages
- **Extensible Design**: Easy to add new AI providers or storage backends
- **Full Test Coverage**: Unit and integration tests with pytest
- **Type Safety**: Full type hints throughout the codebase
- **Dependency Injection**: Flexible configuration and easy testing

## 📁 Project Structure

```
openai-client/
├── src/                    # Source code
│   ├── domain/            # Core business logic & entities
│   │   ├── entities.py    # Domain models (Document, ProcessedChunk, etc.)
│   │   ├── services.py    # Domain services (TextChunking, PromptBuilder)
│   │   └── value_objects.py # Value objects and enums
│   ├── application/       # Application layer
│   │   ├── ports.py       # Abstract interfaces (Ports)
│   │   ├── use_cases.py   # Business use cases
│   │   └── services.py    # Application services
│   └── infrastructure/    # External integrations
│       ├── adapters.py    # Concrete implementations (OpenAI, FileSystem)
│       ├── dependency_injection.py # DI container
│       └── exceptions.py  # Custom exception hierarchy
├── tests/                 # Test suite
│   ├── test_domain_*.py  # Domain layer tests
│   ├── test_*.py         # Other tests
│   └── conftest.py       # Test fixtures
├── data/                  # Data files (gitignored)
│   ├── prompt.md         # Formatting instructions template
│   ├── message.md        # Input text to process
│   ├── output.md         # Formatted output
│   └── context.json      # Session context persistence
├── docs/                  # Documentation
│   ├── README_ARCHITECTURE.md # Architecture details
│   └── CLAUDE.md         # AI assistant guidelines
├── scripts/              # Utility scripts
│   ├── run_tests.sh      # Unix test runner
│   └── run_tests.bat     # Windows test runner
├── main.py               # Application entry point
├── pyproject.toml        # Project configuration
├── requirements.txt      # Production dependencies
├── requirements-test.txt # Test dependencies
└── .env                  # Environment variables (create from .env.example)
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- OpenAI API key

### Setup Steps

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/openai-client.git
cd openai-client
```

2. **Create virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment**:
```bash
# Create .env file from example (if available)
cp .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-5  # Optional, defaults to gpt-4
```

5. **Initialize data files**:
```bash
# Run the initialization script to create working files from examples
python scripts/init_data.py

# Or on Unix/Linux:
chmod +x scripts/init_data.sh
./scripts/init_data.sh
```

This will:
- Copy `data/message.example.md` → `data/message.md`
- Copy `data/output.example.md` → `data/output.md`
- Create an empty `data/context.json` if needed
- Verify that `data/prompt.md` exists (core configuration file)

## 📖 Usage

### Basic Usage

Run the text formatter with default settings:
```bash
python main.py
```

The application will:
1. Load the formatting instructions from `data/prompt.md` (version-controlled configuration)
2. Load the input text from `data/message.md` (your text to format)
3. Process the text through OpenAI's API
4. Save the formatted output to `data/output.md`
5. Persist the session context to `data/context.json`

### Customizing the Prompt

Edit `data/prompt.md` to change how text is formatted. This file is tracked in git, so your formatting rules are preserved and versioned.

### Output

The formatted text will be:
- Displayed in the console
- Saved to `data/output.md`
- Session metadata saved to `data/context.json`

### Error Handling

The application provides detailed error messages for common issues:
- Missing API key
- Network errors
- Rate limiting
- Invalid input files
- API errors

## 🧪 Testing

### Run All Tests
```bash
python -m pytest
```

### Run with Coverage
```bash
python -m pytest --cov=src --cov-report=html
```

### Run Specific Test Categories
```bash
# Unit tests only
python -m pytest -m unit

# Integration tests
python -m pytest -m integration

# Domain tests
python -m pytest tests/test_domain_*.py
```

### View Coverage Report
After running tests with coverage:
```bash
open htmlcov/index.html  # On macOS
# Or navigate to htmlcov/index.html in your browser
```

## 🏗️ Architecture

This application implements Clean Architecture (Hexagonal Architecture) with three distinct layers:

### Domain Layer
- **Pure business logic** without external dependencies
- Domain entities, value objects, and domain services
- No knowledge of databases, APIs, or frameworks

### Application Layer
- **Use cases** that orchestrate domain logic
- **Ports** (interfaces) defining contracts for external services
- Application services for cross-cutting concerns

### Infrastructure Layer
- **Adapters** implementing the ports
- External service integrations (OpenAI API, file system)
- Framework-specific code and utilities

For detailed architecture documentation, see [docs/README_ARCHITECTURE.md](docs/README_ARCHITECTURE.md).

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | - | Yes |
| `OPENAI_MODEL` | Model to use | `gpt-4` | No |
| `MAX_CHUNK_SIZE` | Maximum chunk size for text processing | `3000` | No |
| `CHUNK_OVERLAP` | Overlap between chunks | `200` | No |

### Data Files

| File | Purpose | Format | Tracked in Git |
|------|---------|--------|----------------|
| `data/prompt.md` | Core formatting instructions | Markdown | ✅ Yes |
| `data/message.md` | Input text to process | Markdown | ❌ No (user data) |
| `data/output.md` | Processed output (generated) | Markdown | ❌ No (generated) |
| `data/context.json` | Session context (generated) | JSON | ❌ No (generated) |
| `data/message.example.md` | Example input template | Markdown | ✅ Yes |
| `data/output.example.md` | Output file placeholder | Markdown | ✅ Yes |

**Note**: The `prompt.md` file is version-controlled as it contains the core configuration for text formatting. Working files (`message.md`, `output.md`) are gitignored to keep user data private.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add type hints to all functions
- Write tests for new features
- Update documentation as needed
- Keep commits atomic and descriptive

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Clean Architecture principles
- Inspired by Domain-Driven Design
- Uses OpenAI's GPT models for text processing

## 📚 Further Reading

- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [OpenAI API Documentation](https://platform.openai.com/docs)