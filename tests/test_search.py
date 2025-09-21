from duckduckgo import search


def test_search():
    # Note: This test makes a real API call; in production, consider mocking
    results = search("python", max_results=1)
    assert isinstance(results, list)
    if results:
        assert isinstance(results[0], dict)
        assert "title" in results[0]
