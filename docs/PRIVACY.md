# KeyPool privacy policy

Effective date: 30 September 2026. Operator: WEN LIU.
Contact: **nextcheckin@gmail.com**.

## Scope and permitted data

This policy covers the KeyPool plugin, its MCP/API service, OAuth connection,
and generated-file delivery. Use public or non-sensitive sample data. Do not
submit confidential information, personal data, passwords, or API credentials
as tool inputs. Enter your owner-issued team token only on KeyPool's OAuth
consent page. The plugin offers no payment or public self-service enrollment.

## What is processed and why

KeyPool processes the queries, URLs, text, identifiers, and options you send to
a selected tool to execute that request. The selected provider receives the
inputs needed for that operation. Results return through KeyPool to your
connected ChatGPT, Codex, or other authorized client.

KeyPool stores account and authorization records, selected service permissions,
OAuth client/grant state, and operational usage records. Detailed usage records
include account/service/credential identifiers, method, request path, status,
latency, usage quantities where available, and request time. A request path may
contain an identifier or query information; do not put sensitive data in it.
KeyPool's usage table does not store complete request or response bodies.

Speech and subtitle tools temporarily store the resulting file and file
metadata for download. Job ownership records associate asynchronous jobs with
the account that started them. These records enforce account boundaries.

## Sharing and hosting

Cloudflare hosts the Worker, D1 database, KV state, and private R2 file storage.
The upstream provider you select processes that tool's inputs under its own
terms and data practices. ChatGPT/OpenAI or another connected client receives
the tool results and any file links returned in the conversation. Their
retention and data controls are separate from KeyPool's.

A generated file link is a temporary bearer capability: anyone possessing it
can download that file while access remains valid. Share it only with intended
recipients. KeyPool does not sell data or use the plugin to sell products.

## Retention and access

Detailed usage logs are scheduled for pruning after seven days; per-account
daily usage totals are retained indefinitely for usage tracking. Asynchronous
job ownership records expire after seven days and are removed by cleanup.

File download access expires after one hour. Expired files and metadata are
deleted by scheduled cleanup, so physical deletion may occur after link expiry.
Cleanup processes a bounded batch and may be delayed by execution failures.
Account/credential records and OAuth grants remain as needed for access and
operation until expiry, revocation, or operator-managed removal. Operational
logs or provider-held records can have separate retention periods; the
seven-day usage-table period does not promise deletion from every system.

## Requests and changes

Email the contact above to request access revocation or deletion of retained
KeyPool account-associated data. We verify account control before acting and
explain any records that must be retained. Do not include a token in the email.
Deleting KeyPool records does not delete conversations or upstream provider
records; use those services' controls for those requests.

We may update this policy as the service changes. The current version is
published with its effective date in the KeyPool plugin repository.
