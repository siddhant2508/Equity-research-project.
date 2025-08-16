# News Research Tool 📈

A Streamlit app that ingests news/article URLs, builds a local FAISS vector index with OpenAI embeddings, and answers questions with source citations using a Retrieval-QA chain (LangChain).

> ✅ Updated for LangChain v0.2+ (`langchain_openai`, `langchain_community`)  
> ✅ Uses `FAISS.save_local()` / `FAISS.load_local()` (no pickling)  
> ✅ Streamlit-first run instructions (no more ScriptRunContext warnings)

---

## ✨ Features

- Paste up to 3 article URLs; the app:
  - fetches & parses pages (`UnstructuredURLLoader`)
  - splits content into chunks
  - embeds with `OpenAIEmbeddings`
  - builds a FAISS vector store and saves it locally
- Ask questions — answers come with **sources**.
- Simple Streamlit UI you can run locally.

---

## 🏗️ Architecture

```
Streamlit UI → LangChain RetrievalQAWithSourcesChain
              → Retriever (FAISS + OpenAIEmbeddings)
              → Documents (UnstructuredURLLoader)
```

---

## 📁 Project Structure

```
Equity-research-project/
├─ main.py
├─ requirements.txt
├─ .env                  # contains OPENAI_API_KEY=...
└─ faiss_index_openai/   # created at runtime by save_local()
```

---

## 🔧 Requirements

- Python 3.10
- macOS
- An OpenAI **Platform** API key (billing enabled)

### Python packages

```
streamlit
langchain
langchain-community
langchain-openai
faiss-cpu
unstructured
python-dotenv
```

Install:

```bash
pip install -U streamlit langchain langchain-community langchain-openai faiss-cpu unstructured python-dotenv
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

---

## ▶️ Run the App

Always run with **Streamlit** 
```bash
cd "/Users/siddhantdhatrak/Desktop/Gen AI/Equity-research-project"
python3 -m streamlit run main.py
# or: streamlit run main.py
```

Then open the printed URL (usually http://localhost:8501).

---

## 🖥️ Usage

1. Enter up to 3 article URLs in the sidebar.
2. Click **Process URLs**. Wait until you see *“Index ready!”*
3. Ask a question in the input box.
4. Read the **Answer** and **Sources** shown below.

---

## ✅ Checklist

- [ ] `.env` contains `OPENAI_API_KEY`
- [ ] Installed requirements in the **same** interpreter you run
- [ ] Start with `streamlit run main.py`
- [ ] If using OpenAI: billing set up + credits purchased + monthly budget > $0

---
