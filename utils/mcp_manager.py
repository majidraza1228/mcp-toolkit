"""MCP Client Manager for handling connections to multiple MCP servers."""

import os
import json
import asyncio
from typing import Any, Dict, List, Optional
from pathlib import Path

from mcp_use import MCPClient


class MCPManager:
    """Manages MCP client connections and provides utility methods."""

    def __init__(self, config_path: str = "mcp_config.json"):
        """Initialize the MCP manager.

        Args:
            config_path: Path to MCP configuration file
        """
        self.config_path = config_path
        self.client: Optional[MCPClient] = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the MCP client and create sessions."""
        if self._initialized:
            return

        # Load configuration and substitute environment variables
        config = self._load_config()
        config = self._substitute_env_vars(config)

        # Create client from config
        self.client = MCPClient.from_dict(config)

        # Create sessions with all configured servers
        await self.client.create_all_sessions()

        self._initialized = True
        print(f"✓ Connected to {len(self.client.sessions)} MCP servers")

    async def cleanup(self) -> None:
        """Close all MCP server connections."""
        if self.client and self._initialized:
            await self.client.close_all_sessions()
            self._initialized = False
            print("✓ Closed all MCP server connections")

    def _load_config(self) -> Dict[str, Any]:
        """Load MCP configuration from file.

        Returns:
            Configuration dictionary

        Raises:
            FileNotFoundError: If config file doesn't exist
        """
        config_file = Path(self.config_path)
        if not config_file.exists():
            raise FileNotFoundError(
                f"MCP config file not found: {self.config_path}\n"
                "Please create mcp_config.json with your server configurations."
            )

        with open(config_file) as f:
            return json.load(f)

    def _substitute_env_vars(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Substitute environment variables in configuration.

        Args:
            config: Raw configuration dictionary

        Returns:
            Configuration with environment variables substituted
        """
        config_str = json.dumps(config)

        # Replace ${VAR_NAME} with environment variable values
        for key in os.environ:
            placeholder = f"${{{key}}}"
            if placeholder in config_str:
                config_str = config_str.replace(placeholder, os.environ[key])

        return json.loads(config_str)

    def get_available_servers(self) -> List[str]:
        """Get list of connected server names.

        Returns:
            List of server names
        """
        if not self.client or not self._initialized:
            return []

        return list(self.client.sessions.keys())

    async def get_available_tools(self, server: Optional[str] = None) -> Dict[str, List[Dict]]:
        """Get available tools from servers.

        Args:
            server: Optional server name to get tools from. If None, gets from all servers.

        Returns:
            Dictionary mapping server names to their tools
        """
        if not self.client or not self._initialized:
            return {}

        tools_by_server = {}

        if server:
            session = self.client.get_session(server)
            if session:
                tools_by_server[server] = session.list_tools()
        else:
            for server_name in self.client.sessions:
                session = self.client.get_session(server_name)
                if session:
                    tools_by_server[server_name] = session.list_tools()

        return tools_by_server

    async def call_tool(
        self,
        server: str,
        tool: str,
        arguments: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Call a tool on a specific server directly (no LLM).

        Args:
            server: Server name
            tool: Tool name
            arguments: Tool arguments

        Returns:
            Tool execution result
        """
        if not self.client or not self._initialized:
            raise RuntimeError("MCPManager not initialized. Call initialize() first.")

        session = self.client.get_session(server)
        if not session:
            raise ValueError(f"Server '{server}' not found")

        result = await session.call_tool(name=tool, arguments=arguments or {})
        return result

    async def get_resource(self, server: str, uri: str) -> Any:
        """Get a resource from a specific server.

        Args:
            server: Server name
            uri: Resource URI

        Returns:
            Resource content
        """
        if not self.client or not self._initialized:
            raise RuntimeError("MCPManager not initialized. Call initialize() first.")

        session = self.client.get_session(server)
        if not session:
            raise ValueError(f"Server '{server}' not found")

        result = await session.read_resource(uri=uri)
        return result

    def get_server_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all connected servers.

        Returns:
            Dictionary with server status information
        """
        if not self.client or not self._initialized:
            return {}

        status = {}
        for server_name in self.client.sessions:
            session = self.client.get_session(server_name)
            if session:
                tools = session.list_tools()
                resources = session.list_resources()
                status[server_name] = {
                    "connected": True,
                    "tools_count": len(tools),
                    "resources_count": len(resources),
                    "tools": [t.get("name", "unknown") for t in tools],
                }
            else:
                status[server_name] = {"connected": False}

        return status


# Singleton instance for easy access
_manager_instance: Optional[MCPManager] = None


def get_mcp_manager(config_path: str = "mcp_config.json") -> MCPManager:
    """Get or create the global MCPManager instance.

    Args:
        config_path: Path to MCP configuration file

    Returns:
        MCPManager instance
    """
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = MCPManager(config_path)
    return _manager_instance
