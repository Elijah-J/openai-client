#!/usr/bin/env python3
# Minimal CLI: pip install openai && export OPENAI_API_KEY=sk-... && python gpt5.py "Your prompt"
import os
import sys
from pathlib import Path
from openai import OpenAI


def get_prompt():
    """Get prompt from file, command line arguments, or stdin."""
    if not sys.argv[1:]:
        return sys.stdin.read()
    
    # Check if first argument is a file
    potential_file = Path(sys.argv[1])
    if potential_file.is_file():
        return potential_file.read_text(encoding='utf-8')
    
    # Otherwise, join all arguments as prompt
    return " ".join(sys.argv[1:])


def extract_response_text(response):
    """Extract text from API response with fallback options."""
    # Try direct attribute
    if text := getattr(response, "output_text", None):
        return text
    
    # Try extracting from output array
    output_items = getattr(response, "output", [])
    text_parts = [
        getattr(item, "content", "")
        for item in output_items
        if getattr(item, "type", "") == "output_text"
    ]
    
    if text_parts:
        return "".join(text_parts)
    
    # Final fallback
    return str(response)


def main():
    client = OpenAI()  # uses OPENAI_API_KEY from environment
    model = os.getenv("OPENAI_MODEL", "gpt-5")
    
    prompt = get_prompt()
    response = client.responses.create(model=model, input=prompt)
    text = extract_response_text(response)
    
    print(text)


if __name__ == "__main__":
    main()