# guardrails.py

def validate_company_input(company_input: str) -> str:
    """
    Basic guardrail for user input.
    Currently acts as a pass-through (non-intrusive).

    Future scope:
    - Input sanitization
    - Profanity filtering
    - Injection protection
    """

    if not company_input:
        return ""

    # Strip unwanted spaces
    cleaned_input = company_input.strip()

    return cleaned_input


def validate_articles(articles: list) -> list:
    """
    Ensures articles list is safe and valid.
    Currently does minimal filtering.
    """

    if not articles:
        return []

    valid_articles = []

    for article in articles:
        if (
            isinstance(article, dict)
            and "title" in article
            and "url" in article
            and "content" in article
        ):
            valid_articles.append(article)

    return valid_articles