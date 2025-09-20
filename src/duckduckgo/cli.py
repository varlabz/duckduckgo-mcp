import click

from duckduckgo import search

BODY_PREVIEW_LENGTH = 200


@click.command()
@click.argument("query")
@click.option("--max-results", "-m", default=10, type=int, help="Max results")
@click.option("--region", "-r", default=None, help="Region code (e.g., us-en)")
@click.option(
    "--safesearch",
    "-s",
    default="moderate",
    type=click.Choice(["on", "moderate", "off"]),
    help="Safe search level",
)
@click.option(
    "--timelimit",
    "-t",
    default=None,
    type=click.Choice(["d", "w", "m", "y"]),
    help="Time limit",
)
def cli(query, max_results, region, safesearch, timelimit):
    """DuckDuckGo search CLI using ddgs API."""
    kwargs = {}
    if region:
        kwargs["region"] = region
    if safesearch:
        kwargs["safesearch"] = safesearch
    if timelimit:
        kwargs["timelimit"] = timelimit

    results = search(query, max_results=max_results, **kwargs)

    if not results:
        click.echo("No results found.")
        return

    for i, result in enumerate(results, 1):
        click.echo(f"{i}. {result.get('title', 'No title')}")
        click.echo(f"   URL: {result.get('href', 'No URL')}")
        body = result.get("body", "No body")
        click.echo(
            f"   Body: {body[:BODY_PREVIEW_LENGTH]}"
            f"{'...' if len(body) > BODY_PREVIEW_LENGTH else ''}"
        )
        click.echo()


if __name__ == "__main__":
    cli()

