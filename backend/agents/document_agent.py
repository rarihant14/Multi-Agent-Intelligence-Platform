from groq import Groq
from backend.tools.pdf_parser import pdf_parser
import asyncio
from typing import Optional

class DocumentAgent:
    def __init__(self, client: Groq):
        self.client = client
    
    async def analyze(
        self, 
        query: str, 
        file_id: str, 
        temperature: float = 0.7, 
        max_tokens: int = 1024,
        model: Optional[str] = None  # ✅ ADD: Accept model parameter
    ) -> str:
        """
        Analyze documents and answer questions
        
        Args:
            query: Question about document
            file_id: Uploaded file ID
            temperature: Model temperature
            max_tokens: Max tokens in response
            model: Model to use (e.g., "llama-3.3-70b-versatile")
        """
        await asyncio.sleep(0.1)
        
        # ✅ Use provided model or default
        if model is None:
            model="openai/gpt-oss-120b",
        
        print(f"📄 DocumentAgent: Using model {model}")
        
        try:
            from backend.config import settings
            file_path = f"{settings.upload_dir}/{file_id}"
            parsed = pdf_parser.parse_pdf(file_path)
            content = parsed.get("full_text", "")[:2000]
            prompt = f"Document content:\n{content}\n\nQuestion: {query}"
        except Exception as e:
            print(f"⚠️ PDF parsing error: {e}, using direct query")
            prompt = query
        
        response = self.client.chat.completions.create(
            model=model,  # ✅ USE: Model parameter
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
           
    