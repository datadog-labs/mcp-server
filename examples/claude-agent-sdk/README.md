# Claude Agent SDK Example

A simple Python agent using the [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk) with access to the Datadog MCP server. Requires [uv](https://docs.astral.sh/uv/) to be installed.

## Usage

```bash
export DD_API_KEY=your_api_key
export DD_APPLICATION_KEY=your_app_key

./datadog_agent.py "Is the `foo` service logging any errors I should know about in the last 24 hours?"
```
