# Search and extraction

| Provider | Operation | Input and follow-up |
| --- | --- | --- |
| Exa | `exa_search` | A query, optional search type and `numResults`; request `contents.text` only when page text is needed. |
| Exa | `exa_get_contents` | `ids` contains up to 10 Exa document IDs or page URLs; bound text with `text.maxCharacters` when using that object form. |
| Exa | `exa_find_similar` | Similar pages for one source `url`. This is a retained deprecated compatibility operation; use it only for a similarity request. |
| Tavily | `tavily_search` | A query with optional depth, topic and time range. Raw content and provider-generated answers are opt-in; neither replaces checking sources. |
| Tavily | `tavily_extract` | Up to 10 supplied URLs; optional relevance query, depth and markdown/text format. |
| Firecrawl | `firecrawl_search` | Search selected web, image or news sources; it does not start a crawl. |
| Firecrawl | `firecrawl_scrape` | One URL with requested markdown, HTML, raw HTML or links. If a job ID is returned, use `firecrawl_scrape_status`. |
| Firecrawl | `firecrawl_extract` | Up to five URLs and a prompt describing the fields to extract. If a job ID is returned, use `firecrawl_extract_status`. |
| Serper | `serper_search` | `q` is the query. Required `vertical` is one of `search` (web), `images`, `news`, `maps`, `places`, `videos`, `shopping`, `scholar`, `patents`, or `autocomplete`. |

Parameter names belong to each provider: `numResults`, `max_results`, `limit`, and `num` are not interchangeable. Use the supplied schema. For a sourced answer, inspect promising returned source URLs and retrieve full text only when useful. Cite the source page, not a fabricated search URL, and identify claims supported only by a snippet.

Firecrawl status tools take the exact returned `id` and require the initiating KeyPool team-token identity. A scrape ID must go to the scrape status tool; an extraction ID must go to the extraction status tool. Poll while pending. A missing-job error does not authorize another account or guessed IDs.

SerpAPI, research agents, bulk crawling, and monitors are outside this plugin. Scrapestack retrieves a supplied page's HTML; it is not a SERP search tool.
