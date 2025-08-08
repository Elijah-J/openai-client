#!/usr/bin/env python3
"""OpenAI API client for text formatting using markdown templates."""

import os
import sys
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


DEFAULT_MODEL = "gpt-5"
PROMPT_FILE = "prompt.md"
MESSAGE_FILE = "message.md"
OUTPUT_FILE = "output.md"


def get_fallback_input():
    """Get input from command line arguments or stdin."""
    if not sys.argv[1:]:
        return sys.stdin.read()
    
    # Check if first argument is a file
    potential_file = Path(sys.argv[1])
    if potential_file.is_file():
        return potential_file.read_text(encoding='utf-8')
    
    # Otherwise, join all arguments as prompt
    return " ".join(sys.argv[1:])


def read_file_safely(filepath):
    """Read file content if it exists, return empty string otherwise."""
    file_path = Path(filepath)
    if file_path.is_file():
        return file_path.read_text(encoding='utf-8')
    return ""


def extract_response_text(response):
    """Extract text from API response with multiple fallback strategies."""
    # Strategy 1: Direct attribute access
    if text := getattr(response, "output_text", None):
        return text
    
    # Strategy 2: Extract from output array
    output_items = getattr(response, "output", [])
    text_parts = [
        getattr(item, "content", "")
        for item in output_items
        if getattr(item, "type", "") == "output_text"
    ]
    
    if text_parts:
        return "".join(text_parts)
    
    # Strategy 3: Convert response to string
    return str(response)


def build_prompt(formatting_instructions, content):
    """Combine formatting instructions with content."""
    if formatting_instructions and content:
        return f"{formatting_instructions}\n\n---\n\n# Text to Format:\n\n{content}"
    return content or formatting_instructions


def save_and_display_output(text, output_path):
    """Save output to file and display to console."""
    output_file = Path(output_path)
    output_file.write_text(text, encoding='utf-8')
    
    print(f"Output saved to {output_file}")
    print("\n" + "="*50 + "\n")
    print(text)


def main():
    """Main application flow for text formatting."""
    # Initialize OpenAI client
    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    
    # Load formatting instructions
    formatting_prompt = read_file_safely(PROMPT_FILE)
    
    # Load content to format (with fallback to command line)
    message_content = read_file_safely(MESSAGE_FILE)
    if not message_content:
        message_content = get_fallback_input()
    
    # Build and send request
    full_prompt = build_prompt(formatting_prompt, message_content)
    response = client.responses.create(model=model, input=full_prompt)
    
    # Extract and save response
    formatted_text = extract_response_text(response)
    save_and_display_output(formatted_text, OUTPUT_FILE)


if __name__ == "__main__":
    main()