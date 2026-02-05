# Datadog MCP Server

Datadog's managed [MCP server](https://modelcontextprotocol.io/) connects your AI agents to Datadog's observability tools and data. Query logs, metrics, traces, incidents, and more - directly from your AI-powered dev tools.

> **Note:** The MCP server is currently in Preview. [Request access here](https://www.datadoghq.com/product-preview/datadog-mcp-server/) if you haven't already.

## Quick Setup

For Claude Code (US1 [site](https://docs.datadoghq.com/getting_started/site/)):

```bash
claude mcp add --transport http datadog-mcp https://mcp.datadoghq.com/api/unstable/mcp-server/mcp
```

The MCP server should work with any standards-compliant MCP client. See the [full setup docs](https://docs.datadoghq.com/bits_ai/mcp_server/setup/) for other clients, alternative auth methods, and regional endpoints.

## Links

- [Setup docs](https://docs.datadoghq.com/bits_ai/mcp_server/setup/) - Full setup instructions, available tools, example prompts
- [Feedback form](https://docs.google.com/forms/d/e/1FAIpQLSeorvIrML3F4v74Zm5IIaQ_DyCMGqquIp7hXcycnCafx4htcg/viewform) - Share feedback or report issues
