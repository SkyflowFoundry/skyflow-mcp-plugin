# Skyflow plugin for Grok Bot (test)

This is a throwaway test plugin. It checks whether Grok Bot and Cursor resolve a plugin variable inside the URL of a remote MCP server.

## What it contains

1. `.cursor-plugin/plugin.json` declares the `SKYFLOW_ACCOUNT_ID` variable.
2. `mcp.json` points at `https://mcp.skyflow.com/${SKYFLOW_ACCOUNT_ID}` which is the production Skyflow MCP server.
3. `skills/skyflow-connection-test` tells the agent to call `list_accounts` and to report failures precisely.

## Test in Grok Bot

1. Open Settings → Plugins.
2. Paste `https://github.com/SkyflowFoundry/grok-bot-plugin` into the **Search or Paste Link** box.
3. Select the plugin and click **Add**.
4. Note whether Grok Bot asks for the Skyflow account ID. If it does not ask then look for a **Configure** option on the installed plugin.
5. Connect the `skyflow` server and finish the Skyflow sign-in.
6. Ask the bot to test the Skyflow connection.

## Test in Cursor

```bash
mkdir -p ~/.cursor/plugins/local
cp -R . ~/.cursor/plugins/local/skyflow-test
```

Then run **Developer: Reload Window** and ask the agent to test the Skyflow connection.

## Network endpoints and credentials

The plugin calls only the Skyflow MCP server. It uses OAuth and stores no credentials.
