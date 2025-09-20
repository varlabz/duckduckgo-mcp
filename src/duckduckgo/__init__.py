from ddgs import DDGS


def search(query, max_results=10, **kwargs):
    """Search for text using DuckDuckGo via ddgs API.

    Args:
        query (str): The search query.
        max_results (int): Maximum number of results to return. Defaults to 10.
        **kwargs: Additional DDGS.text() args (region, safesearch, timelimit).

    Returns:
        list: List of dictionaries with search results.
    """
    ddgs = DDGS()
    return ddgs.text(query, max_results=max_results, **kwargs)
