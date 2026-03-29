# Quick Start
1. Install requirements
2. Add API key in .env
3. Run: streamlit run app.py

# 📊 Market Scout Agent

An AI-powered competitive intelligence tool that analyzes recent updates from companies and generates structured, developer-focused insights.

---

## 🚀 Features

* 🔍 Automated web search & article scraping
* 🧠 AI-generated structured competitor briefings
* 📊 Competitor Mode (multi-company comparison)
* 🏆 Leader detection based on recent technical activity
* 📄 Download reports as PDF
* ⚡ Robust pipeline with retry & fallback handling

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit** (UI)
* **Groq API (LLM)**
* **BeautifulSoup** (Web scraping)
* **Pandas**
* **ReportLab** (PDF generation)

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/market-scout-agent.git
cd market-scout-agent
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Add API key

Create a `.env` file in the root folder:

```env
GROQ_API_KEY=your_api_key_here
```

---

### 5. Run the application

```bash
streamlit run app.py
```

---

## 🧪 How to Use

### 🔹 Single Company Mode

* Enter a company name
* The system fetches recent articles
* Generates a structured technical briefing

---

### 🔹 Competitor Mode

* Enter multiple companies (comma-separated)
* View:

  * 📊 Comparison table
  * 📄 Individual reports
  * 🏆 Activity-based leader

---

## ⏱️ Performance

* Execution time: **~5 seconds to 1 minute**
* Depends on:

  * Web scraping latency
  * API response time

---

## 🧠 Key Highlights

* Structured output using prompt engineering
* Fault-tolerant AI calls (retry + fallback)
* Clean UI with actionable insights
* Supports both **deep analysis** and **comparative analysis**

---

## ⚠️ Limitations

* Depends on publicly available articles
* Some sources may lack technical details
* API latency may vary

---
