#!/usr/bin/env python3
"""Debug script to trace the append issue."""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.infrastructure.dependency_injection import ApplicationFactory
from src.infrastructure.adapters import FileSystemAdapter

# Setup
load_dotenv()
Path("data/message.md").write_text("Small test content")
Path("data/output.md").write_text("OLD CONTENT THAT SHOULD BE REPLACED\n" * 3)

print("Initial output.md content:")
print(Path("data/output.md").read_text())
print("-" * 40)

# Test the file system adapter directly
fs = FileSystemAdapter()

print("\n1. Testing clear_file:")
fs.clear_file("data/output.md")
content_after_clear = Path("data/output.md").read_text()
print(f"   Content after clear: '{content_after_clear}' (length: {len(content_after_clear)})")

print("\n2. Testing write_file with append=False:")
fs.write_file("data/output.md", "NEW CONTENT", append=False)
content_after_write = Path("data/output.md").read_text()
print(f"   Content after write: '{content_after_write}'")

print("\n3. Testing write_file with append=True:")
fs.write_file("data/output.md", " APPENDED", append=True)
content_after_append = Path("data/output.md").read_text()
print(f"   Content after append: '{content_after_append}'")

# Reset for actual test
Path("data/output.md").write_text("OLD CONTENT THAT SHOULD BE REPLACED\n" * 3)

print("\n" + "=" * 40)
print("Now testing actual use case...")
print("=" * 40)

# Get the use case
use_case = ApplicationFactory.create_default()

# Monkey-patch to add logging
original_prepare = use_case.output_writer.prepare_output_file
original_write = use_case.output_writer.write_chunk

def logged_prepare(output_file):
    print(f"\n>>> prepare_output_file called for: {output_file}")
    result = original_prepare(output_file)
    content = Path(str(output_file)).read_text()
    print(f"    After prepare, file content: '{content}' (length: {len(content)})")
    return result

def logged_write(output_file, content, append=False):
    print(f"\n>>> write_chunk called with append={append}")
    print(f"    Writing {len(content)} chars")
    result = original_write(output_file, content, append)
    file_content = Path(str(output_file)).read_text()
    print(f"    After write, file has {len(file_content)} chars")
    return result

use_case.output_writer.prepare_output_file = logged_prepare
use_case.output_writer.write_chunk = logged_write

# Run
try:
    result = use_case.execute()
    print(f"\nResult: {result.success}")
    
    final_content = Path("data/output.md").read_text()
    print(f"\nFinal output.md content ({len(final_content)} chars):")
    print(final_content[:200] + "..." if len(final_content) > 200 else final_content)
    
    if "OLD CONTENT" in final_content:
        print("\n[X] BUG CONFIRMED: Old content was not replaced!")
    else:
        print("\n[OK] Working correctly: Old content was replaced")
        
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()