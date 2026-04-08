import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

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


def search_web(query: str, max_results: int = 10):
    """
    Uses DuckDuckGo (ddgs) to fetch filtered URLs.
    """
    urls = []

    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)

            for result in results:
                url = result.get("href")

                if url and is_valid_url(url):
                    urls.append(url)

                # collect more links for better success rate
                if len(urls) >= 5:
                    break

    except Exception as e:
        print("Search error:", e)

    return urls


def scrape_page(url: str):
    """
    Scrapes title, publish date (if found),
    and main text content from a webpage.
    Always returns fallback data to avoid empty results.
    """
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, "lxml")

        title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"

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

        # ✅ Fallback if scraping fails or content too small
        if not text or len(text) < 50:
            text = "Content could not be fully scraped. Showing limited extracted information."

        return {
            "url": url,
            "title": title,
            "date": date,
            "content": text[:2000]  # keep safe size
        }

    except Exception as e:
        print("Scraping error:", e)

        # ✅ Always return fallback instead of None
        return {
            "url": url,
            "title": "Unavailable",
            "date": None,
            "content": "Failed to scrape full content from this source."
        }
