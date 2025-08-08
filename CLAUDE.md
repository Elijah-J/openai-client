# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Minimal OpenAI API client CLI tool that supports multiple input methods for prompts.

## Setup and Dependencies

```bash
# Install required dependency
pip install openai

# Set environment variables
export OPENAI_API_KEY=sk-...
export OPENAI_MODEL=gpt-5  # Optional, defaults to gpt-5
```

## Running the Application

```bash
# Direct prompt
python main.py "Your prompt here"

# From file
python main.py prompt.md

# From stdin
echo "Your prompt" | python main.py
```

## Architecture

The application consists of a single `main.py` file with three core functions:

- `get_prompt()`: Handles input from file path, command arguments, or stdin
- `extract_response_text()`: Extracts text from API response with multiple fallback strategies
- `main()`: Orchestrates the API call flow

## Response Extraction Strategy

The code attempts to extract response text through three fallback mechanisms:
1. Direct `output_text` attribute
2. Iterating through `output` array for items with type `output_text`
3. String conversion of entire response object

## Working Files

The repository includes prompt templates and input/output files that are gitignored:
- `prompt.md`: Text reformatting prompt template
- `message.md`: Input text to be processed
- `output.md`: Processed output storage