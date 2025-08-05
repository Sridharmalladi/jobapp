# 🧠 JobApp – AI-Powered Resume Matcher

JobApp is a lightweight AI-based tool built using Gradio that lets you upload a job description and multiple resumes, computes semantic similarity between them, and ranks candidates based on relevance — all with a simple UI.

# Approach - 
I built this app to match resumes with job descriptions using a combination of LLM-based summarization and embedding similarity. Resumes are parsed, summarized, and scored against the job description to find the best fit. A simple Gradio interface displays the ranked results. The goal was to go beyond keyword matching and use contextual relevance to make hiring smarter.

## 🚀 Features
- 📄 Upload a Job Description (JD) and multiple resumes
- 🧠 Auto-summarizes long JDs using OpenAI
- 🔍 Embeds text with OpenAI Embeddings (text-embedding-ada-002)
- 📈 Computes semantic similarity (cosine similarity)
- 📊 Ranks candidates by best fit
- 🎛️ Gradio interface — clean, interactive, minimal

## 🛡️ Tech Stack
- Python – Core logic
- Gradio – Frontend UI
- OpenAI API – For summarization and embeddings
- SQLite – Lightweight database
- dotenv – For managing API keys
- FAISS / Cosine Similarity – For document similarity (you may customize)


## ✅ How to Run Locally

Pre-requisite: Python 3.8+

1. Clone or download the project folder

2. Install dependencies

```bash
pip install -r requirements.txt


OPENAI_API_KEY=sk-your-openai-key-here
