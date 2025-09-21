"""DuckDuckGo MCP Server.

This module provides an MCP server that exposes DuckDuckGo search functionality
as MCP tools, resources, and prompts.
"""

from typing import Literal

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from duckduckgo import search as ddg_search

BODY_PREVIEW_LENGTH = 200


class SearchResult(BaseModel):
    """A single search result from DuckDuckGo."""

    title: str = Field(description="The title of the search result")
    url: str = Field(description="The URL of the search result")
    body: str = Field(description="The body/snippet of the search result")


class SearchResponse(BaseModel):
    """Response containing search results."""

    query: str = Field(description="The search query that was executed")
    results: list[SearchResult] = Field(description="List of search results")
    total_results: int = Field(description="Total number of results returned")


# Create the FastMCP server instance
mcp = FastMCP(
    name="DuckDuckGo Search",
    instructions="A search server that provides access to DuckDuckGo search results. "
    "Use the search tools to find information on the web.",
)


@mcp.tool(name="search")
def search_tool(
    query: str,
    max_results: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of results to return (1-50)",
    ),
    region: str | None = Field(
        default=None, description="Region code (e.g., 'us-en', 'uk-en', 'de-de')"
    ),
    safesearch: Literal["on", "moderate", "off"] = Field(
        default="off", description="Safe search level"
    ),
    timelimit: Literal["day", "week", "month", "year"] | None = Field(
        default=None, description="Time limit for results"
    ),
) -> SearchResponse:
    """Search the web using DuckDuckGo.

    This tool performs a web search using DuckDuckGo and returns structured results
    including titles, URLs, and body snippets.

    Args:
        query: The search query string
        max_results: Maximum number of results to return (1-50)
        region: Region code for localized results (optional)
        safesearch: Safe search filtering level
        timelimit: Time limit for results (day, week, month, year)

    Returns:
        SearchResponse with query, results, and total count
    """
    # map timelimit values to ddg_search parameters
    tl = (
        {
            "day": "d",
            "week": "w",
            "month": "m",
            "year": "y",
        }.get(timelimit.strip().lower(), None)
        if timelimit
        else None
    )
    raw_results = ddg_search(
        query,
        max_results=max_results,
        region=region,
        safesearch=safesearch,
        timelimit=tl,
    )

    # Convert to structured results
    results = [
        SearchResult(
            title=result.get("title", "No title"),
            url=result.get("href", "No URL"),
            body=result.get("body", "No body"),
        )
        for result in raw_results
    ]

    return SearchResponse(query=query, results=results, total_results=len(results))


@mcp.tool()
def quick_search(query: str, max_results: int = 5) -> str:
    """Perform a quick web search and return formatted text results.

    This is a simplified version that returns human-readable text instead of
    structured data, useful for quick lookups.

    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 5)

    Returns:
        Formatted string with search results
    """
    results = ddg_search(query, max_results=max_results)

    if not results:
        return f"No results found for query: {query}"

    output = f"Search results for: {query}\n\n"
    for i, result in enumerate(results, 1):
        output += f"{i}. {result.get('title', 'No title')}\n"
        output += f"   URL: {result.get('href', 'No URL')}\n"
        body = result.get("body", "No body")
        # Truncate body if too long
        if len(body) > BODY_PREVIEW_LENGTH:
            body = body[:BODY_PREVIEW_LENGTH] + "..."
        output += f"   {body}\n\n"

    return output.strip()


@mcp.resource("search://recent/{query}")
def recent_search_results(query: str) -> str:
    """Get recent search results for a query.

    This resource provides access to recent search results that can be
    referenced by other tools or cached for performance.

    Args:
        query: The search query

    Returns:
        Formatted search results
    """
    return quick_search(query, max_results=10)


@mcp.prompt()
def search_assistant(query: str, context: str = "") -> str:
    """Generate a search assistant prompt for analyzing search results.

    This prompt helps users analyze and understand search results by providing
    context and asking targeted questions.

    Args:
        query: The search query
        context: Additional context about what the user is looking for

    Returns:
        A formatted prompt for search analysis
    """
    query_line = (
        f'I need you to help me analyze search results for the query: "{query}"'
    )
    base_prompt = f"""{query_line}

Please examine the following search results and provide insights about:
1. The most relevant and authoritative sources
2. Key information and facts from the results
3. Any patterns or trends in the information
4. Potential biases or limitations in the results
5. Recommendations for follow-up searches if needed

"""

    if context:
        base_prompt += f"\nAdditional context: {context}\n\n"

    base_prompt += "Search Results:\n[SEARCH_RESULTS]"

    return base_prompt


@mcp.prompt()
def research_planner(topic: str, depth: str = "basic") -> str:
    """Generate a research planning prompt for comprehensive topic exploration.

    This prompt helps structure research by breaking down complex topics into
    manageable search queries and analysis steps.

    Args:
        topic: The research topic
        depth: Research depth level (basic, intermediate, comprehensive)

    Returns:
        A structured research planning prompt
    """
    depth_levels = {
        "basic": "3-5 key questions",
        "intermediate": "5-8 focused questions",
        "comprehensive": "8-12 detailed questions",
    }

    questions_desc = depth_levels.get(depth, depth_levels["basic"])

    topic_line = f'I need to research the topic: "{topic}"'
    plan_line = (
        "Please help me create a structured research plan. "
        f"Break this topic down into {questions_desc} that I should search for."
    )

    return f"""{topic_line}

{plan_line}

For each question, suggest:
1. Specific search queries to use
2. What type of information I'm looking for
3. How the results will contribute to understanding the overall topic

Organize the research plan logically, starting with foundational questions
and building to more complex analysis.

Topic: {topic}
Research Depth: {depth}
"""


def main():
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
