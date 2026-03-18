from groq import Groq
import asyncio
from typing import Optional

class KnowledgeAgent:
    def __init__(self, client: Groq):
        self.client = client
    
    async def retrieve_and_answer(
        self, 
        query: str, 
        temperature: float = 0.7, 
        max_tokens: int = 1024,
        model: Optional[str] = None  # ✅ ADD: Accept model parameter
    ) -> str:
        """
        Answer questions using general knowledge
        
        Args:
            query: Question to answer
            temperature: Model temperature
            max_tokens: Max tokens in response
            model: Model to use (e.g., "llama-3.3-70b-versatile")
        """
        await asyncio.sleep(0.1)
        
        # ✅ Use provided model or default
        if model is None:
            model = "llama-3.3-70b-versatile"
        
        print(f"💡 KnowledgeAgent: Using model {model}")
        
        response = self.client.chat.completions.create(
            model=model,  # ✅ USE: Model parameter
            messages=[{"role": "user", "content": query}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content