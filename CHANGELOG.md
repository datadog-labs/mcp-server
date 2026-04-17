# Changelog

## April 17, 2026

- The `ddsql` toolset is now generally available.
- `search_datadog_logs` (`core` toolset) now accepts a `clustering_pattern_field` argument to cluster logs by a specific field.

## April 16, 2026

- `get_datadog_error_tracking_issue` (`error-tracking` toolset) now includes an `impact` field.
- Log search and analysis tools (`core` toolset) now return helpful timeout messages instead of opaque errors.

## April 15, 2026

- `aggregate_rum_events`, `aggregate_spans`, and `aggregate_events` (`core` toolset) now support percentile aggregation.
- `create_datadog_notebook` (`core` toolset) can now create private notebooks.
- Security signals tools (`security` toolset) now support filtering by `event_tracker_id`.
- The `whoami` MCP resource (`core` toolset) now includes `user_uuid`.
- Date-only ISO 8601 strings (e.g., `2026-04-15`) are now parsed as midnight UTC.

## April 13, 2026

- The `kubernetes` toolset is now generally available.
- The `reference-tables` toolset is now generally available.
- Improved `analyze_security_findings` (`security` toolset) tool documentation.

## April 9, 2026

- The `dashboards` toolset is now generally available.
- Notebook create/edit tools (`core` toolset) unified around the raw API cell format and now support general widget types.

## April 7, 2026

- `search_datadog_notebooks` (`core` toolset) now accepts `count` and `include_facets` parameters.
- `search_datadog_service_dependencies` (`core` toolset) now defaults to `downstream` direction.
- Removed unused boolean filter parameters from `search_datadog_metrics` (`core` toolset).

## April 6, 2026

- Fixed `search_datadog_monitors` (`core` toolset) sort parameter validation.

## April 3, 2026

- Fixed a pagination bug in `search_datadog_service_dependencies` (`core` toolset) that could return incomplete results.

## April 2, 2026

- `search_datadog_metrics` (`core` toolset) now searches over the last 2 weeks by default, up from 1 hour.
- The OAuth consent screen is now more user-friendly; now shows OAuth client names instead of IDs.

## March 31, 2026

- A new `submit_mcp_feedback` tool (`core` toolset) has been added – agents can use it to tell us about bugs and missing features.

## March 30, 2026

- Aggregate tools (`aggregate_rum_events`, `aggregate_events`, `aggregate_spans`) have been added to the `core` toolset to help agents reason about large numbers of items in aggregate.

## March 27, 2026

- Added `toolsets=all` shorthand that expands to all generally-available toolsets.
- Reduced token usage of `core` toolset tool definitions by ~15%.

## March 24, 2026

- Fixed an issue preventing ChatGPT from connecting to the MCP server.

## March 19, 2026

- Added `aggregate_rum_events`, `aggregate_events`, and `aggregate_spans` tools to the new `aggregation` toolset for computing metrics, counts, and groupings over RUM events, events, and spans. (This toolset is experimental — these tools will likely move to other toolsets in the future.)

## March 18, 2026

- `get_datadog_trace` and `search_datadog_spans` (`apm` toolset) now include deep links to the trace view in Datadog, so agents can share direct URLs instead of constructing them.
- Fixed a bug where month-based relative time ranges (e.g., `now-2M`) were silently interpreted as minutes.

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
