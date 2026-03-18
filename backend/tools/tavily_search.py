import httpx
import asyncio
from backend.config import settings

class TavilySearch:
    @staticmethod
    async def search(query: str, max_results: int = 5):
        try:
            if not settings.tavily_api_key:
                return "Web search not available (no Tavily API key)"
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": settings.tavily_api_key,
                        "query": query,
                        "max_results": max_results
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    
                    formatted = "Search Results:\n"
                    for i, result in enumerate(results, 1):
                        formatted += f"\n{i}. {result.get('title', 'No title')}\n"
                        formatted += f"   {result.get('content', 'No content')}\n"
                        formatted += f"   Source: {result.get('url', 'No URL')}\n"
                    
                    return formatted
                else:
                    return "Search request failed"
        except Exception as e:
            return f"Search error: {str(e)}"

tavily_search = TavilySearch()
