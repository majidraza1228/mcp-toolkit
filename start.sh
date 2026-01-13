#!/bin/bash

# MCP Toolkit Launcher
# Automatically uses the correct Python version (3.11+)

echo "🚀 Starting MCP Toolkit..."
echo ""

# Find Python 3.11+
PYTHON=""

# Check common locations for Python 3.11+
for py in python3.11 python3.12 python3.13 /usr/local/opt/python@3.11/libexec/bin/python3 /opt/homebrew/bin/python3.11; do
    if command -v "$py" &> /dev/null; then
        VERSION=$("$py" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
        MAJOR=$(echo "$VERSION" | cut -d. -f1)
        MINOR=$(echo "$VERSION" | cut -d. -f2)

        if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 11 ]; then
            PYTHON="$py"
            echo "✓ Found Python $VERSION at: $py"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "❌ Error: Python 3.11+ not found!"
    echo ""
    echo "Please install Python 3.11 or higher:"
    echo "  - macOS: brew install python@3.11"
    echo "  - Ubuntu: sudo apt install python3.11"
    echo "  - Windows: Download from python.org"
    exit 1
fi

# Run the application
echo ""
echo "▶️  Launching application..."
echo ""
"$PYTHON" run.py

