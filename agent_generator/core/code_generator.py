"""
Code Generator module for generating agent code
"""

from typing import Dict, Any

from agent_generator.core.llm_provider import LLMProvider
from agent_generator.adapters.base import BaseAdapter


class CodeGenerator:
    """
    Generator for creating agent code based on specifications and framework adapters
    """
    
    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize the code generator
        
        Args:
            llm_provider: LLM provider for generating code
        """
        self.llm_provider = llm_provider
    
    def generate(self, specifications: Dict[str, Any], adapter: BaseAdapter) -> str:
        """
        Generate agent code based on specifications and adapter
        
        Args:
            specifications: Dictionary containing user specifications for the agent
            adapter: Framework adapter to use for code generation
            
        Returns:
            Generated code as a string
        """
        # Get the prompt template from the adapter
        prompt_template = adapter.get_prompt_template()
        
        # Prepare the prompt with specifications
        prompt = prompt_template.format(
            specifications=self._format_specifications(specifications),
            framework=adapter.get_framework_name(),
            language=specifications.get("language", "python")
        )
        
        # Generate code using the LLM provider
        code = self.llm_provider.generate_code(
            specifications, 
            language=specifications.get("language", "python")
        )
        
        # Post-process the code with the adapter
        processed_code = adapter.post_process_code(code, specifications)
        
        return processed_code
    
    def _format_specifications(self, specifications: Dict[str, Any]) -> str:
        """
        Format specifications for inclusion in the prompt
        
        Args:
            specifications: Dictionary containing user specifications for the agent
            
        Returns:
            Formatted specifications as a string
        """
        formatted = ""
        for key, value in specifications.items():
            if isinstance(value, dict):
                formatted += f"{key}:\n"
                for sub_key, sub_value in value.items():
                    formatted += f"  {sub_key}: {sub_value}\n"
            elif isinstance(value, list):
                formatted += f"{key}:\n"
                for item in value:
                    formatted += f"  - {item}\n"
            else:
                formatted += f"{key}: {value}\n"
        
        return formatted
