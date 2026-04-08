import os
import json
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
                temperature=0,
                messages=messages,
                timeout=20   # prevents hanging
            )
            return response

        except Exception as e:
            print(f"Attempt {attempt+1} failed:", e)
            time.sleep(2)

    return None


# -----------------------------
# MAIN FUNCTION
# -----------------------------

def generate_search_queries(company_name: str):
    """
    Generates 3–4 highly targeted search queries
    focused on recent technical updates.
    """

    system_prompt = """
You are a competitive intelligence search planner.

Your job is to generate 3 to 4 highly targeted search engine queries
to find ONLY technical feature updates released in the last 7 days.

Focus only on:
- API updates
- Release notes
- Developer documentation updates
- Technical feature launches

Avoid:
- Marketing campaigns
- Financial news
- Opinion articles
- General company news

IMPORTANT:
Return ONLY valid JSON in this format:

{
  "queries": [
    "query 1",
    "query 2",
    "query 3",
    "query 4"
  ]
}

Do not include explanations.
Do not include extra text.
Only return JSON.
"""

    user_prompt = f"Company Name: {company_name}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # -----------------------------
    # CALL WITH RETRY
    # -----------------------------

    response = call_groq_with_retry(messages)

    # -----------------------------
    # FALLBACK IF API FAILS
    # -----------------------------

    if response is None:
        print("⚠ Using fallback queries due to API failure")

        return {
            "queries": [
                f"{company_name} release notes last 7 days",
                f"{company_name} API updates recent",
                f"{company_name} developer documentation update",
                f"{company_name} new technical features"
            ]
        }

    content = response.choices[0].message.content

    # -----------------------------
    # SAFE JSON PARSING
    # -----------------------------

    try:
        parsed = json.loads(content)
        return parsed

    except json.JSONDecodeError:
        print("⚠ Model did not return valid JSON.")
        print("Raw output:\n", content)

        # fallback if JSON fails
        return {
            "queries": [
                f"{company_name} release notes",
                f"{company_name} API updates",
                f"{company_name} developer updates",
                f"{company_name} new features"
            ]
        }
