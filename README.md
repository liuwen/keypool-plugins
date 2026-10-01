# KeyPool plugin

KeyPool connects ChatGPT and Codex to search, extraction, speech, subtitle, and data services through one authenticated MCP server. It is operated by WEN LIU. The plugin bundles one KeyPool skill and service references alongside the MCP connection.

## Install in Codex

```sh
codex plugin marketplace add liuwen/keypool-plugins
codex plugin add keypool@keypool-team
```

Start a new Codex chat after installation. The MCP server is `https://keypool.whatsinfor.me/mcp`. When Codex opens KeyPool's OAuth consent page, enter your KeyPool team token **only on that page**. Do not put the token in chat, plugin files, or command arguments.

## Available services

The plugin covers 13 services and up to 33 provider tools, plus a KeyPool profile tool. The connected account sees only its authorized services and tools.

| Purpose | Services |
| --- | --- |
| Search and extraction | Exa, Tavily, Firecrawl |
| SERP | Serper |
| Speech synthesis | Cartesia, Deepgram |
| Subtitle search and download | SubDL, OpenSubtitles |
| Data and page scraping | Weatherstack, IPAPI, Aviationstack, Positionstack, Scrapestack |

Weatherstack, IPAPI, Aviationstack, Positionstack and Scrapestack use **Free-tier credentials only**. Available operations are current weather, single-IP location, current flights plus reference lists, single geocoding in default JSON, and basic GET page retrieval without JavaScript rendering. Paid features are unavailable. Current provider plans publish 100 included requests per month per upstream account for non-commercial use; this does not promise a combined pool budget or remaining quota. See the bundled [data reference](plugins/keypool/skills/keypool/references/data.md) for service limits and official sources.

The bundled `keypool` skill explains provider selection, job polling, source attribution, and private file downloads. Provider quota and plan restrictions still apply.

## Hosting and authentication

This repository is a public catalog and plugin package. It contains no credential values, Worker deployment configuration, or server runtime code. Cloudflare hosts the MCP server and OAuth consent flow. Public access to these files does not grant permission to run tools; each connection needs a valid KeyPool team token and selected service scopes.

The current package is version `0.1.4`. `release.json` records its file, skill-resource, and tool-contract hashes. The release provides `keypool-portable.zip` and `keypool-agents-api.zip`. The Agents API route requires the calling application to complete KeyPool OAuth and supply a short-lived MCP access token as `KEYPOOL_MCP_ACCESS_TOKEN`; the parent team token is not an MCP bearer token. The export format has been checked locally; a live Agents API session has not been tested. See the [Agents API plugin guide](https://developers.openai.com/api/docs/guides/agents-api/tools/plugins) for loading the ZIP.

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
| ChatGPT web | One combined KeyPool cloud plugin containing the connected app, canonical skill and references. |
| ChatGPT native mobile | The same account plugin if available; qualify native skill/tool execution separately. |
| Codex and ChatGPT desktop using the marketplace package | One KeyPool package containing the remote MCP connection and skill. |
| Agents API application | The derived Agents API ZIP and application-managed OAuth onboarding/refresh. |

Work is a ChatGPT mode. Each client keeps its own connection and installed bundle.
Adding this GitHub marketplace to Codex does not install a ChatGPT web plugin.

## ChatGPT web

An account with app-package release controls can add the skill directly to its
existing registered KeyPool app:

1. Register `https://keypool.whatsinfor.me/mcp` from ChatGPT's Plugins page in
   developer mode. Complete OAuth on KeyPool consent using your operator-issued token.
2. Refresh tool metadata if needed **before** the final package upload.
3. In the existing app's details, use **More actions → Download plugin ZIP**.
   Keep that original ZIP for recovery. Read the exact native package name/version
   from `.codex-plugin/plugin.json` and app ID from `.app.json`.
4. Build the combined package using those verified values and a higher native version:

   ```sh
   python3 tools/build-plugin.py \
     --chatgpt-app-id asdk_app_YOUR_VERIFIED_ID \
     --chatgpt-base-archive /path/to/downloaded-plugin.zip \
     --chatgpt-package-name YOUR_VERIFIED_NATIVE_PACKAGE_NAME \
     --chatgpt-version NEXT_NATIVE_PACKAGE_VERSION
   ```

5. Use that same app's **Upload new version** control with the generated ZIP under
   `dist/keypool-chatgpt-cloud/`. Download it again and compare all seven files.
6. In a new Work chat, select only **keypool**, load its skill and call
   `keypool_profile` once. Check the actual skill load and granted catalog before
   uninstalling a redundant **KeyPool workflows** wrapper.

The builder preserves the app binding byte for byte and retains native presentation
and default-prompt metadata. It changes only native version/skill path and adds the
canonical skill files with app-only presentation metadata. It supports the observed
minimal app archive, rejecting other content for review. The cloud native version is
independent of canonical/backend `0.1.4`. Account-specific bindings and ZIPs are
never published here. The connection and its OAuth permissions remain unchanged.

Observed on 2026-10-01: **Refresh tools** regenerated the app's downloadable archive
as a two-file package without skills. The details page still showed Skills 1, but a
fresh chat could not load the skill. Refresh first, then restore the combined package;
verify saved bytes and actual fresh-chat execution after the final upload.

Accounts without app-package release controls can use the previous private wrapper:
`python3 tools/build-plugin.py --chatgpt-app-id asdk_app_YOUR_VERIFIED_ID`, then
create/update the private **KeyPool workflows** plugin through Plugin Creator.
Keep its registered app connected and select one skill variant per chat.
[App references](https://developers.openai.com/codex/enterprise/plugin-management)
do not grant access or register another MCP server. Arbitrary imported remote-MCP
packages have a different host support boundary.

The previous wrapper release `0.1.4` was verified in a fresh web Work chat with one
profile call, 13 services and 33 provider tools. It did not run provider operations.
The combined native package `1.0.1` was verified on 2026-10-01 after the redundant
wrapper was uninstalled: a fresh web Work chat loaded the actual bundled skill
and reference, then one profile call returned 13 services and 33 provider tools.
All seven downloaded files matched the candidate and the app binding was preserved.
No provider operations were run. Native mobile and Codex execution remain separate
from web qualification. A viewport emulation is insufficient.

Public ChatGPT directory distribution requires a separate verified publisher
submission. This repository is a public self-distributed marketplace, not an
approved OpenAI directory listing.

## Missing services and reconnection

All 13 services, including SubDL, OpenSubtitles and the five APIlayer data/scraping services, remain in the catalog. `keypool_profile` reports the intersection of active services, current parent team-token policy and OAuth-selected service scopes. Its count excludes the profile tool and does not prove provider health or plan access.

In ChatGPT Settings, open the connected KeyPool account's **Actions → Reconnect**. Use your own operator-issued team token on KeyPool consent and check the desired service boxes; reconnect can preselect only the previous six. A shell variable may contain a restricted or shared-context token. A revoked token cannot be recovered from the database, which stores hashes; contact the operator for personal-token recovery. Never paste it in chat. Start a fresh chat and check the profile once; full access reports 13 services and 33 provider tools.

Complete consent within ten minutes in the browser/profile where reconnect opened it. The form requires its secure browser cookie. If it reports that authorization was not started in this browser, or has expired/already been used, start again from **Reconnect**; do not reuse the old form or copy its URL into another browser. See [Cloudflare consent transactions](https://github.com/cloudflare/workers-oauth-provider/blob/main/docs/upstream-sign-in.md).

## Keeping versions aligned

Install the matching canonical release and rebuild the combined app package after a skill update. The backend uses this package's version and serves identical canonical skill resources over MCP. Maintainer checks compare every skill digest, the account-filtered tool schemas, and the server version against `release.json` before publishing marketplace changes.

Changes to MCP tool descriptions, schemas, annotations or authentication metadata require a server deployment followed by **Refresh tools** on the existing ChatGPT app, restoration of the combined package, and a new chat. A skill/reference change requires a new package version: refresh the Codex marketplace installation and upload the combined app package separately. Reconnection changes token/scopes. These are separate operations; GitHub releases do not automatically update an uploaded private skill. See [OpenAI metadata refresh](https://developers.openai.com/plugins/deploy/connect-chatgpt).
