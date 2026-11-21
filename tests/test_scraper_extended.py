from scraper.scraper import PropertyScraper

def test_invalid_cards_are_ignored():
    scraper = PropertyScraper()
    html = """
    <article class="property-card">
        <h2 class="title">Missing URL</h2>
    </article>
    <article class="property-card">
        <a class="listing-link" href="/property/2">View</a>
    </article>
    """
    assert scraper.extract(html, "https://example.com") == []

def test_relative_listing_url_resolution():
    scraper = PropertyScraper()
    html = """
    <article class="property-card">
        <h2 class="title">Office</h2>
        <a class="listing-link" href="../property/3">View</a>
    </article>
    """
    records = scraper.extract(html, "https://example.com/listings/page1")
    assert records[0]["url"] == "https://example.com/property/3"

def test_rel_next_pagination():
    scraper = PropertyScraper()
    html = '<a rel="next" href="/page/2">Next</a>'
    assert scraper.next_page(
        html, "https://example.com/page/1"
    ) == "https://example.com/page/2"

def test_scrape_respects_max_pages():
    scraper = PropertyScraper()
    calls = []

    scraper.fetch = lambda url: calls.append(url) or "<html></html>"
    scraper.next_page = lambda html, url: (
        "https://example.com/page/2"
        if url.endswith("page/1")
        else "https://example.com/page/3"
    )

    scraper.scrape("https://example.com/page/1", max_pages=2)
    assert len(calls) == 2

def test_scrape_stops_after_fetch_failure():
    scraper = PropertyScraper()
    calls = []

    def fake_fetch(url):
        calls.append(url)
        return None

    scraper.fetch = fake_fetch
    result = scraper.scrape("https://example.com/page/1")

    assert result == []
    assert len(calls) == 1

def test_scrape_stops_pagination_loop():
    scraper = PropertyScraper()
    calls = []

    scraper.fetch = lambda url: calls.append(url) or "<html></html>"
    scraper.next_page = lambda html, url: "https://example.com/page/1"

    scraper.scrape("https://example.com/page/1", max_pages=5)
    assert len(calls) == 1

def test_fetch_handles_request_exception():
    from unittest.mock import Mock
    import requests

    scraper = PropertyScraper()
    response = Mock()
    response.raise_for_status.side_effect = requests.RequestException("test error")
    scraper.session.get = Mock(return_value=response)

    assert scraper.fetch("https://example.com") is None
