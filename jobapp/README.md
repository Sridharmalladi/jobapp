---
title: JobApp
emoji: 🧠
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.40.0
app_file: app.py
pinned: false
---

# 🧠 JobApp – AI-Powered Resume Matcher

JobApp is a lightweight AI-based tool built using Gradio that lets you upload a job description and multiple resumes, computes semantic similarity between them, and ranks candidates based on relevance — all with a simple UI.

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

## 📁 Folder Structure

JobApp/
│
├── app.py # Main Gradio app
├── db.py # DB connection and schema logic
├── document_processor.py # File parsing and text extraction
├── embeddings.py # Generates OpenAI embeddings
├── summarizer.py # Summarizes job descriptions
├── utils.py # Common helper methods
├── init_db.py # Database initializer
├── requirements.txt # Python dependencies
├── data/ # Resumes and JD files (PDF/text)



## ✅ How to Run Locally

Pre-requisite: Python 3.8+

1. Clone or download the project folder

2. Install dependencies

```bash
pip install -r requirements.txt


OPENAI_API_KEY=sk-your-openai-key-here