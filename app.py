
import os
import webbrowser
import time
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from datetime import datetime
from contextlib import asynccontextmanager

from backend.config import settings

BASE_DIR = Path(__file__).parent
FRONTEND_DIR = BASE_DIR / "frontend"

print(f"""
Initializing NeuroAgent with Fixed Static File Serving...       
Frontend: {str(FRONTEND_DIR)}

""")

orchestrator = None
start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """App startup and shutdown"""
    global orchestrator
    
    print("🚀 Starting NeuroAgent...")
    
    try:
        from backend.agents.orchestrator_langgraph import create_orchestrator
        orchestrator = await create_orchestrator()
        print("✅ Orchestrator ready")
        
        def open_browser():
            time.sleep(2)
            try:
                url = "http://localhost:8000"
                webbrowser.open(url)
                print(f"🌐 Browser opened: {url}")
            except:
                pass
        
        import threading
        threading.Thread(target=open_browser, daemon=True).start()
        
        print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  ✅ NeuroAgent is READY!                                         ║
║                                                                  ║
║  🌐 Open: http://localhost:8000                                 ║
║  📚 API Docs: http://localhost:8000/docs                        ║
║                                                                  ║
║  🤖 LangGraph Multi-Agent System Active                         ║
║  🎯 Model Selection Enabled                                     ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
        """)
    
    except Exception as e:
        print(f"❌ Startup Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    
    yield
    
    print("🛑 Shutting down...")


app = FastAPI(
    title="NeuroAgent",
    description="Multi-Agent AI System with Advanced Model Selection",
    version="2.2.0",
    lifespan=lifespan
)


# Static file serving with improved logging and error handling
if FRONTEND_DIR.exists():
    print(f"\n📁 Setting up static files...")
    
    # ✅ FIX: Mount CSS directory
    css_dir = FRONTEND_DIR / "css"
    if css_dir.exists():
        print(f"   ✅ Mounting CSS at /css")
        app.mount("/css", StaticFiles(directory=str(css_dir)), name="css")
    else:
        print(f"   ⚠️ CSS directory not found at {css_dir}")
    
    # ✅ FIX: Mount JS directory
    js_dir = FRONTEND_DIR / "js"
    if js_dir.exists():
        print(f"   ✅ Mounting JS at /js")
        app.mount("/js", StaticFiles(directory=str(js_dir)), name="js")
    else:
        print(f"   ⚠️ JS directory not found at {js_dir}")
    
    # ✅ FIX: Mount all frontend as static
    print(f"   ✅ Mounting frontend at /static")
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
    
    print(f"   ✅ All static files mounted successfully\n")
else:
    print(f"   ⚠️ Frontend directory not found at {FRONTEND_DIR}")


#Routes for serving frontend

@app.get("/")
async def serve_root():
    """Serve main HTML page"""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        print(f"📄 Serving: {index_path}")
        return FileResponse(index_path, media_type="text/html")
    else:
        print(f"❌ index.html not found at {index_path}")
        return {"error": "index.html not found", "path": str(index_path)}


@app.get("/index.html")
async def serve_index():
    """Serve index.html directly"""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path, media_type="text/html")
    return {"error": "index.html not found"}

# API Routes

@app.post("/api/query")
async def query(request: dict):
    """Process query with selected model"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not ready")
    
    try:
        selected_model = request.get('model', 'llama-3.3-70b-versatile')
        
        print(f"📊 Model selected: {selected_model}")
        
        result = await orchestrator.process_query(
            query=request.get('query', ''),
            conversation_id=request.get('conversation_id'),
            chat_history=request.get('chat_history', []),
            uploaded_file_id=request.get('uploaded_file_id'),
            temperature=request.get('temperature', 0.7),
            max_tokens=request.get('max_tokens', 1024),
            model=selected_model
        )
        
        return {
            **result,
            "model_used": selected_model
        }
    except Exception as e:
        print(f"❌ Query Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload PDF"""
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files allowed")
        
        file_path = os.path.join(settings.upload_dir, file.filename)
        contents = await file.read()
        
        with open(file_path, 'wb') as f:
            f.write(contents)
        
        return {
            "success": True,
            "file_id": file.filename,
            "filename": file.filename,
            "file_size": len(contents),
            "pages": 0,
            "upload_time": str(datetime.now())
        }
    except Exception as e:
        print(f"❌ Upload Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "version": "2.2.0",
        "features": ["model_selection", "langgraph", "multi_agent"],
        "uptime": time.time() - start_time,
        "groq_connected": bool(settings.groq_api_key)
    }


@app.get("/api/models")
async def get_models():
    """Get available models"""
    return {
        "models": [
            {
                "id": "openai/gpt-oss-120b",
                "name": "GPT-OSS 120B",
                "provider": "OpenAI",
                "context": 200000,
                "speed": "Fast",
                "cost": "Medium"
            },
            {
                "id": "llama-3.3-70b-versatile",
                "name": "Llama 3.3 70B",
                "provider": "Meta",
                "context": 8000,
                "speed": "Very fast",
                "cost": "Low"
            },
            {
                "id": "llama-3.1-8b-instant",
                "name": "Llama 3.1 8B",
                "provider": "Meta",
                "context": 8000,
                "speed": "Ultra-fast",
                "cost": "Very low"
            }
        ],
        "default_model": "llama-3.3-70b-versatile"
    }


@app.get("/api/config")
async def get_config():
    """Get system config"""
    return {
        "system_name": settings.app_name,
        "version": "2.2.0",
        "agents": ["Knowledge", "Research", "Document", "Summary"],
        "features": ["Model Selection", "LangGraph", "Web Search", "PDF Analysis"],
        "model_selection_enabled": True
    }


@app.get("/api/agents/status")
async def agents_status():
    """Get agent status"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not ready")
    
    stats = orchestrator.get_agent_stats()
    return {
        "agents": [
            {"id": "knowledge", "name": "Knowledge", "status": "ready", "success": stats.get("knowledge", {}).get("success", 0), "errors": stats.get("knowledge", {}).get("error", 0)},
            {"id": "research", "name": "Research", "status": "ready", "success": stats.get("research", {}).get("success", 0), "errors": stats.get("research", {}).get("error", 0)},
            {"id": "document", "name": "Document", "status": "ready", "success": stats.get("document", {}).get("success", 0), "errors": stats.get("document", {}).get("error", 0)},
            {"id": "summary", "name": "Summary", "status": "ready", "success": stats.get("summary", {}).get("success", 0), "errors": stats.get("summary", {}).get("error", 0)}
        ]
    }


@app.post("/api/conversation/clear")
async def clear_conversation(data: dict):
    """Clear chat"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not ready")
    
    conversation_id = data.get("conversation_id")
    if not conversation_id:
        raise HTTPException(status_code=400, detail="No conversation_id")
    
    orchestrator.clear_conversation(conversation_id)
    return {"success": True}



if __name__ == "__main__":
    import uvicorn
    
    print(f"""
Starting server...
URL: http://localhost:8000


Press Ctrl+C to stop
    """)
    
uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False
    )