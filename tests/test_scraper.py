
from scraper.scraper import PropertyScraper


def test_extract_listing():
    scraper = PropertyScraper()

    html = """
    <article class="property-card">
        <h2 class="title">Office Space</h2>
        <span class="price">$100,000</span>
        <span class="location">New York</span>
        <span class="broker">John Smith</span>
        <span class="phone">123456789</span>
        <a class="listing-link" href="/property/1">View</a>
    </article>
    """

    records = scraper.extract(
        html,
        "https://example.com/listings"
    )

    assert len(records) == 1
    assert records[0]["title"] == "Office Space"
    assert records[0]["url"] == "https://example.com/property/1"


def test_missing_fields():
    scraper = PropertyScraper()

    html = """
    <article class="property-card">
        <h2 class="title">Office Space</h2>
        <a class="listing-link" href="/property/2">View</a>
    </article>
    """

    records = scraper.extract(
        html,
        "https://example.com"
    )

    assert records[0]["phone"] == ""
    assert records[0]["broker"] == ""


def test_next_page():
    scraper = PropertyScraper()

    html = """
    <a class="next" href="/page/2">Next</a>
    """

    result = scraper.next_page(
        html,
        "https://example.com/page/1"
    )

    assert result == "https://example.com/page/2"


def test_no_next_page():
    scraper = PropertyScraper()

    result = scraper.next_page(
        "<html><body>No next page</body></html>",
        "https://example.com"
    )

    assert result is None


def test_duplicate_removal():
    scraper = PropertyScraper()

    html = """
    <article class="property-card">
        <h2 class="title">Office</h2>
        <a class="listing-link" href="/property/1">View</a>
    </article>
    """

    scraper.fetch = lambda url: (
        html if url.endswith("/page1")
        else html
    )

    scraper.next_page = lambda html, url: (
        "https://example.com/page2"
        if url.endswith("/page1")
        else None
    )

    records = scraper.scrape(
        "https://example.com/page1",
        max_pages=5
    )

    assert len(records) == 1
