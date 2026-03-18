from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime

class QueryRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None
    chat_history: Optional[List[Dict]] = []
    uploaded_file_id: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1024

class QueryResponse(BaseModel):
    response: str
    source: str
    agent_used: Optional[str] = None
    conversation_id: str
    timestamp: datetime
    tokens_used: int
    processing_time: float
    references: List[str] = []
    routing: Optional[str] = None

class UploadResponse(BaseModel):
    success: bool
    file_id: str
    filename: str
    file_size: int
    pages: int
    upload_time: datetime

class HealthResponse(BaseModel):
    status: str
    version: str
    models_available: List[str]
    groq_connected: bool
    tavily_connected: bool
    langsmith_connected: bool
    uptime: float

class ModelsResponse(BaseModel):
    models: List[Dict[str, Any]]

class ConfigResponse(BaseModel):
    system_name: str
    version: str
    agents: List[str]
    features: List[str]
    current_model: str
    temperature: float
    max_tokens: int
