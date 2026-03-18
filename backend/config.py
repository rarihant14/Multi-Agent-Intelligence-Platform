import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    langsmith_api_key: str = os.getenv("LANGSMITH_API_KEY", "")
    
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    groq_temperature: float = float(os.getenv("GROQ_TEMPERATURE", "0.7"))
    groq_max_tokens: int = int(os.getenv("GROQ_MAX_TOKENS", "1024"))
    
    langsmith_enabled: bool = os.getenv("LANGSMITH_ENABLED", "false").lower() == "true"
    langsmith_project: str = os.getenv("LANGSMITH_PROJECT", "neuroagent")
    
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    app_name: str = "NeuroAgent - Multi-Agent Intelligence Platform"
    app_version: str = "2.0.0"
    
    server_host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    server_port: int = int(os.getenv("SERVER_PORT", "8000"))
    server_ip: str = os.getenv("SERVER_IP", "localhost")
    
    upload_dir: str = os.getenv("UPLOAD_DIR", "uploads")
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", "50")) * 1024 * 1024
    vector_db_path: str = os.getenv("VECTOR_DB_PATH", "data/chroma_db")
    max_conversation_length: int = 50
    summarization_threshold: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
os.makedirs(settings.upload_dir, exist_ok=True)
