import argparse
import json
import sys
from typing import Final

from duckduckgo.mcp import search_tool

BODY_PREVIEW_LENGTH: Final[int] = 200


def main_cli():
    """DuckDuckGo search CLI using ddgs API."""
    parser = argparse.ArgumentParser(description="DuckDuckGo search CLI")
    parser.add_argument("query", nargs=argparse.ONE_OR_MORE, help="Search query")
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
        "--json", action="store_true", help="Output results as JSON array"
    )
    args = parser.parse_args()

    if not args.query:
        parser.error("Search query is required")

    query = " ".join(args.query)

    response = search_tool(
        query,
        max_results=args.max_results,
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
