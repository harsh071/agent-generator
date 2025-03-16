"""
OpenAI Assistants adapter for the agent generation engine
"""

import os
from typing import Dict, Any

from agent_generator.adapters.base import BaseAdapter


class OpenAIAssistantsAdapter(BaseAdapter):
    """
    Adapter for OpenAI Assistants framework
    
    Specializes in leveraging OpenAI's agent capabilities
    """
    
    def get_framework_name(self) -> str:
        """
        Get the name of the framework
        
        Returns:
            Name of the framework
        """
        return "openai_assistants"
    
    def get_prompt_template(self) -> str:
        """
        Get the prompt template for generating code with this framework
        
        Returns:
            Prompt template as a string
        """
        return """
Generate {language} code for an LLM agent using the OpenAI Assistants API with the following specifications:

{specifications}

The code should include:
1. All necessary imports for the OpenAI Assistants API
2. Assistant creation and configuration
3. Thread management
4. Message handling
5. Function calling setup if needed
6. Error handling and logging
7. Any additional functionality required by the specifications

Make sure the code follows OpenAI Assistants API best practices and is well-documented.
"""
    
    def post_process_code(self, code: str, specifications: Dict[str, Any]) -> str:
        """
        Post-process the generated code
        
        Args:
            code: Generated code from the LLM
            specifications: Dictionary containing user specifications for the agent
            
        Returns:
            Post-processed code
        """
        # Add standard imports if not present
        standard_imports = [
            "import os",
            "import logging",
            "import time",
            "from typing import List, Dict, Any, Optional",
            "import openai",
            "from openai import OpenAI"
        ]
        
        # Check if imports are already present
        for import_stmt in standard_imports:
            if import_stmt not in code:
                code = import_stmt + "\n" + code
        
        # Add environment variable loading if not present
        if "os.environ.get" not in code and "os.getenv" not in code:
            env_setup = """
# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set up API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
"""
            code = env_setup + "\n" + code
        
        # Add logging setup if not present
        if "logging.basicConfig" not in code:
            logging_setup = """
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
            code = code + "\n" + logging_setup
        
        # Add main function if not present
        if "__main__" not in code:
            main_function = """

if __name__ == "__main__":
    try:
        # Initialize the agent
        agent = OpenAIAssistantAgent()
        
        # Example conversation
        response = agent.chat("Your message here")
        print(f"Assistant: {response}")
    except Exception as e:
        logging.error(f"Error running agent: {e}")
"""
            code = code + "\n" + main_function
        
        return code
    
    def save_additional_files(self, agent_data: Dict[str, Any], output_dir: str) -> None:
        """
        Save any additional files required by the framework
        
        Args:
            agent_data: Dictionary containing the generated agent data
            output_dir: Directory to save the files to
        """
        # Create a .env template file
        env_template = """# OpenAI Assistants Agent Environment Variables
OPENAI_API_KEY=your_openai_api_key_here
"""
        env_file = os.path.join(output_dir, ".env.template")
        with open(env_file, "w") as f:
            f.write(env_template)
        
        # Create a README with usage instructions
        readme = f"""# OpenAI Assistants Agent

This agent was generated using the LLM Agent Generation Engine.

## Setup

1. Copy `.env.template` to `.env` and add your API keys
2. Install the required packages: `pip install -r requirements.txt`
3. Run the agent: `python agent.py`

## Specifications

{agent_data['specifications']}

## Framework

This agent uses the OpenAI Assistants API, which is specialized for leveraging OpenAI's agent capabilities.
"""
        readme_file = os.path.join(output_dir, "README.md")
        with open(readme_file, "w") as f:
            f.write(readme)
        
        # Create a requirements.txt file
        requirements = """openai>=1.0.0
python-dotenv>=1.0.0
"""
        requirements_file = os.path.join(output_dir, "requirements.txt")
        with open(requirements_file, "w") as f:
            f.write(requirements)
    
    def get_requirements(self) -> Dict[str, str]:
        """
        Get the requirements for this framework
        
        Returns:
            Dictionary of package names and versions
        """
        return {
            "openai": ">=1.0.0",
            "python-dotenv": ">=1.0.0"
        }
