#!/bin/bash
# Initialize data files from examples for new users

# Get the script directory and data directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DATA_DIR="$SCRIPT_DIR/../data"

echo "Initializing data files..."

# Copy example files to working files if they don't exist
if [ ! -f "$DATA_DIR/message.md" ]; then
    if [ -f "$DATA_DIR/message.example.md" ]; then
        cp "$DATA_DIR/message.example.md" "$DATA_DIR/message.md"
        echo "  ✓  Created message.md from message.example.md"
    else
        echo "  ⚠️  message.example.md not found"
    fi
else
    echo "  ✓  message.md already exists (skipping)"
fi

if [ ! -f "$DATA_DIR/output.md" ]; then
    if [ -f "$DATA_DIR/output.example.md" ]; then
        cp "$DATA_DIR/output.example.md" "$DATA_DIR/output.md"
        echo "  ✓  Created output.md from output.example.md"
    else
        echo "  ⚠️  output.example.md not found"
    fi
else
    echo "  ✓  output.md already exists (skipping)"
fi

# Check for prompt.md (should exist as it's tracked)
if [ -f "$DATA_DIR/prompt.md" ]; then
    echo "  ✓  prompt.md exists (core configuration)"
else
    echo "  ⚠️  prompt.md is missing! This file is required."
    exit 1
fi

# Create empty context.json if it doesn't exist
if [ ! -f "$DATA_DIR/context.json" ]; then
    echo "{}" > "$DATA_DIR/context.json"
    echo "  ✓  Created empty context.json"
else
    echo "  ✓  context.json exists"
fi

echo ""
echo "Data files initialized successfully!"
echo "You can now run: python main.py"