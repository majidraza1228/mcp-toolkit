#!/bin/bash

echo "Stopping MCP Toolkit..."

# Kill Python processes
pkill -9 -f "python3 run.py" 2>/dev/null
echo "✓ Stopped Python processes"

# Kill MCP server processes
pkill -9 -f "npx @modelcontextprotocol" 2>/dev/null
echo "✓ Stopped MCP server processes"

# Kill any process using port 7860
if lsof -ti:7860 > /dev/null 2>&1; then
    lsof -ti:7860 | xargs kill -9 2>/dev/null
    echo "✓ Freed port 7860"
fi

sleep 1

# Verify everything is stopped
if lsof -i :7860 > /dev/null 2>&1; then
    echo "⚠️  Warning: Port 7860 still in use"
else
    echo "✅ All processes stopped, port 7860 is free"
fi
