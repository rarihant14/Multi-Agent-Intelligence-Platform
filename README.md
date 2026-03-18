# NeuroAgent - Multi-Agent Intelligence Platform

**Powered by LangGraph | Groq | Tavily | LangSmith**

A production-ready multi-agent AI system with an ultra-modern dark theme UI.

## Features

✅ **LangGraph Orchestration** - Graph-based multi-agent system
✅ **4 Intelligent Agents** - Knowledge, Research, Document, Summary
✅ **Real-time Updates** - Live agent status monitoring
✅ **PDF Analysis** - Upload and analyze documents
✅ **Web Search** - Powered by Tavily
✅ **Conversation Memory** - Multi-turn support
✅ **Performance Metrics** - Track response times and tokens

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure .env
```bash
# Add your API keys
GROQ_API_KEY=gsk_your_key_here
TAVILY_API_KEY=your_tavily_key_here
SERVER_IP=your_server_ip
```

### 3. Run
```bash
python app.py
```

### 4. Access
Open browser: `http://SERVER_IP:8000`

## Architecture

- **Frontend**: Dark-themed React-like HTML/CSS/JS
- **Backend**: FastAPI with LangGraph orchestration
- **Agents**: 4 specialized agents with error handling
- **Database**: Conversation memory management

## API Endpoints

- `POST /api/query` - Send query to multi-agent system
- `POST /api/upload` - Upload PDF files
- `GET /api/health` - System health check
- `GET /api/agents/status` - Agent statistics
- `GET /api/models` - Available models
- `POST /api/conversation/clear` - Clear chat

## Requirements

- Python 3.9+
- Groq API Key
- Tavily API Key (for web search)

## Documentation

See LANGGRAPH_SETUP_GUIDE.md for detailed setup
