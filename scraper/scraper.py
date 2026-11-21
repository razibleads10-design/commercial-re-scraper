
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


FIELDS = {
    "title": ".title",
    "price": ".price",
    "location": ".location",
    "broker": ".broker",
    "phone": ".phone"
}


class PropertyScraper:

    def __init__(self, timeout=15):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; PropertyResearch/1.0)"
        })

    def fetch(self, url):
        try:
            response = self.session.get(
                url,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.text

        except requests.RequestException as error:
            print(f"Request failed: {error}")
            return None

    def extract(self, html, page_url):
        soup = BeautifulSoup(html, "html.parser")
        results = []

        for card in soup.select(".property-card"):
            item = {}

            for field, selector in FIELDS.items():
                element = card.select_one(selector)
                item[field] = (
                    element.get_text(" ", strip=True)
                    if element else ""
                )

            link = card.select_one("a.listing-link")

            item["url"] = (
                urljoin(page_url, link["href"])
                if link and link.get("href")
                else ""
            )

            if item["title"] and item["url"]:
                results.append(item)

        return results

    def next_page(self, html, current_url):
        soup = BeautifulSoup(html, "html.parser")
        link = soup.select_one("a.next, a[rel='next']")

        if link and link.get("href"):
            return urljoin(current_url, link["href"])

        return None

    def scrape(self, start_url, max_pages=5):
        records = []
        visited = set()
        current_url = start_url

        while current_url and len(visited) < max_pages:
            if current_url in visited:
                break

            visited.add(current_url)

            html = self.fetch(current_url)

            if html is None:
                break

            records.extend(
                self.extract(html, current_url)
            )

            current_url = self.next_page(
                html,
                current_url
            )

        unique = {}

        for record in records:
            unique[record["url"]] = record

        return list(unique.values())
