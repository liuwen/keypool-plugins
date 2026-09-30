# KeyPool plugin

KeyPool connects Codex to search, extraction, speech, subtitle, and data services through one authenticated MCP server. The plugin bundles one KeyPool skill and service references alongside the MCP connection.

## Install in Codex

```sh
codex plugin marketplace add liuwen/keypool-plugins
codex plugin add keypool@keypool-team
```

Start a new Codex chat after installation. The MCP server is `https://keypool.whatsinfor.me/mcp`. When Codex opens KeyPool's OAuth consent page, enter your KeyPool team token **only on that page**. Do not put the token in chat, plugin files, or command arguments.

## Available services

The plugin covers 13 services and up to 44 provider tools, plus a KeyPool profile tool. The connected account sees only its authorized services and tools.

| Purpose | Services |
| --- | --- |
| Search and extraction | Exa, Tavily, Firecrawl |
| SERP | Serper |
| Speech synthesis | Cartesia, Deepgram |
| Subtitle search and download | SubDL, OpenSubtitles |
| Data and page scraping | Weatherstack, IPAPI, Aviationstack, Positionstack, Scrapestack |

The bundled `keypool` skill explains provider selection, job polling, source attribution, and private file downloads. Provider quota and plan restrictions still apply.

## Hosting and authentication

This repository is a public catalog and plugin package. It contains no credential values, Worker deployment configuration, or server runtime code. Cloudflare hosts the MCP server and OAuth consent flow. Public access to these files does not grant permission to run tools; each connection needs a valid KeyPool team token and selected service scopes.

The current package is version `0.1.1`. Its matching GitHub release also provides `keypool.zip` for Agents API plugin loading. That route requires the calling application to complete KeyPool OAuth and supply a short-lived MCP access token as `KEYPOOL_MCP_ACCESS_TOKEN`; the parent team token is not an MCP bearer token. The export format has been checked locally; a live Agents API session has not been tested. See the [Agents API plugin guide](https://developers.openai.com/api/docs/guides/agents-api/tools/plugins) for loading the ZIP.

## Update

Refresh the marketplace and reinstall the plugin to pick up a new bundle version:

```sh
codex plugin marketplace upgrade keypool-team
codex plugin remove keypool@keypool-team
codex plugin add keypool@keypool-team
```

Start a new Codex chat after updating.

## ChatGPT web

Adding this GitHub marketplace to Codex does not register a ChatGPT web plugin. A registered KeyPool MCP app can already supply tools on the web at `https://keypool.whatsinfor.me/mcp`.

To add the skill alongside that existing app, use a separate private package with the skill, its references, and a `.app.json` binding to the verified registered app ID. Its portable manifest references that file through `extensions.com.openai.apps`. This package must omit `mcp.json` and `.mcp.json`: ChatGPT marks imported packages with either MCP configuration as **Desktop only**, even for an HTTPS server. See [OpenAI's app-reference guide](https://learn.chatgpt.com/docs/enterprise/plugin-management#reference-an-existing-app-with-appjson).

The private skill package reuses the existing app's connection and permissions. Each account needs access to the referenced app and must install the skill package. Account-specific app bindings are not published in this repository. Public ChatGPT directory distribution requires separate submission and publication.
