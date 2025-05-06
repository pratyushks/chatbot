# 📘 Retrieval-Augmented Generation (RAG) Support Chatbot

A smart chatbot that answers user queries based on Angel One support content and insurance plan documents using Retrieval-Augmented Generation (RAG) — powered by FAISS and Hugging Face models.

Site Link: https://pratyushks-chatbot-frontendapp-miuylq.streamlit.app/

---

## 🚀 Features

- 🔍 Answers only from provided documents (insurance PDFs and scraped Angel One support content)
- 🤖 Uses MBZUAI/LaMini-Flan-T5-783M for local, free text generation
- ❓ Responds with "I don't know" for out-of-scope questions
- 🧠 FAISS vector search for document retrieval
- 💬 Streamlit-based chat UI + FastAPI backend
- 🗂️ Fully local and privacy-preserving (no external LLM required)

---

## 📁 Project Structure

```bash
chatbot/
│
├── backend/                 # FastAPI backend + RAG logic
│   ├── main.py              # API entrypoint
│   └── rag_engine.py        # Loads vector DB + model
│
├── frontend/                # Streamlit UI
│   └── app.py
│
├── scripts/                 # Data loading and processing
│   ├── build_vectorstore.py
│   ├── load_documents.py
│   └── scrape_dynamic.py
│
├── data/                    # Insurance PDFs + scraped support text
│
├── vectorstore/             # Saved FAISS index
│
├── .env                     # Environment variables (models etc.)
└── requirements.txt
```

## ⚙️ Setup Instructions

### Clone and Install Dependencies

```bash
git clone https://github.com/pratyush/chatbot.git
cd chatbot
python -m venv venv
venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Add Documents

* Add PDFs under `data/Insurance_PDFs`
* Run dynamic scraping to collect support data:

```bash
python scripts/scrape_dynamic.py
```


### Build Vectorstore

```bash
python scripts/build_vectorstore.py
```

### Start FastAPI Backend

```bash
uvicorn backend.main:app --reload
```

Visit the interactive API docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

### Start Chat UI

In a new terminal:

```bash
streamlit run frontend/app.py
```

The chat interface will launch at: [http://localhost:8501](http://localhost:8501)

---

## 🧪 Example Questions

* What is the deductible for the 2500 Gold plan?
* Are chiropractic services covered?
* How do I withdraw funds from Angel One?
