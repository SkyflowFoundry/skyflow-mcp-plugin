#!/usr/bin/env python3
"""Validate the plugin, MCP, and marketplace manifests.

- plugin.json                     Agent Plugins 1.0.0 plugin manifest
- mcp.json                        Agent Plugins 1.0.0 MCP configuration
- .cursor-plugin/marketplace.json Cursor and Grok Bot marketplace

plugin.json and mcp.json are checked against the vendored 1.0.0 schemas. The
marketplace entry must agree with plugin.json so that a version bump or new
description can't land in one place and miss the other. Every MCP server must
point at the production Skyflow host because mcp.skyflow.dev is internal.

Exit code 0 = all valid, 1 = one or more problems (details printed).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

import jsonschema

PLUGIN_DIR = Path(".")
PLUGIN = PLUGIN_DIR / "plugin.json"
MCP = PLUGIN_DIR / "mcp.json"
MARKETPLACE = Path(".cursor-plugin/marketplace.json")
SCHEMAS = {
    PLUGIN: Path(".github/schemas/agent-plugins-1.0.0-plugin.schema.json"),
    MCP: Path(".github/schemas/agent-plugins-1.0.0-mcp.schema.json"),
}
# The only MCP host this plugin may point at.
MCP_HOST = "mcp.skyflow.com"


def load(path: Path, errors: list[str]) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{path}: missing")
        return None
    except json.JSONDecodeError as e:
        errors.append(f"{path}: invalid JSON ({e})")
        return None
    if not isinstance(data, dict):
        errors.append(f"{path}: top level must be a JSON object")
        return None
    return data


def check_schema(path: Path, errors: list[str]) -> dict | None:
    schema = load(SCHEMAS[path], errors)
    data = load(path, errors)
    if schema is not None and data is not None:
        validator = jsonschema.Draft202012Validator(schema)
        for err in sorted(validator.iter_errors(data), key=str):
            where = "/".join(str(p) for p in err.absolute_path) or "(root)"
            errors.append(f"{path}: {where}: {err.message}")
    return data


def check_mcp_hosts(mcp: dict, errors: list[str]) -> None:
    for name, server in mcp.get("mcpServers", {}).items():
        url = server.get("url") if isinstance(server, dict) else None
        if not isinstance(url, str) or urlsplit(url).hostname != MCP_HOST:
            errors.append(f"{MCP}: server `{name}` must use https://{MCP_HOST}")


def check_marketplace(plugin: dict, errors: list[str]) -> None:
    market = load(MARKETPLACE, errors)
    if market is None:
        return
    entries = [p for p in market.get("plugins", []) if p.get("name") == plugin["name"]]
    if len(entries) != 1:
        errors.append(f"{MARKETPLACE}: expected one entry named `{plugin['name']}`, found {len(entries)}")
        return
    entry = entries[0]
    source = entry.get("source")
    if not isinstance(source, str) or Path(source).resolve() != PLUGIN_DIR.resolve():
        errors.append(f"{MARKETPLACE}: `{plugin['name']}` source must be `./`")
    if entry.get("description") != plugin.get("description"):
        errors.append(f"{MARKETPLACE}: `{plugin['name']}` description differs from {PLUGIN}")
    logo = entry.get("logo")
    if isinstance(logo, str) and not logo.startswith(("http://", "https://")):
        if not (PLUGIN_DIR / logo).is_file():
            errors.append(f"{MARKETPLACE}: `{plugin['name']}` logo `{logo}` not found")
    version = market.get("metadata", {}).get("version")
    if version is not None and version != plugin.get("version"):
        errors.append(f"{MARKETPLACE}: metadata.version `{version}` differs from {PLUGIN}")


def main() -> int:
    errors: list[str] = []

    plugin = check_schema(PLUGIN, errors)
    mcp = check_schema(MCP, errors)
    if mcp is not None:
        check_mcp_hosts(mcp, errors)
    if plugin is not None and isinstance(plugin.get("name"), str):
        check_marketplace(plugin, errors)

    if errors:
        print("Manifest validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"All manifests valid and in sync ({plugin['name']} {plugin.get('version')}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
