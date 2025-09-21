import duckduckgo as ddg


def test_search(monkeypatch):
    # Avoid real network by faking the DDGS client

    class FakeDDGS:
        def text(
            self,
            query,
            max_results=10,
            _region=None,
            _safesearch="off",
            _timelimit=None,
            **_kwargs,
        ):
            data = [
                {
                    "title": f"Result for {query}",
                    "href": "https://example.com",
                    "body": "Example search result",
                }
            ]
            return data[:max_results]

    monkeypatch.setattr(ddg, "DDGS", lambda: FakeDDGS())

    results = ddg.search("python", max_results=1)
    assert isinstance(results, list)
    if results:
        assert isinstance(results[0], dict)
        assert "title" in results[0]
