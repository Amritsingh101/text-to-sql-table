# Text-to-SQL Table Finder

An end-to-end AI-powered schema retrieval system and interactive web application. Given a natural language query (e.g., *"find the user details named anshul"*), the system identifies and ranks the most relevant database tables required for SQL query generation using **Hybrid BM25 + FAISS Vector Search + Cross-Encoder Reranking**.

---

## 🚀 Key Features

- **Hybrid Retrieval Architecture**: Combines keyword search (BM25) with dense semantic search (`BAAI/bge-base-en-v1.5` via FAISS).
- **Cross-Encoder Reranking**: Re-evaluates top candidates using `ms-marco-MiniLM-L6-v2` for precise joint self-attention ranking.
- **Offline Model Support**: Downloads ML models once on initial setup and caches them locally under `backend/data/models/` for full offline execution.
- **FastAPI Backend**: Asynchronous Python backend with automatic lifespan initialization and schema hash tracking.
- **Modern React + Vite Frontend**: Fast, responsive dark-mode UI with query input, Top-K controls, preset query pills, and one-click table name copy.

---

## 🏗️ Architecture & Pipeline Flow

```
                      User Query (Natural Language)
                                   │
                                   ▼
                ┌──────────────────┴──────────────────┐
                │                                     │
                ▼                                     ▼
      1. BM25 Lexical Search              2. FAISS Vector Search
       (Term Matching Score)              (BGE-Base Dense Embedding)
                │                                     │
                └──────────────────┬──────────────────┘
                                   │
                                   ▼
                     3. Reciprocal Rank Fusion (RRF)
                         (Top 15 Candidate Tables)
                                   │
                                   ▼
                     4. Cross-Encoder Reranker
                     (ms-marco-MiniLM-L6-v2)
                                   │
                                   ▼
                    Top K Relevant Database Tables
```

---

## 📁 Repository Structure

```
text-sql/
├── README.md                      # Unified project documentation
├── schema/                        # Database schema definition
│   └── schema.json                # Primary database schema input
│
├── backend/                       # Python FastAPI Backend
│   ├── main.py                    # FastAPI app entry point & CORS configuration
│   ├── startup.py                 # Lifespan initializer & index builder
│   ├── matadata.py                # Schema documentation parser & tokenizer
│   ├── requirements.txt           # Python dependencies
│   ├── data/                      # Local offline storage for artifacts & models
│   │   ├── models/                # Downloaded SentenceTransformer & CrossEncoder models
│   │   ├── table_names.pkl
│   │   ├── documents.pkl
│   │   ├── tokenized_docs.pkl
│   │   ├── bm25.pkl
│   │   └── embedding_index.faiss
│   ├── indexing/                  # Index builders (BM25, FAISS, CrossEncoder)
│   │   ├── bm25.py
│   │   ├── embedding.py
│   │   └── cross_encoder.py
│   └── search/                    # Search & retrieval algorithms
│       ├── bm25_search.py
│       ├── embedding_search.py
│       ├── rrf_search.py
│       └── reranker.py
│
└── frontend/                      # React + Vite Frontend
    ├── index.html                 # Main HTML entry point
    ├── vite.config.js             # Vite configuration
    ├── package.json               # Node.js dependencies
    └── src/
        ├── main.jsx               # React entry point
        ├── App.jsx                # Main app layout & state management
        ├── index.css              # Glassmorphic dark mode styling
        └── components/
            ├── Header.jsx         # Live backend status indicator & branding
            ├── SearchCard.jsx     # Query input, Top K selector & sample pills
            ├── TableCard.jsx      # Ranked table card display with copy button
            └── ResultsSection.jsx # Results grid & state handling
```

---

## 🛠️ Quick Start Guide

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** & **npm**

---

### Step 1: Set Up & Run the Backend

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI backend server:
   ```bash
   python -m uvicorn main:app --reload
   ```
   *The backend runs at **`http://127.0.0.1:8000`**.*

> **Note:** On first startup, the backend automatically reads `schema/schema.json`, builds all FAISS vector indices, and downloads ML models to `backend/data/models/`. All subsequent runs execute completely offline.

---

### Step 2: Set Up & Run the Frontend

1. Open a new terminal and navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The frontend runs at **`http://localhost:5173`**.*

---

## 📡 API Reference

### Health Check
- **`GET /`**
- **Response:**
  ```json
  {
    "message": "Text-to-SQL Table Finder is running. POST to /search"
  }
  ```

### Search Tables
- **`POST /search`**
- **Headers:** `Content-Type: application/json`
- **Request:**
  ```json
  {
    "query": "find the user details named anshul",
    "top_k": 7
  }
  ```
- **Response:**
  ```json
  {
    "query": "find the user details named anshul",
    "tables": [
      { "table": "customer", "score": -8.9969 },
      { "table": "tbl_ord_item", "score": -10.6416 },
      { "table": "recommendation_log", "score": -10.7920 }
    ]
  }
  ```

---

## ⚙️ Tech Stack Summary

| Layer | Technologies |
|---|---|
| **Frontend** | React 19, Vite, Lucide React, CSS3 (Glassmorphism Dark Mode) |
| **Backend API** | Python, FastAPI, Uvicorn, Pydantic |
| **Lexical Retrieval** | Rank-BM25 |
| **Vector Retrieval** | FAISS (`faiss-cpu`), SentenceTransformers (`BAAI/bge-base-en-v1.5`) |
| **Reranking** | CrossEncoder (`cross-encoder/ms-marco-MiniLM-L6-v2`) |
| **Persistence** | Pickle, NumPy, FAISS Index |
