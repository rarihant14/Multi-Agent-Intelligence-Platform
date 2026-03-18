"""
Research Agent - Updated to use selected model
"""

from groq import Groq
from backend.tools.tavily_search import tavily_search
import asyncio
from typing import Optional


class ResearchAgent:
    def __init__(self, client: Groq):
        self.client = client
    
    async def research(
        self, 
        query: str, 
        temperature: float = 0.7, 
        max_tokens: int = 1024,
        model: Optional[str] = None  # NEW: Accept model parameter
    ) -> str:
        """
        Research using web search and selected model
        
        Args:
            query: Research query
            temperature: Model temperature
            max_tokens: Max tokens in response
            model: Model to use (e.g., "llama-3.3-70b-versatile")
        """
        await asyncio.sleep(0.1)
        
        # Use provided model or default
        if model is None:
            model = "llama-3.3-70b-versatile"
        
        print(f"🔍 ResearchAgent: Using model {model}")
        
        try:
            # Get search results
            search_results = await tavily_search.search(query)
            prompt = f"Based on these search results:\n{search_results}\n\nAnswer: {query}"
        except Exception as e:
            print(f"⚠️ Search failed: {e}, using direct query")
            prompt = query
        
        # Use selected model
        response = self.client.chat.completions.create(
            model=model,  # Use the selected model!
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content