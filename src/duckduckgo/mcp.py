"""DuckDuckGo MCP Server.

This module provides an MCP server that exposes DuckDuckGo search functionality
as MCP tools, resources, and prompts.
"""

from typing import Literal

from ddgs import DDGS
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

BODY_PREVIEW_LENGTH = 200

# Common DuckDuckGo region codes and human-readable names
REGION_CODES: dict[str, str] = {
    "xa-ar": "Arabia",
    "xa-en": "Arabia (en)",
    "ar-es": "Argentina",
    "au-en": "Australia",
    "at-de": "Austria",
    "be-fr": "Belgium (fr)",
    "be-nl": "Belgium (nl)",
    "br-pt": "Brazil",
    "bg-bg": "Bulgaria",
    "ca-en": "Canada",
    "ca-fr": "Canada (fr)",
    "ct-ca": "Catalan",
    "cl-es": "Chile",
    "cn-zh": "China",
    "co-es": "Colombia",
    "hr-hr": "Croatia",
    "cz-cs": "Czech Republic",
    "dk-da": "Denmark",
    "ee-et": "Estonia",
    "fi-fi": "Finland",
    "fr-fr": "France",
    "de-de": "Germany",
    "gr-el": "Greece",
    "hk-tzh": "Hong Kong",
    "hu-hu": "Hungary",
    "in-en": "India",
    "id-id": "Indonesia",
    "id-en": "Indonesia (en)",
    "ie-en": "Ireland",
    "il-he": "Israel",
    "it-it": "Italy",
    "jp-jp": "Japan",
    "kr-kr": "Korea",
    "lv-lv": "Latvia",
    "lt-lt": "Lithuania",
    "xl-es": "Latin America",
    "my-ms": "Malaysia",
    "my-en": "Malaysia (en)",
    "mx-es": "Mexico",
    "nl-nl": "Netherlands",
    "nz-en": "New Zealand",
    "no-no": "Norway",
    "pe-es": "Peru",
    "ph-en": "Philippines",
    "ph-tl": "Philippines (tl)",
    "pl-pl": "Poland",
    "pt-pt": "Portugal",
    "ro-ro": "Romania",
    "ru-ru": "Russia",
    "sg-en": "Singapore",
    "sk-sk": "Slovak Republic",
    "sl-sl": "Slovenia",
    "za-en": "South Africa",
    "es-es": "Spain",
    "se-sv": "Sweden",
    "ch-de": "Switzerland (de)",
    "ch-fr": "Switzerland (fr)",
    "ch-it": "Switzerland (it)",
    "tw-tzh": "Taiwan",
    "th-th": "Thailand",
    "tr-tr": "Turkey",
    "ua-uk": "Ukraine",
    "uk-en": "United Kingdom",
    "us-en": "United States",
    "ue-es": "United States (es)",
    "ve-es": "Venezuela",
    "vn-vi": "Vietnam",
    "wt-wt": "No region",
}


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
    log_level="CRITICAL",
)


# Regions resource
@mcp.resource("duckduckgo://regions")
def get_regions() -> dict:
    """List supported region codes and human-readable names.

    Returns a JSON object with a short note, the total count, and the
    list of available region codes.
    """
    return {
        "note": (
            "Pass one of these codes as the 'region' parameter. Use null to let "
            "DuckDuckGo choose a default (worldwide)."
        ),
        "count": len(REGION_CODES),
        "regions": [
            {"code": code, "name": name} for code, name in REGION_CODES.items()
        ],
    }


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
    raw_results = DDGS().text(
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


def main_mcp():
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main_mcp()
