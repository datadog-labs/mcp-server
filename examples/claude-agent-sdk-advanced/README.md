# Monitoring Agent Example

A Python agent that connects to the Datadog MCP server, investigates observability data, and posts findings to Slack via a custom tool. Uses [Datadog LLM Observability](https://docs.datadoghq.com/llm_observability/) to trace the entire agent interaction. Requires [uv](https://docs.astral.sh/uv/) to be installed.

## Prerequisites

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

You'll need:
- `DD_API_KEY` and `DD_APPLICATION_KEY` — your [Datadog API and application keys](https://docs.datadoghq.com/account_management/api-app-keys/)
- `SLACK_WEBHOOK_URL` — a [Slack incoming webhook](https://api.slack.com/messaging/webhooks) URL
- The `DD_LLMOBS_*` variables (to enable LLM Observability tracing)

## Usage

```bash
./datadog_agent.py
```
