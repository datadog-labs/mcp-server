#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Find candidate user-facing changes for the Datadog MCP server CHANGELOG.

The MCP monolith (`domains/mcp_services/apps/apis/mcp/main.go`) registers tool
packages from ~25 different domains, so `git log -- domains/mcp_services` alone
misses most user-facing changes. This script derives the *full* set of source
directories that back the monolith's public tool surface from the registration
table itself (authoritative, no path heuristics), joins each to its toolset(s)
and GA state, then prints candidate commits grouped by toolset for a human to
triage into changelog entries.

Scope note: only the monolith (`apps/apis/mcp`) is covered. The distributed
architecture (`mcp-main` + provider services) registers tools in shadow/split
mode during migration and is not yet what users are served, so it's
deliberately excluded. Revisit when those tools graduate to serving real
traffic.

Usage:
    # Fetch first — the detector reads origin/main by default.
    git -C ~/dd/dd-source fetch origin
    uv run scripts/changelog_candidates.py [--since YYYY-MM-DD] [--all]

    --since   Override the start date (default: most recent CHANGELOG.md date).
    --all     Don't split off likely-noise commits; show everything.
    --ref     git ref to read (default: origin/main).
    --dd-source PATH   Path to dd-source checkout (default: ~/dd/dd-source).

Note: dd-source lands PRs as merge commits and (post-July-2026 org migration)
has a history seam that breaks plain `git log --since`. This tool walks
`--first-parent --since-as-filter` to get one clean entry per PR without
silently skipping recent commits. See git_log() for details.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import NoReturn

REPO_ROOT = Path(__file__).resolve().parent.parent
CHANGELOG = REPO_ROOT / "CHANGELOG.md"

# The monolith entrypoint and the canonical toolset registry.
MAIN_GO = "domains/mcp_services/apps/apis/mcp/main.go"
REGISTRY_GO = "domains/api_platform/shared/libs/go/mcp/toolsets/registry.go"

# Commit subjects that are almost never user-facing changelog material. These
# are *split off* into a separate bucket, never silently dropped.
NOISE_RE = re.compile(
    r"("
    r"\btest\w*\b|\brefactor\w*\b|\bbazel\b|\bBUILD\b|\blint\w*\b|\bgofmt\b|"
    r"\bskeleton\b|\beval\w*\b|\bddeval\b|"
    r"\brevert\w*\b|\bbump\w*\b|\bdeps\b|\bdependenc\w*\b|"
    r"\bcodex\b|review feedback|address .*(review|comment)|"
    r"\btypo\w*\b|\bcomment\w*\b|rename var|\bclean(ed)?[ -]?up\b|"
    r"\bshadow\b|split traffic|\bmigrat\w*\b|\bwire\b"
    r")",
    re.IGNORECASE,
)

MERGE_RE = re.compile(r"^Merge\b", re.IGNORECASE)

MONTHS = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"], start=1)}


def die(msg: str) -> NoReturn:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def latest_changelog_date() -> date:
    """Parse the most recent '## Month DD, YYYY' heading in CHANGELOG.md."""
    text = CHANGELOG.read_text()
    for line in text.splitlines():
        m = re.match(r"##\s+(\w+)\s+(\d+),\s+(\d{4})", line)
        if m:
            month, day, year = m.group(1), int(m.group(2)), int(m.group(3))
            if month not in MONTHS:
                continue
            return date(year, MONTHS[month], day)
    die("could not find a '## Month DD, YYYY' heading in CHANGELOG.md")


def parse_imports(main_go: str) -> dict[str, str]:
    """Return {alias: repo-relative-dir} for every dd-source import in main.go.

    Handles both aliased (`foo "github.com/.../bar"`) and unaliased imports
    (alias defaults to the last path segment). Only dd-source paths are kept.
    """
    aliases: dict[str, str] = {}
    in_block = False
    imp_re = re.compile(
        r'^\s*(?:(?P<alias>[A-Za-z_]\w*)\s+)?"github\.com/DataDog/dd-source/(?P<path>[^"]+)"'
    )
    for line in main_go.splitlines():
        stripped = line.strip()
        if stripped.startswith("import ("):
            in_block = True
            continue
        if in_block and stripped == ")":
            break
        if not in_block:
            continue
        m = imp_re.match(line)
        if not m:
            continue
        path = m.group("path")
        alias = m.group("alias") or path.rsplit("/", 1)[-1]
        aliases[alias] = path
    return aliases


def registered_dirs(main_go: str, aliases: dict[str, str]) -> dict[str, str]:
    """Return {repo-relative-dir: alias} for every package whose Register* is
    actually called in main.go (the authoritative public tool surface)."""
    # Match RegisterTools, RegisterTool, and the many RegisterXxxTools /
    # RegisterXxxMcpTools variants (e.g. RegisterFindingsMcpTools,
    # RegisterPublicTools). mcpServer.RegisterToolsetMiddleware also matches but
    # is dropped below because its alias isn't a dd-source import.
    called = set(re.findall(r"\b([A-Za-z_]\w*)\.Register\w*Tools?\w*\s*\(", main_go))
    dirs: dict[str, str] = {}
    for alias in called:
        path = aliases.get(alias)
        if path:  # skip mcpServer.RegisterToolsetMiddleware etc.
            dirs[path] = alias
    return dirs


def parse_registry(registry_go: str) -> tuple[dict[str, str], dict[str, dict]]:
    """Parse registry.go.

    Returns:
      const_to_str: {'ToolsetCore': 'core', ...}
      ga_by_const:  {'ToolsetCore': {'isGA': True, 'clientVisible': True,
                                     'deprecated': False}, ...}
    """
    const_to_str: dict[str, str] = {}
    for m in re.finditer(r'\b(Toolset[A-Za-z0-9]+)\s*=\s*"([^"]+)"', registry_go):
        const_to_str[m.group(1)] = m.group(2)

    ga_by_const: dict[str, dict] = {}
    # Find the toolsetRegistry map body and parse each 'ToolsetX: { ... }' entry.
    start = registry_go.find("toolsetRegistry")
    body = registry_go[start:] if start != -1 else registry_go
    entry_re = re.compile(r"\b(Toolset[A-Za-z0-9]+):\s*\{(.*?)\}", re.DOTALL)
    for m in entry_re.finditer(body):
        const, inner = m.group(1), m.group(2)
        ga_by_const[const] = {
            "isGA": "isGA:" in inner and "isGA:false" not in inner.replace(" ", ""),
            "clientVisible": "clientVisible:" in inner
            and "clientVisible:false" not in inner.replace(" ", ""),
            "deprecated": "deprecated:" in inner
            and "deprecated:false" not in inner.replace(" ", ""),
        }
    return const_to_str, ga_by_const


def dir_toolsets(dd_source: Path, rel_dir: str, const_to_str: dict[str, str]) -> set[str]:
    """Toolset *strings* referenced in a dir tree.

    Resolution works in string space so package-local constants (e.g. ecs's
    `const ToolsetECS = "ecs"`, which doesn't match the canonical `ToolsetEcs`)
    still resolve. We merge any local `Toolset* = "..."` definitions found in
    the dir with the canonical registry map, then keep only consts that resolve
    to a real toolset string — so middleware identifiers like ToolsetResolver /
    ToolsetsUnion don't leak in as fake toolsets.
    """
    root = dd_source / rel_dir
    if not root.exists():
        return set()
    try:
        blob = subprocess.run(
            ["grep", "-rho", "-E",
             r'Toolset[A-Za-z0-9]+( *= *"[^"]+")?', str(root), "--include=*.go"],
            capture_output=True, text=True, check=False,
        ).stdout
    except FileNotFoundError:
        return set()

    local = dict(const_to_str)
    for m in re.finditer(r'(Toolset[A-Za-z0-9]+)\s*=\s*"([^"]+)"', blob):
        local[m.group(1)] = m.group(2)

    valid_strings = set(const_to_str.values())
    found: set[str] = set()
    for m in re.finditer(r"Toolset[A-Za-z0-9]+", blob):
        s = local.get(m.group(0))
        # Keep only if it resolves to a real registry toolset string.
        if s and s in valid_strings:
            found.add(s)
    return found


def git_log(dd_source: Path, since: date, ref: str, rel_dirs: list[str]) -> list[dict]:
    """PR-level commits since `since` touching any of rel_dirs.

    dd-source lands most PRs as merge commits (`... (#NNNN)`), with the intra-PR
    churn on side branches. We walk `--first-parent` so each PR shows up once
    with its title and the intra-PR "address review"/"cleanup" noise is dropped;
    squash-merged single-parent PRs on the mainline are included too. Crucially
    we do NOT pass --no-merges (that would drop every merge-committed PR).

    We use `--since-as-filter` rather than `--since`: the July 2026 monorepo
    migration (old org grafted under the new one) left a date/topology seam that
    makes plain `--since` prune the walk early and silently skip recent commits.
    `--since-as-filter` filters by date without stopping traversal.
    """
    fmt = "%H%x1f%h%x1f%ad%x1f%s"
    cmd = [
        "git", "-C", str(dd_source), "log", ref, "--first-parent",
        f"--since-as-filter={since.isoformat()}", f"--pretty=format:{fmt}",
        "--date=short", "--name-only", "--",
    ] + rel_dirs
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    commits: list[dict] = []
    cur: dict | None = None
    for line in out.splitlines():
        if "\x1f" in line:
            if cur:
                commits.append(cur)
            full, short, adate, subject = line.split("\x1f")
            cur = {"hash": short, "full": full, "date": adate,
                   "subject": subject, "files": []}
        elif line.strip() and cur is not None:
            cur["files"].append(line.strip())
    if cur:
        commits.append(cur)
    return commits


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dd-source", default=os.path.expanduser("~/dd/dd-source"))
    ap.add_argument("--ref", default="origin/main",
                    help="git ref to read (default origin/main; run `git fetch` first)")
    args = ap.parse_args()

    dd_source = Path(args.dd_source).expanduser()
    if not (dd_source / ".git").exists():
        die(f"dd-source not found at {dd_source}")

    since = (datetime.strptime(args.since, "%Y-%m-%d").date()
             if args.since else latest_changelog_date())

    main_go = (dd_source / MAIN_GO).read_text()
    registry_go = (dd_source / REGISTRY_GO).read_text()

    aliases = parse_imports(main_go)
    reg_dirs = registered_dirs(main_go, aliases)

    const_to_str, ga_by_const = parse_registry(registry_go)
    # Drop the "all" meta-alias; it's not a real toolset.
    const_to_str.pop("ToolsetAliasAll", None)

    # GA/client-visible status per toolset *string*.
    str_ga: dict[str, bool] = {}
    for const, info in ga_by_const.items():
        s = const_to_str.get(const)
        if s:
            str_ga[s] = bool(info["isGA"] and info["clientVisible"]
                             and not info["deprecated"])
    ga_strs = {s for s, ga in str_ga.items() if ga}

    # Resolve each registered dir -> toolset strings + whether any is GA-public.
    dir_info: dict[str, dict] = {}
    for rel_dir in reg_dirs:
        strs = sorted(dir_toolsets(dd_source, rel_dir, const_to_str))
        ga = any(s in ga_strs for s in strs)
        dir_info[rel_dir] = {"toolsets": strs, "ga": ga,
                             "alias": reg_dirs[rel_dir]}

    # Scan every registered tool dir, plus mcp_services broadly so shared
    # server/library changes (not tied to one tool) still surface.
    CORE_BUCKET = "mcp_services-core / shared server"
    scan_paths = sorted(set(reg_dirs) | {"domains/mcp_services"})
    commits = git_log(dd_source, since, args.ref, scan_paths)

    # Attribute each commit to the registered dirs it touched.
    def dirs_for_commit(files: list[str]) -> list[str]:
        hit = []
        for rel_dir in reg_dirs:
            if any(f.startswith(rel_dir + "/") or f == rel_dir for f in files):
                hit.append(rel_dir)
        return hit

    grouped: dict[str, list[tuple[dict, str]]] = defaultdict(list)
    noise: list[tuple[dict, list[str]]] = []
    seen = set()
    for c in commits:
        is_noise = bool(NOISE_RE.search(c["subject"])) or bool(MERGE_RE.match(c["subject"]))
        cdirs = dirs_for_commit(c["files"])
        # Commits with no specific tool dir but touching mcp_services shared code
        # still count — they fall into the core bucket below.
        if not cdirs and not any(
            f.startswith("domains/mcp_services/") for f in c["files"]
        ):
            continue
        if is_noise and not args.all:
            noise.append((c, cdirs))
            continue
        # Group by toolset label (union across touched tool dirs). Commits that
        # only touch shared mcp_services code land in the core bucket.
        labels = set()
        for d in cdirs:
            info = dir_info[d]
            for ts in info["toolsets"] or [f"(unresolved:{info['alias']})"]:
                labels.add(ts)
        key = ", ".join(sorted(labels)) if labels else CORE_BUCKET
        attribution = ", ".join(cdirs) if cdirs else CORE_BUCKET
        if c["full"] not in seen:
            grouped[key].append((c, attribution))
            seen.add(c["full"])

    # ---- Report -----------------------------------------------------------
    print(f"# Changelog candidates since {since.isoformat()}")
    print(f"# monolith surface: {len(reg_dirs)} registered dirs\n")

    # GA/client-visible toolsets first, then the rest, noise last. A group is
    # "GA" if ANY of its unioned toolsets is GA — not just the first label —
    # otherwise a GA change bundled with a non-GA package (e.g. skills) would be
    # mislabeled non-GA and skipped during triage.
    def is_ga_key(k: str) -> bool:
        return any(label.strip() in ga_strs for label in k.split(","))

    def sort_key(k: str) -> tuple:
        return (0 if is_ga_key(k) else 1, k.lower())

    for key in sorted(grouped, key=sort_key):
        tag = "GA" if is_ga_key(key) else "non-GA/preview?"
        print(f"## [{tag}] {key}")
        for c, cdirs in sorted(grouped[key], key=lambda x: x[0]["date"], reverse=True):
            print(f"  {c['date']}  {c['hash']}  {c['subject']}")
            print(f"           ↳ {cdirs}")
        print()

    if noise and not args.all:
        print(f"## likely-not-user-facing ({len(noise)} commits, --all to inspect)")
        for c, _ in sorted(noise, key=lambda x: x[0]["date"], reverse=True):
            print(f"  {c['date']}  {c['hash']}  {c['subject']}")
        print()

    # ---- Completeness warnings (surface blind spots loudly) ---------------
    print("## completeness checks")
    resolved_toolsets = {ts for info in dir_info.values() for ts in info["toolsets"]}
    ga_missing = sorted(ga_strs - resolved_toolsets)
    if ga_missing:
        print("  ⚠ GA/client-visible toolsets with NO registered monolith package")
        print("    (possible blind spot — tool may be distributed-only or unregistered):")
        for ts in ga_missing:
            print(f"      - {ts}")
    unresolved = sorted(d for d, i in dir_info.items() if not i["toolsets"])
    if unresolved:
        print("  ⚠ registered dirs with NO resolvable toolset (check manually):")
        for d in unresolved:
            print(f"      - {d}")
    if not ga_missing and not unresolved:
        print("  ✓ every GA toolset maps to a registered package; all dirs resolved")


if __name__ == "__main__":
    main()
