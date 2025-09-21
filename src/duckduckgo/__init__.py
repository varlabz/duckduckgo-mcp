from ddgs import DDGS

__version__ = "0.0.1"


def search(
    query, max_results=10, region=None, safesearch="off", timelimit=None, **kwargs
):
    """Search for text using DuckDuckGo via ddgs API.

    Args:
        query (str): The search query.
        max_results (int): Maximum number of results to return. Defaults to 10.
        region (str): Region code (e.g., us-en). Defaults to None.
        safesearch (str): Safe search ('on', 'moderate', 'off'). Defaults to 'off'.
        timelimit (str): Time limit ('d', 'w', 'm', 'y'). Defaults to None.
        **kwargs: Additional DDGS.text() args.

    Returns:
        list: List of dictionaries with search results.
    """
    ddgs = DDGS()
    return ddgs.text(
        query,
        max_results=max_results,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        **kwargs,
    )
