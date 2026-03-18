import asyncio
import time
import uuid
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("⚠️ Groq not available, will try alternative providers")

from langgraph.graph import StateGraph, END
from backend.config import settings


class LangGraphOrchestrator:
    """Multi-agent orchestrator with updated model support"""

    def __init__(self):
        try:
            # Try to initialize with Groq first (for compatibility)
            if GROQ_AVAILABLE:
                self.client = Groq(api_key=settings.groq_api_key)
                self.api_type = "groq"
            else:
                # You can add alternative API providers here
                self.client = None
                self.api_type = "generic"
            
            self.default_model = 'llama-3.3-70b-versatile'
            
            # Model configurations
            self.models = {
                'openai/gpt-oss-120b': {
                    'name': 'GPT-OSS 120B',
                    'context': 200000,
                    'max_tokens': 4000
                },
                'llama-3.3-70b-versatile': {
                    'name': 'Llama 3.3 70B',
                    'context': 8000,
                    'max_tokens': 4000
                },
                'llama-3.1-8b-instant': {
                    'name': 'Llama 3.1 8B',
                    'context': 8000,
                    'max_tokens': 4000
                }
            }
        except Exception as e:
            print(f"❌ Failed to initialize API client: {e}")
            raise
        
        self.conversation_histories: Dict[str, Any] = {}
        self.agent_stats = {
            'knowledge': {'success': 0, 'error': 0},
            'research': {'success': 0, 'error': 0},
            'document': {'success': 0, 'error': 0},
            'summary': {'success': 0, 'error': 0},
        }
        
        self.graph = self._build_graph()
        print("✅ LangGraph Orchestrator initialized with updated models")
        print(f"   Available models: GPT-OSS 120B, Llama 3.3 70B, Llama 3.1 8B")

    def _build_graph(self):
        """Build simple LangGraph workflow"""
        workflow = StateGraph(dict)
        
        workflow.add_node("input", self._input_node)
        workflow.add_node("router", self._routing_node)
        workflow.add_node("agent", self._agent_node)
        workflow.add_node("output", self._output_node)
        
        workflow.set_entry_point("input")
        workflow.add_edge("input", "router")
        workflow.add_edge("router", "agent")
        workflow.add_edge("agent", "output")
        workflow.add_edge("output", END)
        
        return workflow.compile()

    async def process_query(
        self,
        query: str,
        conversation_id: Optional[str] = None,
        chat_history: Optional[List[Dict]] = None,
        uploaded_file_id: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process query through LangGraph with model selection"""
        
        start_time = time.time()
        
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        
        if conversation_id not in self.conversation_histories:
            self.conversation_histories[conversation_id] = {
                "messages": [],
                "created_at": datetime.now().isoformat()
            }
        
        # Use provided model or default
        selected_model = model or self.default_model
        
        #  model
        if selected_model not in self.models:
            print(f"⚠️ Unknown model: {selected_model}, using default: {self.default_model}")
            selected_model = self.default_model
        
        print(f"🎯 Using model: {self.models[selected_model]['name']}")
        
        initial_state = {
            "query": query,
            "conversation_id": conversation_id,
            "chat_history": chat_history or [],
            "uploaded_file_id": uploaded_file_id,
            "temperature": temperature,
            "max_tokens": min(max_tokens, self.models[selected_model]['max_tokens']),
            "model": selected_model,
            "routing_decision": {},
            "selected_agent": "knowledge",
            "response": "",
            "source": "",
            "tokens_used": 0,
            "error": None
        }
        
        try:
            final_state = await asyncio.to_thread(
                self.graph.invoke,
                initial_state
            )
            
            processing_time = time.time() - start_time
            
            return {
                "response": final_state.get("response", ""),
                "source": final_state.get("source", "Knowledge Agent"),
                "agent_used": final_state.get("selected_agent", "knowledge"),
                "conversation_id": conversation_id,
                "timestamp": datetime.now(),
                "tokens_used": final_state.get("tokens_used", 0),
                "processing_time": processing_time,
                "references": [],
                "routing": final_state.get("selected_agent", "knowledge"),
                "model": selected_model,
                "model_name": self.models[selected_model]['name']
            }
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return {
                "response": f"Error: {str(e)}",
                "source": "Error Handler",
                "agent_used": "error",
                "conversation_id": conversation_id,
                "timestamp": datetime.now(),
                "tokens_used": 0,
                "processing_time": time.time() - start_time,
                "error": str(e),
                "model": selected_model,
                "model_name": self.models[selected_model]['name']
            }

    # nodes for the LangGraph workflow

    def _input_node(self, state: dict) -> dict:
        """Input validation"""
        model_name = self.models[state.get('model', self.default_model)]['name']
        print(f"🔹 INPUT: {state['query'][:50]} [Model: {model_name}]")
        return state

    def _routing_node(self, state: dict) -> dict:
        """Route to appropriate agent"""
        print("🔹 ROUTING: Analyzing query...")
        
        query_lower = state['query'].lower()
        
        if state.get('uploaded_file_id'):
            agent = 'document'
            print(f"✅ ROUTE: Document (PDF uploaded)")
        elif any(word in query_lower for word in ['summarize', 'summary', 'condense', 'shorten']):
            agent = 'summary'
            print(f"✅ ROUTE: Summary")
        elif any(word in query_lower for word in ['search', 'latest', 'current', 'news', 'trending']):
            agent = 'research'
            print(f"✅ ROUTE: Research")
        else:
            agent = 'knowledge'
            print(f"✅ ROUTE: Knowledge")
        
        state['selected_agent'] = agent
        return state

    def _agent_node(self, state: dict) -> dict:
        """Execute selected agent with chosen model"""
        agent = state['selected_agent']
        query = state['query']
        model = state.get('model', self.default_model)
        model_name = self.models[model]['name']
        
        print(f"🔹 AGENT: Executing {agent} with {model_name}...")
        
        try:
            response = self._call_model(
                query,
                state['temperature'],
                state['max_tokens'],
                agent,
                model
            )
            
            state['response'] = response
            state['tokens_used'] = len(response.split())
            state['source'] = f"{agent.capitalize()} Agent"
            
            self.agent_stats[agent]['success'] += 1
            print(f"✅ {agent}: Got response from {model_name}")
            
        except Exception as e:
            print(f"❌ {agent} Error: {e}")
            state['response'] = f"Error from {agent} agent: {str(e)}"
            state['source'] = f"{agent.capitalize()} (Error)"
            self.agent_stats[agent]['error'] += 1
        
        return state

    def _output_node(self, state: dict) -> dict:
        """Format output"""
        print(f"🔹 OUTPUT: Preparing response...")
        
        if not state.get('response'):
            state['response'] = "No response generated"
        
        if not state.get('source'):
            state['source'] = 'Unknown Agent'
        
        print(f"✅ Ready to return")
        return state

    def _call_model(self, query: str, temperature: float, max_tokens: int, agent: str, model: str) -> str:
        """Call the selected model with appropriate system prompt"""
        
        # System prompts based on agent
        if agent == 'summary':
            system = "You are a summarization expert. Provide concise summaries."
        elif agent == 'research':
            system = "You are a research expert. Provide detailed, informative responses based on your knowledge."
        elif agent == 'document':
            system = "You are a document analysis expert. Answer questions about provided documents."
        else:
            system = "You are a helpful assistant. Answer questions clearly and concisely."
        
        # Call the appropriate API based on what's available
        if self.api_type == "groq" and self.client:
            # Use Groq API (which can access these models if configured)
            response = self.client.chat.completions.create(
                model=model,  # Use the selected model ID
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": query}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        else:
            # Fallback: return a message indicating model is being used
            model_name = self.models[model]['name']
            return f"[Response from {model_name}] I'm ready to help with: {query[:100]}..."

    def get_agent_stats(self) -> Dict[str, Any]:
        """Get statistics"""
        return self.agent_stats

    def clear_conversation(self, conversation_id: str) -> bool:
        """Clear conversation"""
        if conversation_id in self.conversation_histories:
            del self.conversation_histories[conversation_id]
            return True
        return False


async def create_orchestrator() -> LangGraphOrchestrator:
    """Create orchestrator"""
    return LangGraphOrchestrator()