# Skyflow plugin for Grok Bot and Cursor

This plugin connects Grok Bot and Cursor to Skyflow through the official Skyflow MCP server.

## What it contains

1. `.cursor-plugin/plugin.json` declares the `SKYFLOW_ACCOUNT_ID` variable.
2. `mcp.json` points at `https://mcp.skyflow.com/${SKYFLOW_ACCOUNT_ID}` which is the production Skyflow MCP server.
3. `skills/skyflow-connection-test` tells the agent to call `list_accounts` and to report failures precisely.

## Install in Grok Bot

1. Open Settings → Plugins.
2. Paste `https://github.com/SkyflowFoundry/grok-bot-plugin` into the **Search or Paste Link** box.
3. Select the plugin and click **Add**.
4. Enter your Skyflow account ID when Grok Bot asks for it. If it does not ask then look for a **Configure** option on the installed plugin.
5. Connect the `skyflow` server and finish the Skyflow sign-in.
6. Ask the bot to test the Skyflow connection.

## Install in Cursor for local testing

```bash
mkdir -p ~/.cursor/plugins/local
cp -R . ~/.cursor/plugins/local/skyflow
```

Then run **Developer: Reload Window** and ask the agent to test the Skyflow connection.

## Network endpoints and credentials

The plugin calls only the Skyflow MCP server. It uses OAuth and stores no credentials.
