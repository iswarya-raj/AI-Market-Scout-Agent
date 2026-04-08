from datetime import datetime, timedelta
from dateutil import parser
import re


def extract_date_from_text(text: str):
    """
    Try extracting a date from raw article text using regex.
    """

    # Matches formats like:
    # March 2, 2026
    # 2 March 2026
    # 2026-03-02

    patterns = [
        r"\b\d{4}-\d{2}-\d{2}\b",
        r"\b\d{1,2} [A-Za-z]+ \d{4}\b",
        r"\b[A-Za-z]+ \d{1,2}, \d{4}\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)

    return None


def is_recent(date_string: str, days: int = 7):
    if not date_string:
        return False

    try:
        published_date = parser.parse(date_string, fuzzy=True)
        now = datetime.now(published_date.tzinfo)

        return (now - published_date) <= timedelta(days=days)

    except Exception:
        return False


def filter_recent_articles(articles, days: int = 7):
    return articles
   # filtered = []
#   for article in articles:
 #       date_string = article.get("date")
#
        # If no meta date found, try extracting from text
 #       if not date_string:
  #          date_string = extract_date_from_text(article.get("content", ""))
#
 #       if is_recent(date_string, days):
  #          filtered.append(article)
#
 #   return filtered
