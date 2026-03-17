# Changelog

## March 17, 2026

- Fixed an issue preventing Gemini CLI from connecting to the MCP server
- Fixed a bug where `search_datadog_incidents` was not respecting time filters.
- Improved reliability of `search_datadog_events` for large result sets.

## March 16, 2026

- Added `whoami` and `toolsets` MCP resources to the `core` toolset, so agents can check which user/org is connected and which toolsets are available.

## March 13, 2026

- Fixed an issue preventing Claude Connectors (Claude web UI and Claude Desktop/Cowork) from connecting to the MCP server
- Improved `search_datadog_incidents` tool documentation: clarified commander/responder query syntax, case sensitivity, and wildcard support.

## March 11, 2026

- Replaced `search_datadog_llmobs_spans` with the improved `search_llmobs_spans` tool in the `llm-obs` toolset.
- Fixed `include_path` parameter in `get_datadog_trace` (`apm` toolset) to correctly accept a string array.

## March 10, 2026

- Improved `search_datadog_services` performance by switching to a materialized view backend.
- Fixed a bug where `analyze_datadog_logs` and other analytics tools could return empty results for longer time ranges.

## March 9, 2026

- Datadog MCP Server is now generally available!
- Improved `search_datadog_incidents` with total count, facets, sort options, and advanced query documentation.
