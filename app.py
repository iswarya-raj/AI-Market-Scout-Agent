import streamlit as st
import time
import pandas as pd
import io
from reportlab.pdfgen import canvas

from search_planner import generate_search_queries
from scraper import search_web, scrape_page
from date_filter import filter_recent_articles
from synthesis import generate_brief


st.set_page_config(
    page_title="Market Scout Agent",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# PDF CREATION FUNCTION
# -----------------------------
def create_pdf(text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    y = 800

    for line in text.split("\n"):
        c.drawString(50, y, line)
        y -= 15

        if y < 50:
            c.showPage()
            y = 800

    c.save()
    buffer.seek(0)
    return buffer


# -----------------------------
# PAGE HEADER
# -----------------------------
st.title("Market Scout Agent")
st.caption("Automated competitor intelligence from the last 7 days")

st.markdown("---")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Agent Controls")

company = st.sidebar.text_input(
    "Competitor Company Name",
    placeholder="Example: OpenAI"
)

# ✅ NEW: Competitor Mode Input
st.sidebar.markdown("---")
st.sidebar.subheader("Competitor Mode")

competitors_input = st.sidebar.text_input(
    "Compare Multiple Companies",
    placeholder="OpenAI, Google, Anthropic"
)

competitor_list = [c.strip() for c in competitors_input.split(",") if c.strip()]

run_agent = st.sidebar.button("Run Market Scout")


# -----------------------------
# MAIN PAGE LAYOUT
# -----------------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Competitor Briefing")

with col2:
    st.subheader("Pipeline Status")


# -----------------------------
# RUN AGENT
# -----------------------------
if run_agent:

    status = st.empty()
    progress = st.progress(0)

    # =========================================================
    # 🔵 COMPETITOR MODE
    # =========================================================
    if competitor_list:

        st.subheader("📊 Competitor Comparison Report")

        comparison_data = []
        full_reports = {}

        for comp in competitor_list:

            status.info(f"Processing {comp}...")

            result = generate_search_queries(comp)
            queries = result["queries"]

            all_articles = []
            seen_urls = set()

            for query in queries:
                urls = search_web(query)

                for url in urls:
                    if url in seen_urls:
                        continue

                    seen_urls.add(url)

                    article = scrape_page(url)

                    if article:
                        all_articles.append(article)

            recent_articles = filter_recent_articles(all_articles, days=7)

            brief = generate_brief(comp, recent_articles)

            full_reports[comp] = brief

            comparison_data.append({
                "Company": comp,
                "Articles Found": len(all_articles),
                "Recent Articles": len(recent_articles),
                "Insights Preview": brief[:150]
            })

        # -----------------------------
        # TABLE VIEW
        # -----------------------------
        df = pd.DataFrame(comparison_data)

        st.dataframe(df, use_container_width=True)

        # -----------------------------
        # SIDE-BY-SIDE COMPARISON
        # -----------------------------
        st.markdown("### 🔍 Side-by-Side Analysis")

        cols = st.columns(len(competitor_list))

        for i, comp in enumerate(competitor_list):
            with cols[i]:
                st.markdown(f"#### {comp}")
                st.write(full_reports[comp][:500])

        # -----------------------------
        # 🧠 WHO IS LEADING (AI SUMMARY)
        # -----------------------------
        st.markdown("### 🏆 Who is Leading?")

        # simple logic (you can upgrade later with AI)
        best_company = max(comparison_data, key=lambda x: x["Recent Articles"])

        st.success(
            f"{best_company['Company']} appears to be leading based on recent activity "
            f"with {best_company['Recent Articles']} recent updates."
        )

        # -----------------------------
        # FULL REPORT EXPANDERS
        # -----------------------------
        st.markdown("### 📄 Detailed Reports")

        for comp in competitor_list:
            with st.expander(f"{comp} Full Report"):
                st.write(full_reports[comp])

        st.stop()

    # =========================================================
    # 🟢 NORMAL MODE (UNCHANGED)
    # =========================================================
    if not company:
        st.warning("Please enter a competitor company name.")
        st.stop()

    # STEP 1
    status.info("Generating search queries using LLM...")
    progress.progress(10)

    with st.spinner("Planning search queries..."):
        result = generate_search_queries(company)
        queries = result["queries"]

    st.success("Search queries generated")

    with st.expander("View Generated Queries"):
        for q in queries:
            st.write(q)

    progress.progress(30)

    # STEP 2
    status.info("Searching and scraping articles...")

    all_articles = []
    seen_urls = set()

    with st.spinner("Collecting data from the web..."):

        for query in queries:
            urls = search_web(query)

            for url in urls:
                if url in seen_urls:
                    continue

                seen_urls.add(url)

                article = scrape_page(url)

                if article:
                    all_articles.append(article)

    progress.progress(55)

    st.metric("Total Articles Collected", len(all_articles))

    # STEP 3
    status.info("Filtering articles from last 7 days")

    with st.spinner("Filtering recent updates..."):
        recent_articles = filter_recent_articles(all_articles, days=7)

    progress.progress(75)

    st.metric("Recent Articles", len(recent_articles))

    # TABLE
    if recent_articles:
        df = pd.DataFrame([
            {"Title": art["title"], "Source": art["url"]}
            for art in recent_articles
        ])

        st.markdown("### Research Sources")
        st.dataframe(df, use_container_width=True)

    # STEP 4
    status.info("Generating competitor briefing")

    with st.spinner("Analyzing articles and generating report..."):
        briefing = generate_brief(company, recent_articles)

    progress.progress(100)
    status.success("Analysis complete")

    st.markdown("### Competitor Briefing Report")

    st.markdown(f"<pre>{briefing}</pre>", unsafe_allow_html=True)

    pdf = create_pdf(briefing)

    st.download_button(
        label="Download Report as PDF",
        data=pdf,
        file_name="competitor_briefing.pdf",
        mime="application/pdf"
    )