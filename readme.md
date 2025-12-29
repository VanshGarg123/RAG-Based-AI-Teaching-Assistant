🤖 RAG-Based AI Teaching Assistant

> An intelligent **Retrieval-Augmented Generation (RAG)** powered AI assistant that helps users instantly find the **exact video and timestamp** where a concept is explained.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![RAG](https://img.shields.io/badge/Architecture-RAG-purple.svg)
![Local AI](https://img.shields.io/badge/AI-Local%20(Ollama)-orange.svg)

---

## 🌟 What Is This Project?

This project converts your **video course library into an interactive AI tutor**.

Instead of manually scrubbing through hours of video content, learners can simply ask questions in natural language, and the AI will:

- Understand the intent of the question
- Search semantically across all video transcripts
- Respond with the **most relevant video name and precise timestamp**

### 🔍 Example Interaction

**User:**  
> How do I center a div in CSS?

**AI:**  
> This topic is covered in **Video 5 – “CSS Basics”**, starting at **03:45**, where multiple centering techniques are explained.

---

## ✨ Key Features

- 🎯 Semantic search across entire video libraries  
- ⏱️ Precise timestamps for instant navigation  
- 💬 Natural chat-style user interface  
- 🚀 Fast vector-based retrieval using embeddings  
- 🔒 Fully local and private using Ollama  
- 🧠 Retrieval-Augmented Generation (RAG) pipeline  
- 🧩 Modular design for easy extension  

---

## 📚 Use Cases

- Online learning platforms  
- University lecture archives  
- Corporate training videos  
- Coaching and mentorship programs  
- Self-hosted AI learning assistants  

---

## 📋 Prerequisites

### 🔹 Install Ollama and Required Models

```bash
# Install Ollama from https://ollama.ai/
ollama pull bge-m3      # Embedding model
ollama pull llama3.2   # Large Language Model


# Install Python dependencies
pip install flask numpy scikit-learn pandas requests joblib
```

## 🚀 Quick Start

### 1. Process Your Videos (One-Time Setup)

```bash
# Step 1: Add videos to videos/ folder
# Step 2: Convert to MP3
python video_to_mp3.py

# Step 3: Transcribe to JSON
python mp3_to_json.py

# Step 4: Generate embeddings
python preprocess_json.py
```

### 2. Launch the Web Interface

```bash
python app.py
```

Visit `http://localhost:5000` and start asking questions! 🎉

## 🏗️ Project Structure

```
rag-ai-assistant/
├── videos/                 # Your video files
├── models/
│   └── embeddings.joblib   # Generated vector database
├── templates/
│   └── index.html         # Chat UI
├── static/
│   ├── style.css
│   └── script.js
├── app.py                 # Flask backend
└── video_to_mp3.py        # Preprocessing scripts
```

## 🔧 How It Works

1. **Videos → Transcripts**: Extract and timestamp audio content
2. **Transcripts → Vectors**: Convert text to embeddings using BGE-M3
3. **User Question → Search**: Find top 5 relevant segments using similarity
4. **Generate Response**: LLM creates natural answer with video/timestamp references

## 📝 API Usage

```javascript
// POST /ask
fetch('/ask', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: "How do I use flexbox?" })
})
```

## 🔮 Future Enhancements

- Integration with **FAISS / Chroma / Qdrant**
- Multi-language transcription support
- PDF and document-based RAG
- User authentication and profiles
- Automatic video seeking to timestamps
- Streaming LLM responses
