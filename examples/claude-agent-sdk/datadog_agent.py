#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["claude-agent-sdk"]
# ///
"""
Simple example of using the Claude Agent SDK to query Datadog via MCP.

Prerequisites:
- Set DD_API_KEY and DD_APPLICATION_KEY environment variables

Usage:
    ./datadog_agent.py
"""

import asyncio
import os
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    ToolUseBlock,
    ToolResultBlock,
    TextBlock,
)


async def main():
    options = ClaudeAgentOptions(
        mcp_servers={
            "datadog": {
                "type": "http",
                "url": "https://mcp.datadoghq.com/v1/mcp",
                "headers": {
                    "DD-API-KEY": os.environ["DD_API_KEY"],
                    "DD-APPLICATION-KEY": os.environ["DD_APPLICATION_KEY"],
                },
            }
        },
        model="claude-sonnet-4-6",
        allowed_tools=["mcp__datadog__*"],
    )

    prompt = "Which services are logging the most errors?"
    print(f"Prompt: {prompt}\n")

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
                        print("[Tool result received]\n")


if __name__ == "__main__":
    asyncio.run(main())
