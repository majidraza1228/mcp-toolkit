"""Launch script for the Python full-stack MCP application."""

import os
import sys
import asyncio
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def check_environment():
    """Check if required environment variables are set."""
    required_vars = ["DATABASE_URL", "GITHUB_TOKEN"]
    llm_vars = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GROQ_API_KEY"]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    # Check if at least one LLM API key is present
    has_llm_key = any(os.getenv(var) for var in llm_vars)

    if missing_vars or not has_llm_key:
        print("❌ Missing required environment variables!\n")

        if missing_vars:
            print("Required variables:")
            for var in missing_vars:
                print(f"  - {var}")

        if not has_llm_key:
            print("\nLLM API Key (at least one required):")
            for var in llm_vars:
                print(f"  - {var}")

        print("\n📝 Please create a .env file with the required variables.")
        print("   You can copy .env.example and fill in your values:")
        print("   cp .env.example .env\n")
        return False

    return True


def check_config_file():
    """Check if MCP configuration file exists."""
    config_file = Path("mcp_config.json")
    if not config_file.exists():
        print("❌ MCP configuration file not found!")
        print("   Expected: mcp_config.json")
        print("\n📝 Please create mcp_config.json with your server configurations.\n")
        return False
    return True


def check_node_installed():
    """Check if Node.js is installed (required for MCP servers)."""
    import subprocess

    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            print(f"✓ Node.js installed: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    print("❌ Node.js not found!")
    print("   MCP servers require Node.js to run.")
    print("   Please install from: https://nodejs.org/\n")
    return False


async def test_mcp_servers():
    """Test connection to MCP servers."""
    print("\n🔍 Testing MCP server connections...")

    try:
        from utils import MCPManager

        manager = MCPManager()
        print("Initializing MCP manager...", flush=True)
        await manager.initialize()
        print("MCP manager initialized!", flush=True)

        print("Getting server status...", flush=True)
        status = manager.get_server_status()
        print("\n✓ Successfully connected to MCP servers:")
        for server, info in status.items():
            print(f"  - {server}: {info.get('tools_count', 0)} tools available")

        print("Cleaning up MCP manager...", flush=True)
        await manager.cleanup()
        print("Cleanup complete!", flush=True)
        return True

    except Exception as e:
        print(f"\n❌ Failed to connect to MCP servers: {e}")
        print("\nTroubleshooting:")
        print("  1. Check that Node.js is installed")
        print("  2. Verify mcp_config.json is correct")
        print("  3. Ensure environment variables are set")
        print("  4. Try running servers manually:")
        print("     npx @modelcontextprotocol/server-postgres $DATABASE_URL")
        print("     npx @modelcontextprotocol/server-github\n")
        return False


def print_banner():
    """Print application banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          🤖  Python Full-Stack MCP Application  🚀           ║
║                                                              ║
║  AI Agent + PostgreSQL + GitHub via MCP Protocol            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def main():
    """Main entry point."""
    print_banner()

    # Pre-flight checks
    print("🔍 Running pre-flight checks...\n")

    if not check_node_installed():
        sys.exit(1)

    if not check_environment():
        sys.exit(1)

    if not check_config_file():
        sys.exit(1)

    # Test MCP server connections
    try:
        print("About to test MCP servers...", flush=True)
        success = asyncio.run(test_mcp_servers())
        print(f"Test completed with success={success}", flush=True)
        if not success:
            print("\n⚠️  MCP server connection failed.")
            response = input("Continue anyway? (y/N): ")
            if response.lower() != 'y':
                sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user")
        sys.exit(0)

    # Launch UI
    print("\n" + "="*60, flush=True)
    print("🚀 Launching web interface...", flush=True)
    print("="*60 + "\n", flush=True)

    try:
        print("Importing ui_client...", flush=True)
        from ui_client import main as launch_ui
        print("Calling launch_ui()...", flush=True)
        launch_ui()
        print("launch_ui() returned", flush=True)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"\n❌ Error launching UI: {e}", flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
