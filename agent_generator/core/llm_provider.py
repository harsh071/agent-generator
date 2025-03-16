"""
LLM Provider module for interacting with language models
"""

import os
from typing import Dict, List, Optional, Any

import openai
from anthropic import Anthropic


class LLMProvider:
    """
    Provider for interacting with different language models
    """
    
    def __init__(self, model: str = "gpt-4"):
        """
        Initialize the LLM provider
        
        Args:
            model: The LLM model to use (gpt-4 or claude)
        """
        self.model = model
        
        # Initialize API clients
        if self.model.startswith("gpt"):
            self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif self.model.startswith("claude"):
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        else:
            raise ValueError(f"Unsupported model: {model}")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, 
                 temperature: float = 0.7, max_tokens: int = 4000) -> str:
        """
        Generate text using the configured LLM
        
        Args:
            prompt: The user prompt to send to the LLM
            system_prompt: Optional system prompt for context
            temperature: Controls randomness (0 to 1)
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated text from the LLM
        """
        if self.model.startswith("gpt"):
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
            
        elif self.model.startswith("claude"):
            system = system_prompt or ""
            response = self.client.messages.create(
                model=self.model,
                system=system,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.content[0].text
    
    def generate_code(self, specifications: Dict[str, Any], language: str = "python") -> str:
        """
        Generate code based on specifications
        
        Args:
            specifications: Dictionary containing specifications for the code
            language: Programming language to generate (python or javascript)
            
        Returns:
            Generated code as a string
        """
        system_prompt = f"""You are an expert {language} developer specializing in LLM agents.
Your task is to generate clean, well-documented {language} code based on the provided specifications.
Follow best practices and include appropriate error handling.
Only output the code without any explanations or markdown formatting."""
        
        prompt = f"""Generate {language} code for an LLM agent with the following specifications:
{specifications}

The code should be complete and ready to run, including all necessary imports and class/function definitions."""
        
        return self.generate(prompt, system_prompt, temperature=0.2)
