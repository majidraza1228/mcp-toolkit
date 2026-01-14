#!/bin/bash

echo "Starting MCP Toolkit..."

# Use Python 3.11
PYTHON=/usr/local/bin/python3.11

if [ ! -f "$PYTHON" ]; then
    echo "❌ Error: Python 3.11 not found at $PYTHON"
    echo "   Please install Python 3.11 or update the PYTHON variable in this script"
    exit 1
fi

# Start the application
$PYTHON run.py > /tmp/mcp_app.log 2>&1 &
APP_PID=$!

echo "Waiting for server to start..."

# Wait up to 20 seconds for the server to start
for i in {1..20}; do
    sleep 1
    if lsof -i :7860 > /dev/null 2>&1; then
        echo ""
        echo "✅ Server started successfully!"
        echo ""
        echo "🌐 Open in your browser: http://localhost:7860"
        echo ""
        echo "📋 Logs: tail -f /tmp/mcp_app.log"
        echo "⏹️  Stop: ./stop.sh"
        exit 0
    fi
    echo -n "."
done

echo ""
echo "❌ Server did not start within 20 seconds"
echo "Check the logs: tail -20 /tmp/mcp_app.log"
exit 1
