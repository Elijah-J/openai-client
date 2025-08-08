#!/usr/bin/env python3
"""Initialize data files from examples for new users."""

import os
import shutil
from pathlib import Path


def init_data_files():
    """Copy example files to working files if they don't exist."""
    # Get the data directory
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data"
    
    # Define file mappings (example -> working)
    file_mappings = {
        "message.example.md": "message.md",
        "output.example.md": "output.md"
    }
    
    print("Initializing data files...")
    
    for example_file, working_file in file_mappings.items():
        example_path = data_dir / example_file
        working_path = data_dir / working_file
        
        if not example_path.exists():
            print(f"  ⚠️  Example file not found: {example_file}")
            continue
        
        if working_path.exists():
            print(f"  ✓  {working_file} already exists (skipping)")
        else:
            shutil.copy2(example_path, working_path)
            print(f"  ✓  Created {working_file} from {example_file}")
    
    # Check for prompt.md (should exist as it's tracked)
    prompt_path = data_dir / "prompt.md"
    if prompt_path.exists():
        print(f"  ✓  prompt.md exists (core configuration)")
    else:
        print(f"  ⚠️  prompt.md is missing! This file is required.")
        return False
    
    # Create empty context.json if it doesn't exist
    context_path = data_dir / "context.json"
    if not context_path.exists():
        context_path.write_text("{}")
        print(f"  ✓  Created empty context.json")
    else:
        print(f"  ✓  context.json exists")
    
    print("\nData files initialized successfully!")
    print("You can now run: python main.py")
    return True


if __name__ == "__main__":
    success = init_data_files()
    exit(0 if success else 1)