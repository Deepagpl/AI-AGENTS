import os
from typing import Dict, List, Any
import google.generativeai as genai
from dotenv import load_dotenv
from .memory import ConversationMemory
from .tools.search import SearchTool

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

class AIAgent:
    def __init__(self):
        self.memory = ConversationMemory()
        self.search_tool = SearchTool()
        self.model = genai.GenerativeModel('gemini-pro')
        
        # System prompt to define agent behavior
        self.system_prompt = """
        You are a helpful AI assistant with access to web search capabilities.
        You can search the internet to provide up-to-date information.
        Always be clear about your sources and when you're using search results.
        If you're not sure about something, you should search to verify.
        """

    async def _get_search_results(self, query: str) -> str:
        """Perform web search and format results."""
        results = await self.search_tool.async_search(query)
        return self.search_tool.format_results(results)

    def _build_prompt(self, query: str, search_results: str = None) -> str:
        """Build the complete prompt including context and search results."""
        prompt_parts = [
            self.system_prompt,
            "\nConversation history:",
            self.memory.get_formatted_history(),
            f"\nUser query: {query}"
        ]
        
        if search_results:
            prompt_parts.extend([
                "\nSearch results:",
                search_results
            ])

        return "\n".join(prompt_parts)

    def _should_use_search(self, query: str) -> bool:
        """Determine if the query requires web search."""
        search_indicators = [
            "latest",
            "current",
            "news",
            "recent",
            "update",
            "how to",
            "what is",
            "where can",
            "when did",
            "who is",
            "tell me about",
            "find",
            "search",
            "look up",
            "weather",
            "price",
            "cost"
        ]
        return any(indicator in query.lower() for indicator in search_indicators)

    async def process_message(self, message: str) -> Dict[str, Any]:
        """Process a user message and generate a response."""
        try:
            # Record user message
            self.memory.add_message("user", message)
            
            # Initialize variables
            search_results = None
            search_content = ""
            
            # Perform search if needed
            if self._should_use_search(message):
                try:
                    results = await self._get_search_results(message)
                    if results:
                        search_content = f"\nBased on recent search results:\n{results}"
                        search_results = results
                except Exception as e:
                    search_content = f"\nNote: Search attempted but failed: {str(e)}"
            
            # Build prompt with context
            context = [
                self.system_prompt,
                "\nPrevious conversation:",
                self.memory.get_formatted_history(),
                f"\nUser query: {message}",
                search_content
            ]
            
            # Generate response using Gemini
            response = self.model.generate_content("\n".join(context))
            
            # Format the response
            ai_response = response.text.strip()
            
            # Add search attribution if results were used
            if search_results:
                ai_response += "\n\n(Response includes information from web search)"
            
            # Record AI response
            self.memory.add_message("assistant", ai_response)
            
            # Return formatted response
            return {
                'response': ai_response,
                'used_search': bool(search_results),
                'search_results': search_results,
                'timestamp': self.memory.messages[-1]['timestamp']
            }
            
        except Exception as e:
            error_response = f"I apologize, but I encountered an error: {str(e)}"
            self.memory.add_message("assistant", error_response)
            return {
                'response': error_response,
                'error': str(e),
                'used_search': False,
                'search_results': None,
                'timestamp': self.memory.messages[-1]['timestamp']
            }

    def clear_memory(self) -> None:
        """Clear the agent's conversation memory."""
        self.memory.clear()
