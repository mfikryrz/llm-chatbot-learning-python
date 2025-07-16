# 🧠 LLM Exercise – Python Tutor Chatbot

This project is an educational chatbot application powered by RAG (Retrieval-Augmented Generation), combining:

* **LLM via Groq (`gemma2-9b-it`)**
* **Embeddings from Ollama (`nomic-embed-text`)**
* **FastAPI** as the backend
* **React + Vite** for the modern frontend
* **Streamlit** as an alternative interface (legacy)
* **Markdown files** as the knowledge base

---

## 🗂 Project Structure

```bash
llm-exercise/
│
├── lessons/                   # Raw markdown lesson files
│   ├── python_variables.md
│   └── ...
│
├── lessons_faiss/             # FAISS indexes generated from lessons
│   ├── python_variables/
│   └── ...
│
├── backend/                   # FastAPI backend source
│   ├── llm_groq.py            # RAG chain logic
│   ├── build_faiss_index.py   # Indexes markdown → FAISS
│   └── app.py                 # Main FastAPI server
│
├── frontend-llm/              # Frontend built with Vite + React
│   ├── src/
│   │   ├── App.jsx
│   │   └── ChatBox.jsx
│   └── ...
│
├── legacy_streamlit.py        # Streamlit-based fallback UI
├── main.py                    # Alternative FastAPI entrypoint
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
```

---

## ⚙️ How It Works

1. **Preprocessing:**

   * Run `build_faiss_index.py` to embed markdown files into FAISS index using `nomic-embed-text`.

2. **Backend:**

   * The `/chat` FastAPI endpoint receives `prompt` and `lesson` → builds a contextual RAG chain via `llm_groq.py`.

3. **RAG Chain:**

   * Retrieves relevant chunks via FAISS
   * Combines them with user prompt
   * Uses `ChatGroq` (Groq API) to generate answers in Bahasa Indonesia.

4. **Frontend:**

   * The React app (`frontend-llm`) sends POST requests to `127.0.0.1:8000/chat`.

5. **Optional:**

   * Streamlit UI (`legacy_streamlit.py`) provides a side-by-side learning/chat interface.

---

## 📘 Sample Lesson Files

```bash
lessons/
├── python_variables.md
├── python_list.md
├── if_else.md
├── while.md
├── for_loops.md
└── functions.md
```

---

## 🚀 How to Run

### 1. Generate FAISS Index

```bash
python backend/build_faiss_index.py
```

### 2. Start FastAPI Server

```bash
uvicorn backend.app:app --reload
```

### 3. Start Frontend (Vite)

```bash
cd frontend-llm
npm install
npm run dev
```

---

## 🔐 .env File

Your `.env` file should look like:

```
GROQ_API_KEY=your_groq_api_key_here
```

---

## 📦 Python Requirements

All packages are listed in `requirements.txt`. Some highlights include:

* `langchain`
* `langchain-groq`
* `langchain-ollama`
* `faiss-cpu`
* `streamlit`
* `fastapi`
* `uvicorn`
* `ollama`
* `python-dotenv`

---

## 📌 Example Request (POST /chat)

```json
{
  "prompt": "What is a for loop?",
  "lesson": "for_loops"
}
```

---


## 📌 Note on `lesson` Variable in Frontend

In the file `frontend-llm/src/ChatBox.jsx`, the lesson used for the query is currently **hardcoded** as `"for_loops"`:

```js
const res = await fetch("http://127.0.0.1:8000/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    prompt: input,
    lesson: "for_loops" // <--- currently hardcoded lesson name
  }),
});
```

⚠️ **Important**:
Make sure the `lesson` value matches the FAISS folder name in `lessons_faiss`. For example:

* `lesson: "functions"` → maps to `lessons_faiss/functions/`

### 🛠 To Do (optional)

If you want the user to select which lesson to use dynamically, you can update the `ChatBox.jsx` component to include a dropdown (`<select>`) or other UI element and pass the selected lesson to the backend. Let me know if you'd like help implementing this dynamic selector!

---
## ⚠️ Important Notes

* Embedding model must be consistent across indexing and querying (`nomic-embed-text`)
* Ollama must be running with the selected embedding model (`ollama run nomic-embed-text`)
* Ensure `lesson` sent from frontend matches the folder name inside `lessons_faiss`
* If you want to use Ollama directly for LLM (instead of Groq), you can swap out the chain logic accordingly
