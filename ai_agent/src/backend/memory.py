from typing import Dict, List
from datetime import datetime

class ConversationMemory:
    def __init__(self):
        self.messages: List[Dict] = []
        self.context: Dict = {}
        self.tool_history: List[Dict] = []

    def add_message(self, role: str, content: str, metadata: Dict = None) -> None:
        """Add a message to the conversation history."""
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self.messages.append(message)

    def add_tool_use(self, tool_name: str, input_data: Dict, output_data: Dict) -> None:
        """Record tool usage in history."""
        tool_use = {
            'tool_name': tool_name,
            'input': input_data,
            'output': output_data,
            'timestamp': datetime.now().isoformat()
        }
        self.tool_history.append(tool_use)

    def get_recent_messages(self, limit: int = 10) -> List[Dict]:
        """Get the most recent messages from history."""
        return self.messages[-limit:]

    def get_relevant_context(self, query: str = None) -> Dict:
        """Get context relevant to the current conversation."""
        # In a more advanced implementation, this could use 
        # semantic search or other relevance mechanisms
        return self.context

    def update_context(self, key: str, value: any) -> None:
        """Update the conversation context."""
        self.context[key] = value

    def clear(self) -> None:
        """Clear all conversation history and context."""
        self.messages = []
        self.context = {}
        self.tool_history = []

    def get_formatted_history(self) -> str:
        """Get formatted conversation history for LLM context."""
        formatted = []
        for msg in self.messages:
            formatted.append(f"{msg['role'].upper()}: {msg['content']}")
        return "\n".join(formatted)
