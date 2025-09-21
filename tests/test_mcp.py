import re

import pytest


@pytest.fixture
def fake_ddgs(monkeypatch):
    """Patch DDGS to avoid network and capture call arguments.

    Provides a FakeDDGS class with configurable `response_data` and a
    `last_kwargs` dict capturing the most recent call.
    """
    import duckduckgo.mcp as m

    class FakeDDGS:
        response_data: list[dict] = []
        last_kwargs: dict | None = None
        last_method: str | None = None

        def text(
            self,
            query,
            max_results=None,
            region=None,
            safesearch=None,
            timelimit=None,
        ):
            FakeDDGS.last_method = "text"
            FakeDDGS.last_kwargs = {
                "query": query,
                "max_results": max_results,
                "region": region,
                "safesearch": safesearch,
                "timelimit": timelimit,
            }
            # Return a shallow copy to avoid accidental mutation between tests
            return list(FakeDDGS.response_data)

        def images(
            self,
            query,
            max_results=None,
            region=None,
            safesearch=None,
            timelimit=None,
        ):
            FakeDDGS.last_method = "images"
            FakeDDGS.last_kwargs = {
                "query": query,
                "max_results": max_results,
                "region": region,
                "safesearch": safesearch,
                "timelimit": timelimit,
            }
            return list(FakeDDGS.response_data)

        def videos(
            self,
            query,
            max_results=None,
            region=None,
            safesearch=None,
            timelimit=None,
        ):
            FakeDDGS.last_method = "videos"
            FakeDDGS.last_kwargs = {
                "query": query,
                "max_results": max_results,
                "region": region,
                "safesearch": safesearch,
                "timelimit": timelimit,
            }
            return list(FakeDDGS.response_data)

        def news(
            self,
            query,
            max_results=None,
            region=None,
            safesearch=None,
            timelimit=None,
        ):
            FakeDDGS.last_method = "news"
            FakeDDGS.last_kwargs = {
                "query": query,
                "max_results": max_results,
                "region": region,
                "safesearch": safesearch,
                "timelimit": timelimit,
            }
            return list(FakeDDGS.response_data)

    monkeypatch.setattr(m, "DDGS", FakeDDGS)
    return FakeDDGS


def test_regions_resource_structure():
    from duckduckgo.mcp import REGION_CODES, get_regions

    res = get_regions()
    assert isinstance(res, dict)
    assert set(["note", "count", "regions"]) <= set(res.keys())
    assert res["count"] == len(REGION_CODES)
    # Ensure regions list contains code/name pairs and all codes are present
    codes_from_resource = {item["code"] for item in res["regions"]}
    assert codes_from_resource == set(REGION_CODES.keys())


def test_search_tool_positive_results_and_mapping(fake_ddgs):
    from duckduckgo.mcp import SearchResponse, search_tool

    fake_ddgs.response_data = [
        {
            "title": "DuckDuckGo",
            "href": "https://duckduckgo.com/",
            "body": "Privacy, simplified.",
        },
        {
            "title": "About",
            "href": "https://duckduckgo.com/about",
            "body": "About DuckDuckGo.",
        },
    ]

    resp = search_tool(
        query="duckduckgo",
        max_results=2,
        region="us-en",
        safesearch="off",
        timelimit=" week ",  # exercise strip/lower mapping → 'w'
    )

    assert isinstance(resp, SearchResponse)
    assert resp.query == "duckduckgo"
    assert resp.total_results == 2
    assert [r.url for r in resp.results] == [
        "https://duckduckgo.com/",
        "https://duckduckgo.com/about",
    ]

    # Validate timelimit mapping applied when calling DDGS().text
    assert fake_ddgs.last_kwargs is not None
    assert fake_ddgs.last_kwargs["timelimit"] == "w"
    assert fake_ddgs.last_kwargs["region"] == "us-en"
    assert fake_ddgs.last_kwargs["max_results"] == 2


def test_search_tool_handles_missing_fields(fake_ddgs):
    from duckduckgo.mcp import search_tool

    # Simulate incomplete result dicts
    fake_ddgs.response_data = [
        {"href": "https://example.com"},  # missing title/body
        {"title": "Only title"},  # missing href/body
        {"body": "Only body"},  # missing title/href
    ]

    resp = search_tool(query="test", max_results=3, timelimit=None)
    assert resp.total_results == 3
    # Defaults from implementation: "No title", "No URL", "No body"
    titles = [r.title for r in resp.results]
    urls = [r.url for r in resp.results]
    bodies = [r.body for r in resp.results]

    assert titles == ["No title", "Only title", "No title"]
    assert urls == ["https://example.com", "No URL", "No URL"]
    assert bodies == ["No body", "No body", "Only body"]


def test_search_tool_dispatches_by_category(fake_ddgs):
    from duckduckgo.mcp import SearchResponse, search_tool

    # News category dispatch and timelimit mapping
    fake_ddgs.response_data = [
        {"title": "N1", "url": "https://news.example", "body": "NB"}
    ]
    resp = search_tool(
        query="q",
        categories="news",
        timelimit="WEEK",  # exercise case-insensitive mapping
        max_results=1,
        region="us-en",
        safesearch="moderate",
    )
    assert isinstance(resp, SearchResponse)
    assert resp.total_results == 1
    assert fake_ddgs.last_method == "news"
    assert fake_ddgs.last_kwargs is not None
    assert fake_ddgs.last_kwargs["timelimit"] == "w"
    assert resp.results[0].url == "https://news.example"

    # Text remains default
    fake_ddgs.response_data = [
        {"title": "T1", "href": "https://t.example", "body": "TB"}
    ]
    resp2 = search_tool(query="q", max_results=1)
    assert fake_ddgs.last_method == "text"
    assert resp2.results[0].url == "https://t.example"


def test_search_tool_images_and_videos_mapping(fake_ddgs):
    from duckduckgo.mcp import search_tool

    # Images: fallback to image when url/href missing
    fake_ddgs.response_data = [
        {"title": "I1", "image": "https://img.example/i.jpg", "thumbnail": "t"}
    ]
    img_resp = search_tool(query="q", categories="images", max_results=1)
    assert fake_ddgs.last_method == "images"
    assert img_resp.results[0].url == "https://img.example/i.jpg"
    assert img_resp.results[0].body == "No body"

    # Videos: use content for url and description for body
    fake_ddgs.response_data = [
        {
            "title": "V1",
            "content": "https://video.example/v",
            "description": "VD",
        }
    ]
    vid_resp = search_tool(query="q", categories="videos", max_results=1)
    assert fake_ddgs.last_method == "videos"
    assert vid_resp.results[0].url == "https://video.example/v"
    assert vid_resp.results[0].body == "VD"


def test_search_tool_invalid_timelimit_maps_to_none(fake_ddgs):
    from duckduckgo.mcp import search_tool

    fake_ddgs.response_data = []
    resp = search_tool(query="test", timelimit="decade")
    assert resp.total_results == 0
    assert fake_ddgs.last_kwargs is not None
    assert fake_ddgs.last_kwargs["timelimit"] is None


def test_search_assistant_prompt_contains_sections():
    from duckduckgo.mcp import search_assistant

    out = search_assistant(query="python testing", context="focus on pytest")
    # Contains query and context
    assert "python testing" in out
    assert "Additional context: focus on pytest" in out
    # Contains the Search Results placeholder
    assert "Search Results:\n[SEARCH_RESULTS]" in out
    # Contains numbered guidance list items
    for n in range(1, 6):
        assert re.search(fr"^{n}\. ", out, re.MULTILINE)


def test_search_assistant_prompt_without_context():
    from duckduckgo.mcp import search_assistant

    out = search_assistant(query="no context test")
    assert "no context test" in out
    assert "Additional context:" not in out


def test_research_planner_depth_variations():
    from duckduckgo.mcp import research_planner

    out_intermediate = research_planner(topic="AI", depth="intermediate")
    assert "5-8 focused questions" in out_intermediate
    assert "Topic: AI" in out_intermediate
    assert "Research Depth: intermediate" in out_intermediate

    # Unknown depth falls back to 'basic' description
    out_unknown = research_planner(topic="AI", depth="deep")
    assert "3-5 key questions" in out_unknown
    assert "Research Depth: deep" in out_unknown


def test_main_mcp_invokes_run(monkeypatch):
    import duckduckgo.mcp as m

    called = {"ran": False}

    def fake_run():  # noqa: D401 - simple test stub
        called["ran"] = True

    monkeypatch.setattr(m.mcp, "run", fake_run)
    m.main_mcp()
    assert called["ran"] is True
