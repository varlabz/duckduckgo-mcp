import argparse
import json
import sys

from duckduckgo import search

BODY_PREVIEW_LENGTH = 200


def main():
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
        choices=["d", "w", "m", "y"],
        help="Time limit",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output results as JSON array"
    )
    args = parser.parse_args()

    if not args.query:
        parser.error("Search query is required")

    query = " ".join(args.query)

    results = search(
        query,
        max_results=args.max_results,
        region=args.region,
        safesearch=args.safesearch,
        timelimit=args.timelimit,
    )

    if not results:
        sys.stdout.write("No results found.\n")
        return

    if args.json:
        sys.stdout.write(json.dumps(results, indent=2) + "\n")
    else:
        for i, result in enumerate(results, 1):
            sys.stdout.write(f"{i}. {result.get('title', 'No title')}\n")
            sys.stdout.write(f"   URL: {result.get('href', 'No URL')}\n")
            body = result.get("body", "No body")
            sys.stdout.write(
                f"   {body[:BODY_PREVIEW_LENGTH]}"
                f"{'...' if len(body) > BODY_PREVIEW_LENGTH else ''}\n"
            )
            sys.stdout.write("\n")


if __name__ == "__main__":
    main()
