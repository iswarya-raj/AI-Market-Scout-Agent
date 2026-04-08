import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

# Domains we want to avoid
BLOCKED_DOMAINS = [
    "wikipedia.org",
    "linkedin.com",
    "facebook.com",
    "twitter.com",
    "dashboard.",
]


def is_valid_url(url: str):
    for blocked in BLOCKED_DOMAINS:
        if blocked in url:
            return False
    return True


def search_web(query: str, max_results: int = 5):
    """
    Uses DuckDuckGo (ddgs) to fetch filtered URLs.
    """
    urls = []

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)

        for result in results:
            url = result["href"]

            if is_valid_url(url):
                urls.append(url)

            if len(urls) >= 3:
                break

    return urls


def scrape_page(url: str):
    """
    Scrapes title, publish date (if found),
    and main text content from a webpage.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "lxml")

        title = soup.title.string.strip() if soup.title else "No Title"

        # Try finding date
        date = None
        meta_tags = soup.find_all("meta")

        for tag in meta_tags:
            if tag.get("property") in ["article:published_time", "og:published_time"]:
                date = tag.get("content")
            if tag.get("name") in ["publish_date", "pubdate", "timestamp"]:
                date = tag.get("content")

        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs)

        if len(text) < 200:
            return None

        return {
            "url": url,
            "title": title,
            "date": date,
            "content": text[:4000]
        }

    except Exception:
        return None
