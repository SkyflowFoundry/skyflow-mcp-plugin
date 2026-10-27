---
name: skyflow-connection-test
description: Check that the Skyflow MCP server is connected and signed in. Use when the user asks to test the Skyflow connection or to list their Skyflow accounts.
---

# Skyflow connection test

This skill checks that the `skyflow` MCP server from this plugin works end to end.

## Steps

1. Call the `list_accounts` tool on the `skyflow` MCP server.
2. Report the name and ID of each account that it returns.

## Report failures precisely

1. If the `skyflow` server or its tools are missing then say that the server is not connected.
2. If an error message or URL contains the literal text `${SKYFLOW_ACCOUNT_ID}` then say that the plugin variable was not resolved.
3. If the server asks for authorization or returns HTTP 401 then say that the Skyflow sign-in did not complete.
4. For any other error quote the error message exactly.
