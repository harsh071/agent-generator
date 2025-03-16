"""
Base adapter interface for framework adapters
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAdapter(ABC):
    """
    Base class for framework adapters
    
    Framework adapters provide a standardized interface between
    generated agents and the underlying frameworks.
    """
    
    @abstractmethod
    def get_framework_name(self) -> str:
        """
        Get the name of the framework
        
        Returns:
            Name of the framework
        """
        pass
    
    @abstractmethod
    def get_prompt_template(self) -> str:
        """
        Get the prompt template for generating code with this framework
        
        Returns:
            Prompt template as a string
        """
        pass
    
    @abstractmethod
    def post_process_code(self, code: str, specifications: Dict[str, Any]) -> str:
        """
        Post-process the generated code
        
        Args:
            code: Generated code from the LLM
            specifications: Dictionary containing user specifications for the agent
            
        Returns:
            Post-processed code
        """
        pass
    
    @abstractmethod
    def save_additional_files(self, agent_data: Dict[str, Any], output_dir: str) -> None:
        """
        Save any additional files required by the framework
        
        Args:
            agent_data: Dictionary containing the generated agent data
            output_dir: Directory to save the files to
        """
        pass
    
    @abstractmethod
    def get_requirements(self) -> Dict[str, str]:
        """
        Get the requirements for this framework
        
        Returns:
            Dictionary of package names and versions
        """
        pass
