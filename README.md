# 🚀 Reddit Sentiment ETL Pipeline (Data & AI Engineering)

An automated Data Engineering pipeline that extracts data from Reddit, performs Natural Language Processing (NLP) sentiment analysis, and loads the structured data into a cloud PostgreSQL database.

## 📌 Project Overview
The goal of this project is to track community sentiment and reactions to PC hardware releases, pricing, and technical issues. It acts as a foundational architecture for AI-driven customer feedback analysis.

## 🏗️ Architecture & ETL Process

1. **Extract (API Integration):** - Connects to the `r/buildapc` subreddit via Reddit's JSON API.
   - Extracts the latest posts (titles, authors, timestamps, URLs).
2. **Transform (Data Cleaning & AI Analysis):** - Cleans and formats raw JSON data into structured Pandas DataFrames.
   - Converts Unix timestamps to standard datetime objects.
   - Integrates **TextBlob (NLP)** to analyze the sentiment of each post title, generating a `sentiment_score` (-1.0 to 1.0) and a categorical `sentiment_label` (Positive, Negative, Neutral).
3. **Load (Cloud Database):** - Connects securely to a **Neon Serverless PostgreSQL** database.
   - Uses `SQLAlchemy` to load the transformed dataset into the cloud via automated queries.
4. **Data Export:**
   - Includes a standalone script to extract the latest database records and export them to a clean `.csv` format for BI tools (Excel, Power BI, Tableau).

## 🛠️ Tech Stack
* **Language:** Python
* **Data Processing:** Pandas, NumPy
* **AI / NLP:** TextBlob
* **Database:** PostgreSQL (Neon DB), SQLAlchemy, psycopg2
* **Security:** `python-dotenv` for secure credential management

## 🔒 Security Note
Database credentials are intentionally excluded from this repository and are managed locally via `.env` variables and GitHub Secrets for CI/CD deployments.
