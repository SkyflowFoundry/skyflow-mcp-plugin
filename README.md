# Skyflow MCP plugin

This plugin connects AI agents to Skyflow through the official Skyflow Developer MCP server at `https://mcp.skyflow.com`. It targets Grok Bot and Cursor and follows the vendor-neutral [Agent Plugins](https://agent-plugins.org/specification) format so other hosts can load it too.

The plugin contains only the MCP server. Skyflow's skills live in [SkyflowFoundry/skyflow-skills](https://github.com/SkyflowFoundry/skyflow-skills) and install separately.

## Install in Grok Bot

1. Open **Settings → Plugins**.
2. Paste `https://github.com/SkyflowFoundry/skyflow-mcp-plugin` into the **Search or Paste Link** box.
3. Select **skyflow** and click **Add**.
4. Connect the `skyflow` server and sign in to Skyflow when prompted.
5. Ask the bot to list your Skyflow accounts to check the connection.

## Install in Cursor

Install from **Settings → Plugins** with the same link as Grok Bot.

To test local changes copy the repo into Cursor's local plugin folder and reload the window:

```bash
mkdir -p ~/.cursor/plugins/local
rm -rf ~/.cursor/plugins/local/skyflow
cp -R . ~/.cursor/plugins/local/skyflow
```

Then run **Developer: Reload Window**.

## Claude Code

Claude Code users should install the Skyflow MCP plugins from [SkyflowFoundry/claude](https://github.com/SkyflowFoundry/claude) for now.

## Network endpoints and credentials

The plugin calls only `https://mcp.skyflow.com`. The server uses OAuth so each user signs in with their own Skyflow account. The plugin needs no environment variables and stores no credentials.

## Files

| File | Purpose |
| ---- | ------- |
| `plugin.json` | Agent Plugins 1.0.0 manifest |
| `mcp.json` | Agent Plugins 1.0.0 MCP configuration that points at `https://mcp.skyflow.com` |
| `.cursor-plugin/marketplace.json` | Lets Cursor and Grok Bot find the plugin from the repo link. Its entry carries the logo because the Agent Plugins manifest has no logo field. |
| `assets/logo.svg` and `assets/logo.png` | Square Skyflow logo for marketplace listings |

## Validation

The **Validate manifests** workflow checks `plugin.json` and `mcp.json` against the vendored Agent Plugins schemas. It also checks that the marketplace entry matches `plugin.json` and that every MCP server points at `mcp.skyflow.com`. Run it locally with:

```bash
pip install jsonschema
python3 .github/scripts/validate-manifests.py
```

To release a new version bump `version` in `plugin.json` and `metadata.version` in `.cursor-plugin/marketplace.json` together because the check fails when they disagree.

## License

[MIT](LICENSE)
