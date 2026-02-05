#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["claude-agent-sdk"]
# ///
"""
Simple example of using the Claude Agent SDK to query Datadog via MCP.

Prerequisites:
- Set DD_API_KEY and DD_APPLICATION_KEY environment variables

Usage:
    uv run datadog_agent.py "Is the `foo` service logging any errors I should know about in the last 24 hours?"
    uv run datadog_agent.py  # Uses default prompt
"""

import asyncio
import os
import sys
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    ToolUseBlock,
    ToolResultBlock,
    TextBlock,
)


async def main():
    # Get prompt from args or use default
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = "Which services are logging the most errors?"

    # Check for required env vars
    api_key = os.environ.get("DD_API_KEY")
    app_key = os.environ.get("DD_APPLICATION_KEY")
    if not api_key or not app_key:
        print("Error: DD_API_KEY and DD_APPLICATION_KEY environment variables are required")
        sys.exit(1)

    options = ClaudeAgentOptions(
        mcp_servers={
            "datadog": {
                "type": "http",
                "url": "https://mcp.datadoghq.com/api/unstable/mcp-server/mcp",
                "headers": {
                    "DD-API-KEY": api_key,
                    "DD-APPLICATION-KEY": app_key,
                },
            }
        },
        model="claude-sonnet-4-5-20250929",
        allowed_tools=["mcp__datadog__*"],
    )

    print(f"Prompt: {prompt}\n")
    print("-" * 60)

    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt)

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)
                    elif isinstance(block, ToolUseBlock):
                        print(f"\n[Tool call: {block.name}]")
                    elif isinstance(block, ToolResultBlock):
                        print(f"[Tool result received]\n")


if __name__ == "__main__":
    asyncio.run(main())
