"""
Factory for creating framework adapters
"""

from typing import Dict, Type

from agent_generator.adapters.base import BaseAdapter
from agent_generator.adapters.llamaindex_adapter import LlamaIndexAdapter
from agent_generator.adapters.langchain_adapter import LangChainAdapter
from agent_generator.adapters.smallagents_adapter import SmallAgentsAdapter
from agent_generator.adapters.openai_assistants_adapter import OpenAIAssistantsAdapter


class AdapterFactory:
    """
    Factory for creating framework adapters
    """
    
    def __init__(self):
        """
        Initialize the adapter factory
        """
        self.adapters: Dict[str, Type[BaseAdapter]] = {
            "llamaindex": LlamaIndexAdapter,
            "langchain": LangChainAdapter,
            "smallagents": SmallAgentsAdapter,
            "openai_assistants": OpenAIAssistantsAdapter
        }
    
    def get_adapter(self, framework: str) -> BaseAdapter:
        """
        Get an adapter for the specified framework
        
        Args:
            framework: Name of the framework
            
        Returns:
            Adapter instance for the framework
            
        Raises:
            ValueError: If the framework is not supported
        """
        if framework not in self.adapters:
            raise ValueError(f"Unsupported framework: {framework}")
        
        return self.adapters[framework]()
