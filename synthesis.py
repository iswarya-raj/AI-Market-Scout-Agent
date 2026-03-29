import os
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -----------------------------
# RETRY FUNCTION
# -----------------------------

def call_groq_with_retry(messages, retries=3):

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                temperature=0.2,
                messages=messages,
                timeout=20
            )
            return response

        except Exception as e:
            print(f"Attempt {attempt+1} failed:", e)
            time.sleep(2)

    return None


# -----------------------------
# MAIN FUNCTION
# -----------------------------

def generate_brief(company_name: str, articles: list):
    """
    Generates final competitor briefing document.
    """

    # -----------------------------
    # NO ARTICLES CASE
    # -----------------------------
    if not articles:
        return f"""
Competitor Briefing – {company_name}

No new technical features or updates were released in the last 7 days.
"""

    # -----------------------------
    # PREPARE CONTENT
    # -----------------------------
    combined_content = ""

    for article in articles:
        combined_content += f"""
Title: {article['title']}
URL: {article['url']}
Content: {article['content'][:1500]}
---
"""

    # -----------------------------
    # PROMPT
    # -----------------------------
    system_prompt = """
You are a competitive intelligence analyst.

Summarize ONLY the new technical features mentioned in the provided articles.

Focus only on:
- API changes
- New technical capabilities
- Developer-related updates

Do NOT include marketing fluff.
Do NOT invent information.
Include citations using the provided URLs.

Return a professional competitor briefing document.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": combined_content}
    ]

    # -----------------------------
    # CALL WITH RETRY
    # -----------------------------
    response = call_groq_with_retry(messages)

    # -----------------------------
    # FALLBACK IF API FAILS
    # -----------------------------
    if response is None:
        return f"""
Competitor Briefing – {company_name}

⚠ Unable to generate AI summary due to API issue.

However, {len(articles)} recent articles were successfully collected.

You can review them in the Research Sources section above.
"""

    # -----------------------------
    # RETURN RESULT SAFELY
    # -----------------------------
    try:
        return response.choices[0].message.content
    except Exception:
        return f"""
Competitor Briefing – {company_name}

⚠ Unexpected error while generating summary.

But {len(articles)} recent articles were found and displayed above.
"""