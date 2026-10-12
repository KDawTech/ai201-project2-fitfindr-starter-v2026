"""FitFindr MCP server — Unit 4 Milestone 1."""
from mcp.server.fastmcp import FastMCP
from tools import search_listings as _search_listings_impl

mcp = FastMCP("fitfindr", log_level="WARNING")


@mcp.tool()
def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """Search secondhand listings using description keywords plus optional size
    and maximum price (in dollars). Returns matching listing dictionaries in
    best-match order, or an empty list when nothing matches all supplied filters.
    """
    return _search_listings_impl(description, size, max_price)


if __name__ == "__main__":
    mcp.run()
