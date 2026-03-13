# Datadog MCP Server

Datadog's managed [MCP server](https://docs.datadoghq.com/bits_ai/mcp_server/) connects your AI agents to Datadog's observability tools and data. Query logs, metrics, traces, incidents, and more - directly from your AI-powered dev tools.

## Quick Setup

For Claude Code (US1 [site](https://docs.datadoghq.com/getting_started/site/)):

```bash
claude mcp add --transport http datadog https://mcp.datadoghq.com/api/unstable/mcp-server/mcp
```

Many MCP clients also support configuration in a `.mcp.json` file:

```json
{
  "mcpServers": {
    "datadog": {
      "type": "http",
      "url": "https://mcp.datadoghq.com/api/unstable/mcp-server/mcp"
    }
  }
}
```

The MCP server should work with any standards-compliant MCP client. See the [full setup docs](https://docs.datadoghq.com/bits_ai/mcp_server/setup/) for other clients, alternative auth methods, and regional endpoints.

## Automated Agent Examples

- [`examples/claude-agent-sdk/`](examples/claude-agent-sdk/) — Minimal agent using the Claude Agent SDK
- [`examples/claude-agent-sdk-advanced/`](examples/claude-agent-sdk-advanced/) — Monitoring agent that investigates issues and posts to Slack. Includes Datadog LLM Observability integration

## Links

- [Setup docs](https://docs.datadoghq.com/bits_ai/mcp_server/setup/) - Full setup instructions, available tools, example prompts
- [Feedback form](https://docs.google.com/forms/d/e/1FAIpQLSeorvIrML3F4v74Zm5IIaQ_DyCMGqquIp7hXcycnCafx4htcg/viewform) - Share feedback or report issues
