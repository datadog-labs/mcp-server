#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["claude-agent-sdk", "ddtrace", "python-dotenv", "requests"]
# ///
"""
Agent with Datadog MCP + a custom Slack webhook tool, traced via LLM Observability.
"""

from dotenv import load_dotenv

load_dotenv()

import ddtrace.auto  # Automatically instruments supported libraries for LLM Observability

import asyncio
import os
import requests
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    ToolUseBlock,
    ToolResultBlock,
    TextBlock,
    tool,
    create_sdk_mcp_server,
)


@tool("send_slack_message", "Post a message to Slack", {"text": str})
async def send_slack_message(args):
    resp = requests.post(os.environ["SLACK_WEBHOOK_URL"], json={"text": args["text"]})
    resp.raise_for_status()
    return {"content": [{"type": "text", "text": "Message sent to Slack."}]}


async def main():
    prompt = (
        "Investigate observability data for email-service over the last hour. "
        "Look for anything an SRE on call would need to know about. "
        "If you find any ongoing issues, send a concise summary to Slack. "
        "If everything looks healthy, just say so — don't message Slack."
    )

    options = ClaudeAgentOptions(
        mcp_servers={
            "datadog": {
                "type": "http",
                "url": "https://mcp.datadoghq.com/api/unstable/mcp-server/mcp",
                "headers": {
                    "DD-API-KEY": os.environ["DD_API_KEY"],
                    "DD-APPLICATION-KEY": os.environ["DD_APPLICATION_KEY"],
                },
            },
            "slack": create_sdk_mcp_server(name="slack", tools=[send_slack_message]),
        },
        model="claude-sonnet-4-6",
        allowed_tools=["mcp__datadog__*", "mcp__slack__*"],
    )

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
