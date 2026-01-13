"""Gradio web interface for the AI Agent service."""

import asyncio
import os
from typing import List, Tuple

import gradio as gr
from dotenv import load_dotenv

from agent_service import AgentService

# Load environment variables
load_dotenv()


class UIClient:
    """Web UI client for interacting with the AI agent."""

    def __init__(self):
        """Initialize the UI client."""
        self.service = AgentService()
        self.conversation_id = "default"
        self._loop = None

    async def initialize(self):
        """Initialize the agent service."""
        await self.service.initialize()

    async def cleanup(self):
        """Cleanup resources."""
        await self.service.cleanup()

    def _get_event_loop(self):
        """Get or create event loop for async operations."""
        if self._loop is None or self._loop.is_closed():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        return self._loop

    def chat(
        self, message: str, history: List
    ) -> Tuple[str, List]:
        """Process a chat message.

        Args:
            message: User's message
            history: Chat history (list of message dicts)

        Returns:
            Tuple of (empty string to clear input, updated history)
        """
        if not message.strip():
            return "", history

        # Ensure history is a list
        if history is None:
            history = []

        # Add user message to history in Gradio 6.x format
        history.append({"role": "user", "content": message})

        # Run agent query
        loop = self._get_event_loop()
        response_text = ""

        try:
            # Collect streaming response
            async def collect_response():
                nonlocal response_text
                async for chunk in self.service.stream(
                    message, conversation_id=self.conversation_id
                ):
                    if "messages" in chunk and chunk["messages"]:
                        last_message = chunk["messages"][-1]
                        if hasattr(last_message, "content"):
                            response_text = last_message.content

            loop.run_until_complete(collect_response())

            # Add assistant response to history
            history.append({"role": "assistant", "content": response_text})

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            # Add error as assistant response
            history.append({"role": "assistant", "content": error_msg})

        return "", history

    def get_server_status(self) -> str:
        """Get formatted server status.

        Returns:
            Formatted status string
        """
        status = self.service.get_server_status()

        if not status:
            return "⚠️ No servers connected. Please check your configuration."

        lines = ["### 🔌 Connected Servers\n"]
        for server, info in status.items():
            if info.get("connected"):
                lines.append(f"**{server}** ✓")
                lines.append(f"  - Tools: {info.get('tools_count', 0)}")
                lines.append(f"  - Resources: {info.get('resources_count', 0)}")
                if info.get("tools"):
                    lines.append(f"  - Available: {', '.join(info['tools'])}")
                lines.append("")
            else:
                lines.append(f"**{server}** ✗ (disconnected)")
                lines.append("")

        return "\n".join(lines)

    def clear_conversation(self) -> Tuple[List, str]:
        """Clear conversation history.

        Returns:
            Empty history and status message
        """
        return [], "Conversation cleared!"

    def create_interface(self, initial_status: str = "") -> Tuple[gr.Blocks, dict]:
        """Create the Gradio interface.

        Args:
            initial_status: Initial server status to display

        Returns:
            Tuple of (Gradio Blocks interface, launch parameters)
        """
        # Custom CSS for better styling
        custom_css = """
        .header {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .server-status {
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            margin: 10px 0;
        }
        .examples-box {
            padding: 10px;
            background: #e8f4f8;
            border-radius: 8px;
            margin: 10px 0;
        }
        """

        with gr.Blocks(
            title="AI Agent Interface",
        ) as interface:
            # Header
            gr.HTML(
                """
                <div class="header">
                    <h1>🤖 AI Agent Interface</h1>
                    <p>Natural language interface to PostgreSQL and GitHub</p>
                </div>
                """
            )

            with gr.Row():
                # Left column - Chat interface
                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(
                        label="Conversation",
                        height=500,
                        value=[],  # Initialize with empty list for message format
                    )

                    with gr.Row():
                        msg_input = gr.Textbox(
                            label="Message",
                            placeholder="Ask me anything about your database or GitHub...",
                            lines=2,
                            scale=4,
                        )
                        send_btn = gr.Button("Send", variant="primary", scale=1)

                    with gr.Row():
                        clear_btn = gr.Button("Clear Conversation", size="sm")
                        status_msg = gr.Textbox(
                            label="Status",
                            interactive=False,
                            show_label=False,
                            scale=2,
                        )

                    # Example queries
                    with gr.Accordion("💡 Example Queries", open=False):
                        gr.Examples(
                            examples=[
                                ["List all tables in my database"],
                                ["Show me the schema of the users table"],
                                ["Count the number of records in each table"],
                                ["List my GitHub repositories"],
                                ["Show my recent GitHub activity"],
                                [
                                    "Create a GitHub issue titled 'Bug: Login not working'"
                                ],
                                [
                                    "Find all users in the database who have GitHub accounts"
                                ],
                            ],
                            inputs=msg_input,
                            label="Click an example to try it",
                        )

                # Right column - Server status and info
                with gr.Column(scale=1):
                    server_status = gr.Markdown(
                        value=initial_status or "⚠️ No server status available",
                        label="Server Status",
                    )
                    refresh_btn = gr.Button("🔄 Refresh Status", size="sm")

                    with gr.Accordion("ℹ️ About", open=True):
                        gr.Markdown(
                            """
                            ### Features
                            - **Natural Language**: Ask questions in plain English
                            - **Multi-Server**: Connects to Postgres, GitHub, and more
                            - **Smart Routing**: Agent automatically selects the right tools
                            - **Conversation Memory**: Maintains context across queries

                            ### Tips
                            - Be specific about what you want
                            - The agent will ask for confirmation before destructive operations
                            - You can reference previous responses in your queries
                            """
                        )

                    with gr.Accordion("⚙️ Configuration", open=False):
                        gr.Markdown(
                            """
                            **Servers Configured:**
                            - PostgreSQL Database
                            - GitHub API
                            - Filesystem (optional)

                            Edit `mcp_config.json` to add/remove servers.
                            """
                        )

            # Event handlers
            def submit_message(message, history):
                return self.chat(message, history)

            # Send button and Enter key
            send_btn.click(
                fn=submit_message,
                inputs=[msg_input, chatbot],
                outputs=[msg_input, chatbot],
            )

            msg_input.submit(
                fn=submit_message,
                inputs=[msg_input, chatbot],
                outputs=[msg_input, chatbot],
            )

            # Clear conversation
            clear_btn.click(
                fn=self.clear_conversation,
                outputs=[chatbot, status_msg],
            )

            # Refresh server status
            refresh_btn.click(
                fn=self.get_server_status,
                outputs=server_status,
            )

            # Startup message
            interface.load(
                lambda: "✓ Agent service ready! Start chatting below.",
                outputs=status_msg,
            )

        # Return interface and launch parameters for Gradio 6.0
        launch_params = {
            "theme": gr.themes.Soft(),
            "css": custom_css,
        }
        return interface, launch_params

    def launch(
        self,
        share: bool = False,
        server_port: int = 7860,
        server_name: str = "0.0.0.0",
    ):
        """Launch the Gradio interface.

        Args:
            share: Whether to create a public share link
            server_port: Port to run the server on
            server_name: Server name/IP to bind to
        """
        # Initialize agent service
        print("Getting event loop...", flush=True)
        loop = self._get_event_loop()
        print("Initializing agent service...", flush=True)
        loop.run_until_complete(self.initialize())
        print("Agent service initialized!", flush=True)

        # Get initial server status before creating interface
        print("Getting initial server status...", flush=True)
        try:
            initial_status = self.get_server_status()
            print(f"Initial status retrieved: {len(initial_status) if initial_status else 0} chars", flush=True)
        except Exception as e:
            print(f"Error getting server status: {e}", flush=True)
            import traceback
            traceback.print_exc()
            initial_status = f"⚠️ Error getting status: {e}"

        # Create and launch interface
        print("Creating interface...", flush=True)
        interface, launch_params = self.create_interface(initial_status=initial_status)
        print("Interface created!", flush=True)

        try:
            print(f"\n✓ Server starting on http://{server_name}:{server_port}", flush=True)
            print(f"✓ Local URL: http://localhost:{server_port}", flush=True)
            print("✓ Press Ctrl+C to stop\n", flush=True)
            print("Calling interface.launch()...", flush=True)

            interface.launch(
                share=share,
                server_port=server_port,
                server_name=server_name,
                show_error=True,
                **launch_params,
            )
            print("interface.launch() completed", flush=True)
        finally:
            # Cleanup on exit
            loop.run_until_complete(self.cleanup())


def main():
    """Launch the UI client."""
    print("🚀 Starting AI Agent UI...")
    print("📝 Loading configuration...")

    # Create and launch UI
    ui = UIClient()
    print("\n" + "="*60)
    print("🌐 Web interface starting...")
    print("="*60)
    ui.launch(
        share=False,  # Set to True to create a public link
        server_port=7860,
        server_name="0.0.0.0",  # Listen on all interfaces
    )


if __name__ == "__main__":
    main()
