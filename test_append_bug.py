#!/usr/bin/env python3
"""Test to reproduce the append bug with small files."""

from pathlib import Path

# Create test files
data_dir = Path("data")
message_file = data_dir / "message.md"
output_file = data_dir / "output.md"

# Write a small message (won't need chunking)
message_file.write_text("This is a small test message that should replace the output file completely.")

# Pre-populate output file with old content
output_file.write_text("OLD CONTENT THAT SHOULD BE REPLACED\n" * 10)

print(f"Before running main.py:")
print(f"Output file size: {len(output_file.read_text())} chars")
print(f"First 50 chars: {output_file.read_text()[:50]}")

print("\nNow run: python main.py")
print("Then run this script again to see if output was replaced or appended")