# Skyflow MCP plugin

This plugin connects AI agents to Skyflow through the official Skyflow Developer MCP server at `https://mcp.skyflow.com`. It targets Grok Bot and Cursor and follows the vendor-neutral [Agent Plugins](https://agent-plugins.org/specification) format so other hosts can load it too.

The plugin contains only the MCP server. Skyflow's skills live in [SkyflowFoundry/skyflow-skills](https://github.com/SkyflowFoundry/skyflow-skills) and install separately.

## Before you install

Enable the MCP server in your Skyflow account first because sign-in fails until you do.

1. Sign in to Skyflow.
2. Open **AI Controls** in the left nav.
3. Enable the MCP server if it is not already enabled.
4. Add the redirect URL for each host you sign in from.

| Host | Redirect URL |
| ---- | ------------ |
| Grok Bot | `https://www.cursor.com/agents/mcp/oauth/callback` |
| Cursor web and Cloud Agents | `https://www.cursor.com/agents/mcp/oauth/callback` |
| Cursor desktop | `http://localhost:8787/callback` |

Grok Bot uses the same URL as Cursor's Cloud Agents because it signs in through Cursor's connector backend. The Cursor URLs come from Cursor's [MCP documentation](https://cursor.com/docs/context/mcp).

### Other MCP clients

Other clients can connect to `https://mcp.skyflow.com` directly without this plugin. These redirect URLs come from Zuora's list of [redirect URIs by MCP client](https://docs.zuora.com/en/zuora-ai/zuora-mcp-server/zuora-mcp-server/configure-zuora-remote-mcp-server/redirect-uris-by-mcp-client) and not from each client's own docs. Check the URL your client sends if sign-in fails.

| Client | Redirect URL |
| ------ | ------------ |
| Claude.ai and Claude Desktop | `https://claude.ai/api/mcp/auth_callback` and `https://claude.com/api/mcp/auth_callback` |
| VS Code desktop | `http://127.0.0.1:33418/` |
| VS Code web | `https://vscode.dev/redirect/` |
| Gemini CLI | `http://localhost:7777/oauth/callback` |

ChatGPT generates a different callback URL for each connector so copy it from the ChatGPT connector settings.

## Install in Grok Bot

These steps follow xAI's guide to [connecting apps in Grok Bot](https://docs.x.ai/grok-bot/computer-and-apps). Once the plugin is listed in the marketplace you can install it from the catalog:

1. Open **Connect apps** from the sidebar.
2. Search for **Skyflow** and add it.
3. Choose **Authenticate** and sign in to Skyflow in the browser that opens.
4. Confirm that Skyflow appears under **Installed**.
5. Type `@` in a chat to attach Skyflow and ask the bot to list your Skyflow accounts.

Until the plugin is listed you can add the server as a custom connector:

1. Choose **Add a custom connector** at the bottom of **Connect apps**.
2. Enter `Skyflow` as the **Name** and choose **Remote HTTPS** as the **Type**.
3. Enter `https://mcp.skyflow.com` as the **Server URL** and leave the headers and OAuth fields empty.
4. Choose **Add plugin**.
5. Choose **Authenticate** if Skyflow shows **Needs auth** and then sign in to Skyflow.

You can also ask the bot to add a custom MCP server at `https://mcp.skyflow.com`. If your team admin's MCP policy blocks the server then ask the admin to allow it.

## Install in Cursor

Once the plugin is listed you can install it from the [Cursor marketplace](https://cursor.com/marketplace).

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
