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

This GitHub marketplace installs the plugin in Codex. ChatGPT web needs separate registration of the plugin with its skill packaging or publication through the ChatGPT public directory. Adding this GitHub marketplace does not make ChatGPT web load it automatically. The MCP endpoint for that separate integration is `https://keypool.whatsinfor.me/mcp`.
