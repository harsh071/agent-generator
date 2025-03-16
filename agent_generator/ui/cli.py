"""
Command-line interface for the agent generation engine
"""

import os
import json
from typing import Dict, Any, List, Optional

from agent_generator.core.engine import AgentGenerationEngine


class CLI:
    """
    Command-line interface for the agent generation engine
    """
    
    def __init__(self, engine: AgentGenerationEngine):
        """
        Initialize the CLI
        
        Args:
            engine: Agent generation engine
        """
        self.engine = engine
    
    def run(self):
        """
        Run the CLI
        """
        print("=" * 50)
        print("LLM Agent Generation Engine - CLI")
        print("=" * 50)
        print("\nWelcome! Let's create a custom LLM agent.")
        
        # Collect specifications
        specifications = self._collect_specifications()
        
        # Generate the agent
        print("\nGenerating agent code...")
        agent_data = self.engine.generate_agent(specifications)
        
        # Save the agent
        output_dir = self._get_output_directory()
        saved_path = self.engine.save_agent(agent_data, output_dir)
        
        print(f"\nAgent successfully generated and saved to: {saved_path}")
        print("\nYou can now use your agent by following the instructions in the README.md file.")
    
    def _collect_specifications(self) -> Dict[str, Any]:
        """
        Collect agent specifications from the user
        
        Returns:
            Dictionary containing user specifications for the agent
        """
        specifications = {}
        
        # Basic information
        print("\n--- Basic Information ---")
        specifications["name"] = input("Agent name: ")
        specifications["description"] = input("Agent description: ")
        specifications["language"] = self._select_option(
            "Programming language", ["python", "javascript"], "python"
        )
        
        # Framework selection
        print("\n--- Framework Selection ---")
        print("Available frameworks:")
        print("1. LlamaIndex - Best for document retrieval and RAG applications")
        print("2. LangChain - Best for workflow and chain-of-thought operations")
        print("3. SmallAgents - Best for lightweight, specific-purpose agents")
        print("4. OpenAI Assistants - Best for leveraging OpenAI's agent capabilities")
        print("5. Auto-select based on requirements")
        
        framework_choice = input("Select a framework (1-5, default: 5): ").strip() or "5"
        framework_map = {
            "1": "llamaindex",
            "2": "langchain",
            "3": "smallagents",
            "4": "openai_assistants"
        }
        
        if framework_choice in framework_map:
            specifications["framework"] = framework_map[framework_choice]
        
        # Capabilities
        print("\n--- Agent Capabilities ---")
        capabilities = []
        print("Select agent capabilities (comma-separated numbers):")
        print("1. Document retrieval")
        print("2. Question answering")
        print("3. Web browsing")
        print("4. Tool usage")
        print("5. Memory/context retention")
        print("6. Chain-of-thought reasoning")
        print("7. Custom capability")
        
        capability_choices = input("Capabilities (e.g., 1,3,4): ").strip()
        capability_map = {
            "1": "document_retrieval",
            "2": "question_answering",
            "3": "web_browsing",
            "4": "tool_usage",
            "5": "memory_retention",
            "6": "chain_of_thought"
        }
        
        for choice in capability_choices.split(","):
            choice = choice.strip()
            if choice in capability_map:
                capabilities.append(capability_map[choice])
            elif choice == "7":
                custom_capability = input("Enter custom capability: ").strip()
                capabilities.append(custom_capability)
        
        specifications["capabilities"] = capabilities
        
        # Use case
        print("\n--- Use Case ---")
        specifications["use_case"] = input("Describe the specific use case for this agent: ")
        
        # Advanced options
        print("\n--- Advanced Options ---")
        if self._confirm("Do you want to configure advanced options?"):
            # Model selection
            specifications["model"] = self._select_option(
                "LLM model", ["gpt-4", "gpt-3.5-turbo", "claude-2", "claude-instant"], "gpt-4"
            )
            
            # Custom requirements
            if self._confirm("Do you have any custom requirements?"):
                specifications["custom_requirements"] = input("Enter custom requirements: ")
            
            # API keys
            if self._confirm("Do you want to configure API keys now?"):
                api_keys = {}
                api_keys["openai"] = input("OpenAI API key (leave blank to skip): ")
                api_keys["anthropic"] = input("Anthropic API key (leave blank to skip): ")
                
                # Only add non-empty keys
                specifications["api_keys"] = {k: v for k, v in api_keys.items() if v}
        
        return specifications
    
    def _get_output_directory(self) -> str:
        """
        Get the output directory for the generated agent
        
        Returns:
            Path to the output directory
        """
        default_dir = os.path.join(os.getcwd(), "generated_agent")
        output_dir = input(f"\nOutput directory (default: {default_dir}): ").strip() or default_dir
        
        # Ensure the directory doesn't already exist
        if os.path.exists(output_dir):
            if not self._confirm(f"Directory {output_dir} already exists. Overwrite?"):
                i = 1
                while os.path.exists(f"{output_dir}_{i}"):
                    i += 1
                output_dir = f"{output_dir}_{i}"
                print(f"Using {output_dir} instead.")
        
        return output_dir
    
    def _confirm(self, message: str) -> bool:
        """
        Ask for user confirmation
        
        Args:
            message: Confirmation message
            
        Returns:
            True if confirmed, False otherwise
        """
        response = input(f"{message} (y/n): ").strip().lower()
        return response == "y" or response == "yes"
    
    def _select_option(self, name: str, options: List[str], default: str) -> str:
        """
        Let the user select an option from a list
        
        Args:
            name: Name of the option
            options: List of available options
            default: Default option
            
        Returns:
            Selected option
        """
        print(f"\n{name} options:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        default_idx = options.index(default) + 1
        choice = input(f"Select {name.lower()} (1-{len(options)}, default: {default_idx}): ").strip() or str(default_idx)
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except ValueError:
            pass
        
        return default
