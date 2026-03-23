# 🎵 Music Store Assistant

> An AI-powered chatbot that lets you query a music store database in plain English — and answers store policy questions too.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=flat)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-6A0DAD?style=flat)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

---

<!-- SCREENSHOT: Replace the placeholder below with a screenshot of your app -->
<!-- ![App Screenshot](docs/screenshot.png) -->

## 📌 Overview

**Music Store Assistant** is a dual-mode AI chatbot built with Streamlit. It uses **semantic routing** to automatically detect what kind of question you're asking and routes it to the right pipeline:

| Question Type | Example | Pipeline |
|---|---|---|
| 🗃️ Database queries | *"Which artist has the most albums?"* | SQL Chain (LLM → SQLite) |
| 📋 Store policies | *"What is your return policy?"* | FAQ Chain (ChromaDB RAG) |

---

## 🏗️ Architecture

```
User Question
      │
      ▼
┌─────────────────┐
│  Semantic Router │  ← FastEmbed encoder classifies intent
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
 [sql]      [faq]
    │         │
    ▼         ▼
Generate   Vector
SQL with   Search
LLM        ChromaDB
    │         │
    ▼         ▼
Run on     Build
SQLite     Prompt
    │         │
    └────┬────┘
         ▼
    LLM generates
    plain English answer
         │
         ▼
    Streamlit UI
```

---

## ✨ Features

- 🔍 **Natural language to SQL** — Ask database questions in plain English; the LLM writes and runs the SQL for you
- 📚 **RAG-powered FAQ** — Store policy questions are answered using semantic search over a CSV knowledge base
- 🧭 **Smart routing** — `semantic-router` automatically detects intent, no need to tell the bot which mode to use
- 💬 **Chat history** — Full conversation memory within a session, with SQL queries displayed inline
- ⚡ **Powered by Groq** — Fast inference using `llama-3.3-70b-versatile`

---

## 🗂️ Project Structure

```
music-store-assistant/
│
├── app.py              # Streamlit UI + routing logic
├── chatbot.py          # SQL chain: schema → SQL → run → answer
├── faq.py              # FAQ chain: ingest CSV → ChromaDB → RAG answer
├── router.py           # Semantic router with intent routes
│
├── data/
│   ├── chinook.db      # SQLite music store database
│   └── faqs.csv        # FAQ knowledge base (question, answer columns)
│
├── .env                # API keys (not committed)
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/music-store-assistant.git
cd music-store-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

Get your free Groq API key at [console.groq.com](https://console.groq.com).

### 4. Add your data

- Place the **Chinook SQLite database** at `data/chinook.db`
  - Download it from [github.com/lerocha/chinook-database](https://github.com/lerocha/chinook-database)
- Add your **FAQ CSV** at `data/faqs.csv` with columns: `question`, `answer`

### 5. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🖼️ Screenshots

<!-- Add your screenshots below. Recommended: drag images into the GitHub editor when editing this README. -->

### Chat Interface
<!-- ![Chat Interface](docs/chat-interface.png) -->
> *Screenshot coming soon — add yours here!*

### SQL Query in Action
<!-- ![SQL Query](docs/sql-query.png) -->
> *The bot displays the generated SQL alongside the plain-English answer.*

### FAQ Response
<!-- ![FAQ Response](docs/faq-response.png) -->
> *Store policy questions are answered from the vector knowledge base.*

---

## 📦 Requirements

```
streamlit
groq
python-dotenv
chromadb
pandas
sentence-transformers
semantic-router
```

Generate a `requirements.txt` with:
```bash
pip freeze > requirements.txt
```

---

## 🧠 How It Works

### SQL Chain (`chatbot.py`)
1. **Schema extraction** — Reads all table and column names from the SQLite DB
2. **SQL generation** — Sends the schema + user question to Groq LLM, gets back a raw SQL query
3. **Query execution** — Runs the SQL on the local Chinook database
4. **Answer generation** — Sends the results back to the LLM to generate a friendly plain-English response

### FAQ Chain (`faq.py`)
1. **Ingestion** — On startup, FAQ CSV rows are embedded using `all-MiniLM-L6-v2` and stored in ChromaDB
2. **Retrieval** — Top 2 most semantically similar Q&A pairs are fetched for each user query
3. **Answer generation** — A prompted LLM answers using only the retrieved context (no hallucination)

### Semantic Router (`router.py`)
- Uses `FastEmbedEncoder` to classify each incoming query
- Routes to `sql` or `faq` based on similarity to predefined example utterances
- Falls back to a helpful default message if neither route matches

---

## 🛠️ Customization

| What to change | Where |
|---|---|
| Add more FAQ routes | `router.py` — add utterances to the `faq` Route |
| Add more SQL example queries | `router.py` — add utterances to the `sql` Route |
| Swap the LLM model | `.env` → `GROQ_MODEL` or hardcode in `chatbot.py` |
| Use a different database | Update `DB_PATH` in `chatbot.py` |
| Update store description in FAQ prompt | `faq.py` — find the `# TODO` comment |

---



## 🙌 Acknowledgements

- [Chinook Database](https://github.com/lerocha/chinook-database) — sample music store dataset
- [Groq](https://groq.com) — fast LLM inference
- [ChromaDB](https://www.trychroma.com) — local vector database
- [Semantic Router](https://github.com/aurelio-labs/semantic-router) — intent classification
- [Streamlit](https://streamlit.io) — UI framework
