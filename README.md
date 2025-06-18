# 📄 CV Parser – Smart Recruiter Assistant

A **Streamlit** web app that uses LLMs and embeddings to parse, analyze, and query candidate CVs (PDF/DOCX/TXT), enabling smart insights and resume search with ease.

🟢 **[Launch the App Now →](https://smart-recruiter-assistant.streamlit.app/)**

---

## ⚙️ Features

- Upload multiple CVs in PDF, DOCX, or TXT formats  
- Display a summary of uploaded files (name, size, type)  
- Extract text using custom `process_uploaded_files()`  
- Embed extracted chunks into a vector store  
- Query the knowledge base using `process_query()`  
- Visual, interactive UI with Lottie animation and beautiful styling  
- Streamlit app hosted and publicly accessible

---

## 🧱 Tech Stack

- **Frontend**: Streamlit, `streamlit_lottie`  
- **Backend**: Python  
- **LLM/Embeddings**:Gemini (configured via `llm_config.py`)  
- **Vector Store**: ChromaDB or other local embedding DB  
- **Others**: Pandas, Pillow, Requests, OS, Shutil

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+  
- pip  
- Gemini API Key

### Installation

```bash
git clone https://github.com/yasminkadry/Smart-Recruiter-Assistant-RAG-based
cd Smart-Recruiter-Assistant-RAG-based
pip install -r requirements.txt
````

### Setup Environment

```bash
cp .env
# Then open .env and add your keys (API_KEY, EMBEDDING_MODEL, etc.)
```

### Run Locally

```bash
streamlit run main.py
```

Visit: [http://localhost:8501](http://localhost:8501)

---

## 🧠 How It Works

1. Upload one or more CVs
2. Type a custom instruction/query for the AI

   * e.g. *"Find candidates with deep learning experience"*
3. Click **Process Query**
4. Watch progress in real time
5. Get visual AI-powered response with summary or matching links

---

## 📂 Project Structure

```
.
├── main.py             # Streamlit app UI
├── llm_config.py       # LLM and embeddings config
├── process_files.py    # Extract text from files
├── process_query.py    # Query vector DB with AI
├── vector_store.py     # Embedding & similarity search
├── assets/             # Animations or images
├── requirements.txt
├── .env
```

---

## 🌐 Live Demo

🟢 **Deployed App**: [https://smart-recruiter-assistant.streamlit.app/](https://smart-recruiter-assistant.streamlit.app/)

---

## 📈 Roadmap

* [x] Upload & parse CVs
* [x] LLM integration for smart queries
* [x] Candidate ranking & scoring
* [x] PDF summary report export



## 🙌 Acknowledgements

* Streamlit Community
* Gemini API integrations
* Inspiration from resume/CV NLP parser projects

---

🧠 Built with ❤️ `By My Team` to help recruiters find the right talent smarter and faster.
