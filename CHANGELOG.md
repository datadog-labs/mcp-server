# Changelog

## August 11, 2026

- `get_datadog_trace` and `aggregate_spans` (`core` toolset) now include a UI deep link in more response cases — including trace-not-found results and traces without a root span — for live (non-archive) queries.

## August 10, 2026

- `list-stale-feature-flags` and `clean-up-flag` (`feature-flags` toolset) now honor an org-level staleness-window override instead of always using a fixed 30-day cutoff when determining which flags are stale.
- `get_autonomous_system_status` (`networks` toolset) now automatically pulls in matching Network Path test run evidence when reporting a degraded autonomous system.

## August 7, 2026

- `get_datadog_metric` (`core` toolset) now includes a link to the Metrics Explorer for scalar query results, matching the link already provided for timeseries results.
- `create-feature-flag` and the allocation-sync tools (`feature-flags` toolset) now accept a future `scheduled_start` for CANARY/FEATURE_GATE allocation rollouts — previously this was rejected.

## August 6, 2026

- New `list_autonomous_system_statuses` tool (`networks` toolset) reports which autonomous systems are currently degraded across your org, without needing to name a specific AS.

## August 4, 2026

- Serverless onboarding (`onboarding` toolset) now supports Azure Container Apps as a compute target, and adds PHP as a supported runtime for GCP Cloud Run, Cloud Run functions, and Azure Container Apps.
- `search_pr_insights` (`software-delivery` toolset) now documents that an `expected` product status means results are still pending, not that nothing was found.

## July 31, 2026

- New `update_data_observability_recommendation_status` tool (`data-observability` toolset) lets you mark a Data Observability recommendation as applied or dismissed. `list_data_observability_recommendations` gained a `tag_query` argument for filtering by tags, and `get_data_observability_recommendation` now returns the recommendation's tags.
- `search_datadog_k8s_resources`, `describe_datadog_k8s_resource`, and `get_datadog_k8s_manifest` (`kubernetes` toolset) are more forgiving on the `kind` argument — accepting case variants, plurals, and kubectl shorthand (`pods`, `svc`, `deploy`), plus clearer errors listing valid kinds.
- `describe_datadog_k8s_resource` (`kubernetes` toolset) now includes container statuses, init container statuses, pod conditions, and the first failing condition's message when describing a pod.

## July 30, 2026

- Serverless onboarding (`onboarding` toolset) now provides dedicated OpenTelemetry setup guidance for GCP Cloud Run instead of the standard Datadog Agent flow.

## July 29, 2026

- `update_datadog_security_signals_triage` (`security` toolset) no longer fails with a permission-denied error when triaging by `filter_query` — it now correctly requires signals read + write permissions instead of write alone.
- `create_datadog_form`, `update_datadog_form`, `clone_datadog_form`, `get_datadog_form`, `search_datadog_forms`, and `publish_datadog_form` (`forms` toolset) now return a `form_url` field linking directly to the form in the Datadog UI.

## July 28, 2026

- `upsert_datadog_spreadsheet` (`sheets` toolset) now drops empty-content cells before saving, so creating a spreadsheet — or adding a new sheet to an existing one — no longer fails when the definition contains blank cells.
- `search_datadog_k8s_resources` (`kubernetes` toolset) accepts a new `include_deep_link` option that adds a link to the matching query in the Orchestration Explorer UI.

## July 24, 2026

- `upsert_datadog_dashboard` and `get_datadog_dashboard` (`dashboards`, `core` toolsets) now support additional widget types: Product Analytics cohort, retention, and funnel, plus Sankey and wildcard widgets.
- New Data Observability monitor annotation tools (`data-observability` toolset) for inspecting, creating/updating, and deleting annotations on data quality monitors, plus entity-aware monitor coverage.
- `list_datadog_database_optimizations` (`dbm` toolset) now supports pagination, filtering by optimization type, and sorting by estimated improvement.
- `get_datadog_spreadsheet_tab_data` (`sheets` toolset) now reads pivot tabs, in addition to table tabs.
- `search_dora_events` (`software-delivery` toolset) now returns the full event object (as YAML), so newly added fields surface automatically.

## July 23, 2026

- `get_datadog_dashboard` and `upsert_datadog_dashboard` (`dashboards`, `core` toolsets) now support dashboard tabs, including per-tab widget layout.
- Redesigned DORA aggregation: `aggregate_dora_events` (`software-delivery` toolset) now takes composable `queries` and `formulas` (like `get_datadog_metric`) instead of fixed metric types. A new `get_dora_fields` tool discovers the available measures, facets, and aggregations per DORA index.

## July 21, 2026

- `cost_recommendations` (`cost` toolset) can now be sorted by savings, risk, or level of effort.

## July 20, 2026

- `generate_monitor_message` (`alerting` toolset): the `type` parameter is now required, and unsupported monitor types return a clear error instead of failing server-side.
- Audit Trail tools (`audit-trail` toolset) now include an `audit_trail_explorer_url` in responses — a deep link into the Audit Trail Explorer scoped to the query and time window you just ran.
- Dashboard tools (`dashboards`, `core` toolsets) now read and write more template variable fields: group-by variables (`type`), a dynamic `available_values_query`, and per-data-source `data_source_mappings`.
- `get_datadog_spreadsheet_table_data` (`sheets` toolset) is deprecated in favor of `get_datadog_spreadsheet_tab_data`.

## July 16, 2026

- New feature flag onboarding tools (`feature-flags` toolset) that guide you through setting up your first flag: detecting your stack, creating a non-production flag, wiring up the SDK, and verifying it end to end.

## July 15, 2026

- `cost_recommendations` (`cost` toolset) now returns a risk level and a level-of-effort estimate for each recommendation.
- `get_datadog_security_detection_rules_schema` (`security` toolset) now includes a `rule_search_facets` section describing the facets you can search detection rules by.

## July 14, 2026

- `search_dora_deployments` is renamed to `search_dora_events` (`software-delivery` toolset) and can now retrieve pull requests in addition to deployments.

## July 13, 2026

- `get_synthetics_tests` (`synthetics` toolset) now handles Synthetics test suite public IDs gracefully instead of erroring.

## July 10, 2026

- `get_rum_summary` (`rum` toolset) now reports ANR rate (Android) and hang rate (iOS).
- New `get_datadog_spreadsheet_tab_data` tool (`sheets` toolset) for reading spreadsheet tab data.

## July 9, 2026

- New `list_datadog_database_optimizations` tool (`dbm` toolset) that lists query optimization suggestions for your databases.
- `get_datadog_dashboard` (`dashboards`, `core` toolsets) now preserves a template variable's `prefix` when it matches the variable name, fixing a round-trip issue where the prefix was lost on read then update.

## July 7, 2026

- New `get_autonomous_system_status` tool (`networks` toolset) that returns Network Path status for a given autonomous system (AS).

## July 6, 2026

- Audit Trail tools (`audit-trail` toolset) now redact large fields (asset diffs and metadata) by default to keep responses compact; pass `detailed_output: true` for the full events.
- `get_datadog_error_tracking_issue` (`error-tracking` toolset) now surfaces session replay links and trace IDs for the sampled errors on an issue.
- `get_synthetics_tests` (`synthetics` toolset) can now attach failure screenshots to browser-test results via a new `include_failure_screenshots` option.
- New Data Observability recommendations tools (`data-observability` toolset): `list_data_observability_recommendations` and `get_data_observability_recommendation`.

## July 3, 2026

- `get_datadog_error_tracking_issue` (`error-tracking` toolset) now surfaces linked GitHub pull requests for an issue, alongside the existing issue details.
- `search_datadog_events` (`core` toolset) now accepts `asc` and `desc` as aliases for the `sort` parameter (mapping to `timestamp` and `-timestamp`). These common values were previously rejected.

## July 2, 2026

- `get_datadog_metric` (`core` toolset) now accepts the `formulas` parameter when items are provided as objects (e.g. `{"formula": "query0 + query1"}`), not just as plain strings. Previously these calls were rejected.

## July 1, 2026

- New RUM retention filter write tools (`rum` toolset) for creating, updating, reordering, and deleting retention filters, complementing the existing search tool. Each write requires `confirm: true` since retention filters affect data retention and billing.
- `get_datadog_security_detection_rules` (`security` toolset) now supports requesting a subset of fields, so responses can be trimmed to just what you need.
- Standardized sorting arguments across several tools: dashboard and notebook search now take `sort` instead of `sort_by` (`dashboards`, `core` toolsets), and `search_datadog_monitors` (`core` toolset) uses `-field` for descending order instead of `field,desc`.

## June 30, 2026

- Fixed `upsert_datadog_spreadsheet` (`sheets` toolset) dropping fields (timeframe, query, schema format) on targeted updates. It now preserves the existing spreadsheet definition instead of wiping unspecified fields.

## June 29, 2026

- The `rum` toolset is now generally available. It includes tools for browsing RUM applications, managing RUM-based metrics, and retrieving RUM insights. `upsert_rum_metric` now also returns a cardinality estimate for the metric you're creating.
- `retry_datadog_ci_job` (`software-delivery` toolset) now supports retrying GitLab pipelines, in addition to the existing GitHub Actions support.
- Fixed `search_datadog_services` (`core` toolset) mishandling service or team names that contain colons, which were incorrectly parsed as `field:value` filters.

## June 26, 2026

- `explore_profiling_call_graph` (`profiling` toolset): the `service` and `family` top-level parameters have been removed. Scope by service or language family using `filter.query` instead (e.g. `service:my-svc family:java`).

## June 23, 2026

- `get_datadog_notebook` (`core` toolset) now accepts an `include_comments` parameter. When set to `true`, the response includes all comments on the notebook threaded by reply, alongside the notebook cells.

## June 22, 2026

- `manage_datadog_error_tracking_issue_comments` (`error-tracking` toolset) is now available to all users with the `error-tracking` toolset enabled. Previously required the `experimental` toolset. Supports adding, updating, and deleting comments on Error Tracking issues.
- `get_datadog_error_tracking_issue` (`error-tracking` toolset) now returns an activity timeline — the most recent comments, state changes, and assignee updates for the issue, matching what's shown in the Datadog UI.
- `create_reference_table` (`reference-tables` toolset) now supports creating empty tables without cloud storage. Pass `source: LOCAL_FILE` to create a table with no backing bucket; rows can then be added with `upsert_reference_table_rows` or `append_reference_table_rows`. Previously all tables required an S3, GCS, or Azure source.
- Fixed `search_datadog_logs` (`core` toolset) log pattern clustering returning results from live data instead of the archived snapshot when `use_log_patterns: true` was used in an archived log snapshot context.

## June 19, 2026

- New `create_notebook_comments` tool (`core` toolset) for adding comments to cells in a Datadog notebook.
- `search_datadog_error_tracking_issues` (`error-tracking` toolset) now surfaces "Did you mean?" suggestions when a search returns zero results, showing similar valid values for facet filters like `service`, `env`, and `version` so agents can correct and retry without an extra round-trip.

## June 17, 2026

- New `get_datadog_security_detection_rules` tool (`security` toolset) for listing and fetching security detection rules. This replaces the old `list_datadog_security_detection_rules` and `get_datadog_security_detection_rule` tools, which have been removed.
- `search_datadog_services` (`core` toolset) now returns both the internal service identifier (used in `service:` tag filters) and the human-readable `display_name` from the catalog, so agents can distinguish them correctly.

## June 15, 2026

- Fixed `analyze_datadog_logs` (`core` toolset) incorrectly auto-prepending `@` to column names in `extra_columns`. Column names like `kube_namespace` are now passed through as-is; grouping by tags works correctly without needing to strip or add the prefix manually.
- Four `security` toolset AppSec tools have been renamed to match Datadog naming standards: `list_security_trace_passlist` → `get_datadog_security_trace_passlist`, `upsert_security_trace_passlist` → `upsert_datadog_security_trace_passlist`, `delete_security_trace_passlist` → `delete_datadog_security_trace_passlist`, `list_datadog_security_aap_denylist` → `get_datadog_security_aap_denylist`. The old names no longer work.

## June 5, 2026

- New `upsert_reference_table_rows` tool (`reference-tables` toolset) for inserting or updating rows in a reference table by primary key. Tables with composite primary keys are not supported.
- Fixed `get_datadog_dashboard` (`dashboards` toolset) rejecting numeric integration dashboard IDs (e.g. `30584`). These IDs now resolve correctly via the integration timeboard and screenboard endpoints.
- Fixed `create_datadog_notebook` (`core` toolset) rejecting valid time spans like `2h` and `3h`. These are now accepted; unsupported values (e.g. `7d`) are coerced to the nearest valid span with a note in the response.

## June 2, 2026

- `analyze_datadog_error_tracking_errors` (`error-tracking` toolset) is now available to all users with the `error-tracking` toolset enabled. Previously it required the `experimental` toolset.

## June 1, 2026

- The `workflows` toolset is now available to HIPAA-compliant organizations.

## May 30, 2026

- `manage_datadog_error_tracking_issue_tickets` (`error-tracking` toolset) now supports creating and linking Linear tickets, in addition to Jira tickets and Datadog cases.

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
