The idea of the game is to see how quickly you can find the page for Adolf Hitler from any other page on wikipedia.

## Rules

- You may only follow links in the **body** of the article (i.e. paragraph text).
- Links in the **sidebar** (infoboxes, navigation boxes) are not allowed.
- Links in the **references section** at the bottom of the article are not allowed.

## Design Considerations

### Algorithm & Search Strategy
- Bidirectional BFS is preferred over standard BFS — search forward from source and backward from Hitler simultaneously, meeting in the middle. Reduces nodes visited from O(b^d) to O(b^(d/2)).
- Standard BFS finds the shortest path; bidirectional BFS finds it much faster.
- A visited set is required in each direction. Care is needed to correctly detect when the two frontiers meet.
- Need a clear policy for when no path is found within the depth limit.

### API Usage
- Prefer `prop=links` via the MediaWiki API over fetching and parsing full HTML — returns structured JSON of all internal links on a page.
- Use `list=backlinks` to get pages that link to Hitler, for the backward BFS frontier.
- Respect Wikipedia's rate limit (~200 req/s). With parallel fetching this must be enforced explicitly.

### Enforcing Game Rules
- Only links in paragraph (`<p>`) body text are allowed — exclude sidebars, infoboxes, navboxes, and the references section.
- The current `get_links_from_html` has a bug: `soup.find_all('a', href=True)` scans the whole document instead of being scoped to `<p>` tags. This needs to be fixed.
- Rule enforcement should be a separate, testable function.

### Concurrency
- Use `asyncio` + `aiohttp` for async parallel page fetching — more efficient than threads for I/O-bound work.
- Determine a safe concurrency limit to stay within Wikipedia's rate limits.

### Caching
- Cache page link lists to avoid re-fetching the same page across runs.
- In-memory cache is simplest; sqlite is better for persistence across runs.
- Cache key should be the page title. Staleness is unlikely to matter.

### Interface
- Source article: CLI argument or random if not provided (already implemented).
- Destination: currently hardcoded as `Adolf_Hitler` — consider making it configurable.
- Output: show the full path, elapsed time, and number of pages fetched.
- Failure case: clear message when no path is found within depth limit.

### Testing
- Avoid hitting the Wikipedia API on every test run — use cached fixtures or mock responses.
