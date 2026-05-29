# Changelog

## May 29, 2026

- New `retry_datadog_ci_job` tool (`software-delivery` toolset) for queuing retries of failed GitHub Actions CI jobs.
- Fixed `search_datadog_logs` (`core` toolset) `extra_fields` matching — field names without a source prefix (e.g. `caller`) now match again and no longer need to be written as `custom.caller` or `attributes.caller`.

## May 27, 2026

- Fixed `search_datadog_metrics` (`core` toolset) returning errors for certain tag filter combinations.

## May 26, 2026

- `update_datadog_security_signals_triage` (`security` toolset) is now available to all organizations with the `security` toolset enabled.
- `create_datadog_notebook` and `edit_datadog_notebook` (`core` toolset) now accept a `tags` parameter for setting notebook tags.
- Fixed `search_datadog_service_dependencies` (`core` toolset) crashing on services with cyclic dependency graphs.
- Fixed `search_datadog_monitors` (`core` toolset) not honoring sort direction when using suffixes like `title,asc` or `title,desc`.

## May 22, 2026

- Error tracking tools (`error-tracking` toolset) now include regression metadata: `get_datadog_error_tracking_issue` includes a `regression` block (with resolved and regressed timestamps and version), and `search_datadog_error_tracking_issues` marks regressed issues with `is_regression: true`.

## May 21, 2026

- Fixed `search_datadog_services` (`core` toolset) not returning results for services whose catalog defines a custom display name.

## May 20, 2026

- New `update_datadog_error_tracking_issue` tool (`error-tracking` toolset) for updating issue state and assignee.
- Fixed incident tools (`core` toolset) producing URLs with the wrong base domain for orgs that use a custom Datadog subdomain.
- `get_datadog_metric` (`core` toolset) now defaults the `aggregator` to `avg` in scalar mode instead of returning an error when it's omitted.

## May 19, 2026

- Fixed `search_datadog_incidents` (`core` toolset) returning no results when state filters used uppercase letters (e.g. `ACTIVE`).
- `get_datadog_flaky_tests` (`software-delivery` toolset) now includes a direct link to each test's history page in Datadog.
- The daily tool-call rate limit has been removed; only burst (50 calls/10s) and monthly (50,000 calls/month) limits now apply.
- `search_datadog_metrics` (`core` toolset) now silently clamps oversized `max_tokens` values instead of returning an error.
- Fixed multi-word fuzzy search in `list_datadog_skills` (`skills` toolset) — searches like "security findings" now return results correctly.
- OAuth now accepts the `cursor-dev://` callback URI scheme, allowing Cursor IDE to complete the authorization flow.

## May 18, 2026

- New `run_network_path` tool (`networks` toolset) for triggering on-demand traceroute tests via a Private Action Runner host.

## May 15, 2026

- New `list_reference_table_rows` tool (`reference-tables` toolset) for paginating through rows in a reference table.

## May 14, 2026

- `search_datadog_monitors` (`core` toolset) now accepts an `include_tags` parameter to return monitor tags in results, with wildcard support.

## May 13, 2026

- New `get_datadog_security_filters` tool (`security` toolset) for listing and fetching Cloud SIEM security filters.

## May 12, 2026

- `get_datadog_error_tracking_issue` (`error-tracking` toolset) now includes a `suspect_commit` field when Error Tracking has identified the likely responsible commit.
- `search_datadog_error_tracking_issues` (`error-tracking` toolset) now supports filtering by issue state (e.g. `open`, `resolved`, `for_review`).
- New `update_datadog_flaky_test_states` tool (`software-delivery` toolset) for quarantining, disabling, or marking flaky tests as fixed.
- Fixed `search_datadog_logs` (`core` toolset) returning incomplete error details for log events with both application-level error fields and error-tracking metadata.

## May 11, 2026

- `edit_datadog_notebook` (`core` toolset) now supports renaming a notebook and setting template variables as metadata-only edits, without re-uploading cell content.
- `get_datadog_notebook` (`core` toolset) now returns `template_variables` and `tags`.

## May 6, 2026

- Data Streams (`data-streams` toolset) Kafka tools now return a link to the Kafka setup documentation when queried in an environment where DSM or Kafka monitoring hasn't been configured.

## May 5, 2026

- `edit_datadog_notebook` and `create_datadog_notebook` (`core` toolset) now accept the legacy `cells`-as-string format and `id` parameter, restoring compatibility for integrations that haven't yet adopted the April 21 API changes.

## May 4, 2026

- New `analyze_datadog_security_signals` tool (`security` toolset) for AI-powered batch analysis of security signals, now available to all organizations with the `security` toolset enabled.

## April 30, 2026

- Added an `omit_tools` query parameter for disabling specific tools at connection time.
- `list_reference_tables` (`reference-tables` toolset) now includes primary key info in schema output.

## April 29, 2026

- New `create_datadog_security_suppression`, `update_datadog_security_suppression`, and `delete_datadog_security_suppression` tools (`security` toolset).
- `search_datadog_metrics` (`core` toolset) now returns up to 1,000 results per query (up from a much smaller cap) and produces more reliable results for historical time ranges.
- Error tracking tools (`error-tracking` toolset) now return human-readable display names for issue states (e.g., "In Progress" instead of `INPROGRESS`).
- OAuth now supports CORS for the `datadoghq.eu` domain so EU-based browser clients can complete the auth flow.

## April 27, 2026

- Log search tools (`core` toolset) now expose `span_id` and `trace_id` in detailed and TSV output, enabling log-to-trace navigation.

## April 24, 2026

- `search_datadog_logs` (`core` toolset) now accepts a `pattern_group_by` parameter for grouping log patterns by a field.
- `create_datadog_notebook` (`core` toolset) now tolerates invalid notebook names instead of failing.
- Renamed `security_signals_schema` to `datadog_security_signals_schema` (`security` toolset).

## April 23, 2026

- `get_datadog_metric` (`core` toolset) now supports scalar queries and structured query inputs.
- New `get_datadog_security_signal` tool (`security` toolset) for fetching individual security signals.
- Aggregate tools (`aggregate_rum_events`, `aggregate_spans`, `aggregate_events` in `core` toolset) now surface dropped compute outputs when responses are truncated.

## April 22, 2026

- `append_reference_table_rows` (`reference-tables` toolset) now requires both read and write permissions on reference tables.

## April 21, 2026

- Notebook tools (`core` toolset): the `cells` argument is now an array of structured cells (previously a string), and the notebook ID parameter was renamed from `id` to `notebook_id`.

## April 20, 2026

- `search_datadog_error_tracking_issues` (`error-tracking` toolset) now supports filtering by assignee.

## April 19, 2026

- Aggregate tools (`aggregate_rum_events`, `aggregate_spans`, `aggregate_events` in `core` toolset) now support response flattening, token budgets, and pagination for large result sets.

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
