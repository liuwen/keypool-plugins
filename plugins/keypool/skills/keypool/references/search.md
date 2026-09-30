# Search and extraction

Exa provides web search, similar-page discovery, and contents extraction. Tavily provides search and URL extraction. Firecrawl provides search, page scraping, and structured extraction, with job-status operations when the provider returns a job ID. These tools expose provider-specific options; consult their schemas rather than assuming parameter names are interchangeable.

Serper is the SERP provider in this plugin. Its vertical parameter selects web, images, news, maps, places, videos, shopping, scholar, patents, or autocomplete. SerpAPI is not included.

For a sourced answer, search first, inspect promising source URLs, and extract content only where useful. Cite the source URLs returned by the tools and distinguish snippets from full-page evidence. The plugin does not expose research agents, bulk crawling, or monitors.

Structured extraction can create an upstream job. Preserve its ID and use the matching Firecrawl status tool. Results are owned by the initiating KeyPool account. A missing-job error is not permission to try another account or guess IDs.
