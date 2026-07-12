# RAG-Based-AI-Assistant-System
AI-powered lecture navigation system that retrieves relevant video segments based on user queries. It uses embeddings and semantic search to return the exact timestamp, related content, and a short explanation, enabling quick and efficient learning without manually searching through long lectures.

# 🎓 Lecture AI Assistant (RAG-Based Lecture Question Answering System)

A Retrieval-Augmented Generation (RAG) system that allows users to upload lecture audio/video, automatically transcribes the lecture using Whisper, creates semantic embeddings using Ollama, and answers questions with timestamps from the lecture.

---

# Features

- Upload lecture videos or audio
- Automatic Speech-to-Text using OpenAI Whisper
- Supports Hindi lectures (translated to English)
- Automatic chunk creation
- Semantic embeddings using Ollama (BGE-M3)
- Local vector storage using Joblib
- Ask natural language questions
- Retrieval using cosine similarity
- Answer generation using Llama 3.2
- Displays relevant lecture timestamps

---

# Tech Stack

Frontend
- Streamlit

Backend
- FastAPI
- Uvicorn

Speech-to-Text
- OpenAI Whisper

Embedding Model
- Ollama
- BGE-M3

LLM
- Ollama
- Llama 3.2

Vector Storage
- Joblib
- Pandas

Similarity Search
- Scikit-learn (Cosine Similarity)

---

# Project Structure

```
project/
│
├── app.py
├── streamlit.py
├── processing_upload.py
├── proccesing_incoming.py
├── create_chunks.py
├── read_chunks.py
├── requirements.txt
│
├── audios/
├── jsons/
├── embedding.joblib
│
└── venv/
```

---

# Prerequisites

Install

- Python 3.11+
- Git
- Ollama
- FFmpeg

---

# Install Ollama

Download Ollama

https://ollama.com/download

After installation verify

```bash
ollama --version
```

---

# Pull Required Models

Embedding Model

```bash
ollama pull bge-m3
```

LLM

```bash
ollama pull llama3.2
```

Verify

```bash
ollama list
```

Expected

```
bge-m3
llama3.2
```

---

# Install FFmpeg

Windows

Download

https://www.gyan.dev/ffmpeg/builds/

Extract

Add

```
ffmpeg/bin
```

to PATH.

Verify

```bash
ffmpeg -version
```

---

# Clone Repository

```bash
git clone <repository-url>

cd project
```

---

# Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

# Install Requirements

```bash
pip install -r requirements.txt
```

---

# Verify Whisper

Run

```bash
python
```

```python
import whisper

model = whisper.load_model("tiny")

print("Whisper Working")
```

---

# Start Ollama

Normally Ollama starts automatically.

Verify

```bash
ollama list
```

If needed

```bash
ollama serve
```

---

# Run FastAPI

```bash
python -m uvicorn app:app --reload
```

Expected

```
Application startup complete

Uvicorn running on

http://127.0.0.1:8000
```

---

# Run Streamlit

Open another terminal

Activate virtual environment

```bash
venv\Scripts\activate
```

Run

```bash
streamlit run streamlit.py
```

---

# Workflow

## Step 1

Upload Lecture

Provide

- Lecture Number
- Lecture Title

Choose

- mp3
- mp4
- wav
- m4a

Click

Upload & Process

Pipeline

```
Upload

↓

Whisper

↓

Chunking

↓

Embedding

↓

embedding.joblib
```

---

## Step 2

Ask Questions

Go to

Ask a Question

Example

```
What is a for loop?

Explain arrays.

What is initialization?

Difference between while and for loop?
```

Pipeline

```
Question

↓

Embedding

↓

Cosine Similarity

↓

Top 5 Chunks

↓

Llama 3.2

↓

Answer
```

---

# Supported Lecture Languages

- Hindi
- English
- Mixed Hindi-English

Current Whisper Configuration

```python
language="hi"

task="translate"
```

---

# Supported Formats

- mp3
- mp4
- wav
- m4a
- avi
- mov
- mkv

---

# Troubleshooting

## Ollama Not Running

```bash
ollama list
```

If error

```bash
ollama serve
```

---

## Whisper Error

Install

```bash
pip install openai-whisper
```

Verify

```python
import whisper

print(whisper.load_model("tiny"))
```

---

## Backend Not Reachable

Check

```
http://localhost:8000/docs
```

If unavailable

Restart

```bash
python -m uvicorn app:app --reload
```

---

## FFmpeg Not Found

Install FFmpeg

Verify

```bash
ffmpeg -version
```

---

## Embedding Error

Verify

```bash
ollama list
```

Should contain

```
bge-m3
```

---

## LLM Error

Verify

```bash
ollama list
```

Should contain

```
llama3.2
```

---

## Slow Processing

Current implementation uses CPU.

Recommendations

- Use Faster Whisper
- Use GPU
- Process uploads asynchronously
- Cache transcripts
- Cache embeddings

---

# Future Improvements

- Faster-Whisper
- ChromaDB / FAISS
- Background processing
- Progress bar during upload
- Multiple lecture collections
- User authentication
- PDF support
- Lecture summarization
- Hybrid Retrieval (BM25 + Dense Retrieval)
- LangChain Integration

---


