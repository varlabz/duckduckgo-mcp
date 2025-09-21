import argparse
import json
import sys
from typing import Final

from duckduckgo.mcp import (
    get_regions,
    research_planner,
    search_assistant,
    search_tool,
)

BODY_PREVIEW_LENGTH: Final[int] = 200


def main_cli():
    """DuckDuckGo search CLI using ddgs API."""
    parser = argparse.ArgumentParser(description="DuckDuckGo search CLI")
    parser.add_argument("query", nargs=argparse.ZERO_OR_MORE, help="Search query")
    parser.add_argument("--max-results", "-m", type=int, default=10, help="Max results")
    parser.add_argument("--region", "-r", help="Region code (e.g., us-en)")
    parser.add_argument(
        "--safesearch",
        "-s",
        choices=["on", "moderate", "off"],
        default="off",
        help="Safe search level",
    )
    parser.add_argument(
        "--timelimit",
        "-t",
        choices=["day", "week", "month", "year"],
        help="Time limit",
    )
    parser.add_argument(
        "--categories",
        "-c",
        choices=["text", "images", "videos", "news"],
        default="text",
        help="Result type to search (text, images, videos, news)",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output results as JSON array"
    )
    parser.add_argument(
        "--resoure-regions",
        action="store_true",
        help="List supported region codes from MCP and exit",
    )
    # Prompt functions
    parser.add_argument(
        "--prompt-search-assistant",
        metavar="QUERY",
        help="Generate the search_assistant prompt text for a query",
    )
    parser.add_argument(
        "--prompt-search-assistant-context",
        metavar="CTX",
        default="",
        help="Optional context string for --prompt-search-assistant",
    )
    parser.add_argument(
        "--prompt-research-planner",
        metavar="TOPIC",
        help="Generate the research_planner prompt text for a topic",
    )
    parser.add_argument(
        "--prompt-research-planner-depth",
        metavar="DEPTH",
        default="basic",
        help="Depth for --prompt-research-planner (basic, intermediate, comprehensive)",
    )
    args = parser.parse_args()

    # Prompt generation handlers (early return)
    if args.prompt_search_assistant:
        prompt_text = search_assistant(
            query=args.prompt_search_assistant,
            context=args.prompt_search_assistant_context,
        )
        sys.stdout.write(prompt_text + "\n")
        return

    if args.prompt_research_planner:
        prompt_text = research_planner(
            topic=args.prompt_research_planner,
            depth=args.prompt_research_planner_depth,
        )
        sys.stdout.write(prompt_text + "\n")
        return

    # If --resoure-regions is requested, list and exit early
    if args.resoure_regions:
        regions_data = get_regions()
        if args.json:
            sys.stdout.write(json.dumps(regions_data, indent=2) + "\n")
        else:
            count = regions_data.get("count", 0)
            sys.stdout.write(f"Supported regions (count {count}):\n")
            for item in regions_data.get("regions", []):
                code = item.get("code", "")
                name = item.get("name", "")
                sys.stdout.write(f"- {code}: {name}\n")
        return

    if not args.query:
        parser.error("Search query is required")

    query = " ".join(args.query)

    response = search_tool(
        query,
        max_results=args.max_results,
        categories=args.categories,
        region=args.region,
        safesearch=args.safesearch,
        timelimit=args.timelimit,
    )
    results = response.results

    if not results:
        sys.stdout.write("No results found.\n")
        return

    if args.json:
        # Convert Pydantic models to a list of dicts for JSON serialization
        results_dicts = [result.model_dump() for result in results]
        sys.stdout.write(json.dumps(results_dicts, indent=2) + "\n")
    else:
        for i, result in enumerate(results, 1):
            sys.stdout.write(f"{i}. {result.title}\n")
            sys.stdout.write(f"   URL: {result.url}\n")
            body = result.body
            sys.stdout.write(
                f"   {body[:BODY_PREVIEW_LENGTH]}"
                f"{'...' if len(body) > BODY_PREVIEW_LENGTH else ''}\n"
            )
            sys.stdout.write("\n")


if __name__ == "__main__":
    main_cli()
