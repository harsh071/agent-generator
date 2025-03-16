"""
Core engine for generating LLM agents
"""

import os
from typing import Dict, List, Optional, Any

from agent_generator.core.llm_provider import LLMProvider
from agent_generator.core.code_generator import CodeGenerator
from agent_generator.core.framework_selector import FrameworkSelector
from agent_generator.adapters.base import BaseAdapter
from agent_generator.adapters.factory import AdapterFactory


class AgentGenerationEngine:
    """
    Main engine for generating LLM agents based on user specifications
    """
    
    def __init__(self, model: str = "gpt-4"):
        """
        Initialize the agent generation engine
        
        Args:
            model: The LLM model to use for generation (gpt-4 or claude)
        """
        self.llm_provider = LLMProvider(model)
        self.code_generator = CodeGenerator(self.llm_provider)
        self.framework_selector = FrameworkSelector(self.llm_provider)
        self.adapter_factory = AdapterFactory()
    
    def generate_agent(self, specifications: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an agent based on user specifications
        
        Args:
            specifications: Dictionary containing user specifications for the agent
            
        Returns:
            Dictionary containing generated code and related information
        """
        # Determine the most appropriate framework based on specifications
        framework = self.framework_selector.select_framework(specifications)
        
        # Get the appropriate adapter for the selected framework
        adapter = self.adapter_factory.get_adapter(framework)
        
        # Generate code using the adapter and specifications
        code = self.code_generator.generate(specifications, adapter)
        
        return {
            "framework": framework,
            "code": code,
            "specifications": specifications
        }
    
    def save_agent(self, agent_data: Dict[str, Any], output_dir: str) -> str:
        """
        Save the generated agent to disk
        
        Args:
            agent_data: Dictionary containing the generated agent data
            output_dir: Directory to save the agent to
            
        Returns:
            Path to the saved agent
        """
        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the agent code to the output directory
        code_file = os.path.join(output_dir, "agent.py")
        with open(code_file, "w") as f:
            f.write(agent_data["code"])
        
        # Save any additional files required by the adapter
        adapter = self.adapter_factory.get_adapter(agent_data["framework"])
        adapter.save_additional_files(agent_data, output_dir)
        
        return output_dir
