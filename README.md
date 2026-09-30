# KeyPool plugin

KeyPool connects ChatGPT and Codex to search, extraction, speech, subtitle, and data services through one authenticated MCP server. It is operated by WEN LIU. The plugin bundles one KeyPool skill and service references alongside the MCP connection.

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

The current package is version `0.1.3`. `release.json` records its file, skill-resource, and tool-contract hashes. The release provides `keypool-portable.zip` and `keypool-agents-api.zip`. The Agents API route requires the calling application to complete KeyPool OAuth and supply a short-lived MCP access token as `KEYPOOL_MCP_ACCESS_TOKEN`; the parent team token is not an MCP bearer token. The export format has been checked locally; a live Agents API session has not been tested. See the [Agents API plugin guide](https://developers.openai.com/api/docs/guides/agents-api/tools/plugins) for loading the ZIP.

Access is distributed by the operator; there are no payments or public self-service enrollment. See [support](docs/SUPPORT.md), [privacy](docs/PRIVACY.md), and [terms](docs/TERMS.md).

## Update

Refresh the marketplace and reinstall the plugin to pick up a new bundle version:

```sh
codex plugin marketplace upgrade keypool-team
codex plugin add keypool@keypool-team
```

Start a new Codex chat after updating.

## Client architecture

| Client | Required pieces |
| --- | --- |
| ChatGPT web and native mobile | One registered KeyPool MCP app for OAuth/tools plus one private KeyPool workflows plugin for the skill/references. |
| Codex and ChatGPT desktop using the marketplace package | One KeyPool package containing the remote MCP connection and skill. |
| Agents API application | The derived Agents API ZIP and application-managed OAuth onboarding/refresh. |

Work is a ChatGPT mode. A web/mobile Work chat uses the app plus private plugin; it does not use the Codex GitHub installation. Each client keeps its own connection and installed bundle.

## ChatGPT web and mobile

Adding this GitHub marketplace to Codex does not register a ChatGPT web plugin. A registered KeyPool MCP app can already supply tools on the web at `https://keypool.whatsinfor.me/mcp`.

For an individual account, use a private plugin containing the same skill and a reference to your own registered KeyPool app:

1. Register `https://keypool.whatsinfor.me/mcp` from ChatGPT's Plugins page in developer mode. Complete OAuth on KeyPool's consent page using your operator-issued team token.
2. Open that app's details and obtain its exact app ID from the URL. An `asdk_app_...` ID is the `plugin_asdk_app_...` URL identifier with only the leading `plugin_` removed.
3. Clone this repository and build the private package with that verified ID:

   ```sh
   python3 tools/build-plugin.py --chatgpt-app-id asdk_app_YOUR_VERIFIED_ID
   ```

4. In a ChatGPT Work chat, ask Plugin Creator to create a private plugin from the generated `dist/keypool-chatgpt/keypool-workflows.zip`. Install it and select **KeyPool workflows** with an @ mention in a new chat.

The private package omits both MCP configuration files, uses an app reference, and keeps the skill and service references aligned with this release. See [OpenAI's app-reference guide](https://developers.openai.com/codex/enterprise/plugin-management).

The private skill package reuses the existing app's connection and permissions. Each account needs its own accessible app and private plugin; another person's private plugin link does not grant access. Keep the original registered app connected. Account-specific bindings are not published here.

The previous version 0.1.2 was tested in a fresh ChatGPT web Work chat: it used the updated skill guidance and called `keypool_profile` once, returning six authorized services and 15 provider tools. The owner also tested the private plugin in native ChatGPT mobile and confirmed that it worked and listed six services. These checks apply to that account and connection. To qualify another account or client version, select KeyPool workflows in a new Work chat and request `keypool_profile`; confirm the skill and actual tool result. See [OpenAI's supported plugin surfaces](https://developers.openai.com/codex/plugins).

An existing Codex marketplace installation can stay installed. It shares the canonical skill and backend with the private ChatGPT package, while each client keeps its own installation. In ChatGPT, select KeyPool workflows and keep the original KeyPool app connected as its dependency. If both variants appear in one client, select one for a chat to avoid duplicate instructions or tool choices.

Public ChatGPT directory distribution requires a separate verified publisher submission. This repository is a public, self-distributed marketplace; it is not an approved OpenAI directory listing.

## Missing services and reconnection

All 13 services, including SubDL, OpenSubtitles and the five APIlayer data/scraping services, remain in the catalog. `keypool_profile` reports the intersection of active services, current parent team-token policy and OAuth-selected service scopes. Its count excludes the profile tool and does not prove provider health or plan access.

In ChatGPT Settings, open the connected KeyPool account's **Actions → Reconnect**. Use your own operator-issued team token on KeyPool consent and check the desired service boxes; reconnect can preselect only the previous six. A shell variable may contain a restricted or shared-context token. A revoked token cannot be recovered from the database, which stores hashes; contact the operator for personal-token recovery. Never paste it in chat. Start a fresh chat and check the profile once; full access reports 13 services and 44 provider tools.

## Keeping versions aligned

Install the matching release and rebuild your private variant after a skill update. The backend uses this package's version and serves identical canonical skill resources over MCP. Maintainer checks compare every skill digest, the account-filtered tool schemas, and the server version against `release.json` before publishing marketplace changes.

Changes to MCP tool descriptions, schemas, annotations or authentication metadata require a server deployment followed by **Refresh tools** on the existing ChatGPT app and a new chat. A skill/reference change requires a new package version: refresh the Codex marketplace installation and update the existing private workflow plugin separately. Reconnection changes token/scopes. These are separate operations; GitHub releases do not automatically update an uploaded private skill. See [OpenAI metadata refresh](https://developers.openai.com/plugins/deploy/connect-chatgpt).
