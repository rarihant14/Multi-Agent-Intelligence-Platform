# 🚀 Multi-Agent  System  
**Powered by LangGraph | Groq | Tavily | LangSmith**

A  multi-agent AI system with a modern dark-themed UI, designed for intelligent task orchestration, document analysis, and real-time agent collaboration.

---

## ✨ Features

- 🧠 LangGraph Orchestration  
  Graph-based execution for multi-agent workflows  

- 🤖 4 Intelligent Agents  
  - Knowledge Agent  
  - Research Agent  
  - Document Agent  
  - Summary Agent  

- ⚡ Real-time Updates  
  Live monitoring of agent execution and status  

- 📄 PDF Analysis  
  Upload and extract insights from documents  

- 🌐 Web Search Integration  
  Powered by Tavily for real-time information  

- 💬 Conversation Memory  
  Supports multi-turn contextual conversations  

- 📊 Performance Metrics  
  - Response time tracking  
  - Token usage monitoring  

---

## 🛠️ Tech Stack

- Frontend: HTML, CSS, JavaScript (Dark UI)  
- Backend: FastAPI  
- AI Engine: LangGraph + Groq  
- Search: Tavily  
- Monitoring: LangSmith  

---

## ⚙️ Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=gsk_your_key_here
TAVILY_API_KEY=your_tavily_key_here
SERVER_IP=127.0.0.1
```

### 3. Run the Application

```bash
python app.py
```

### 4. Access the App

Open in browser:

```
http://127.0.0.1:8000
```

---

## 🧩 Architecture Overview

- Frontend  
  Modern dark-themed UI (React-like structure using vanilla JS)  

- Backend  
  FastAPI server with LangGraph orchestration  

- Agents System  
  - Modular design  
  - Error handling per agent  
  - Independent execution + coordination  

- Database  
  - Conversation memory storage  
  - Context-aware responses  

---

## 🔌 API Endpoints

- POST `/api/query` → Send query to multi-agent system  
- POST `/api/upload` → Upload PDF documents  
- GET `/api/health` → System health check  
- GET `/api/agents/status` → Agent performance stats  
- GET `/api/models` → List available models  
- POST `/api/conversation/clear` → Clear chat history  

---

## 📦 Requirements

- Python 3.9+  
- Groq API Key  
- Tavily API Key  

---

## 💡 Use Cases

- AI Research Assistant  
- Document Analyzer  
- Smart Chat System  
- Knowledge Retrieval Engine  
- Multi-Agent Experimentation  

---

## 🧠 Future Improvements

- Add authentication system  
- Deploy on cloud (AWS / GCP)   
- Integrate vector DB (FAISS / Pinecone)  
- Fine-tuned agent routing  
