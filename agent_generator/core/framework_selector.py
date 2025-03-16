"""
Framework Selector module for determining the most appropriate framework
"""

from typing import Dict, Any

from agent_generator.core.llm_provider import LLMProvider


class FrameworkSelector:
    """
    Selector for determining the most appropriate framework based on specifications
    """
    
    FRAMEWORKS = ["llamaindex", "langchain", "smallagents", "openai_assistants"]
    
    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize the framework selector
        
        Args:
            llm_provider: LLM provider for analysis
        """
        self.llm_provider = llm_provider
        
        # Framework capabilities and use cases
        self.framework_capabilities = {
            "llamaindex": {
                "document_retrieval": 0.9,
                "rag": 0.95,
                "indexing": 0.9,
                "query_engine": 0.85,
                "document_processing": 0.8
            },
            "langchain": {
                "workflow": 0.9,
                "chain_of_thought": 0.95,
                "tool_use": 0.85,
                "memory": 0.8,
                "agent_orchestration": 0.9
            },
            "smallagents": {
                "lightweight": 0.95,
                "specific_purpose": 0.9,
                "efficiency": 0.85,
                "simplicity": 0.9
            },
            "openai_assistants": {
                "openai_integration": 0.95,
                "function_calling": 0.9,
                "retrieval": 0.8,
                "code_interpreter": 0.85,
                "vision": 0.8
            }
        }
    
    def select_framework(self, specifications: Dict[str, Any]) -> str:
        """
        Select the most appropriate framework based on specifications
        
        Args:
            specifications: Dictionary containing user specifications for the agent
            
        Returns:
            Name of the selected framework
        """
        # Check if the user explicitly specified a framework
        if "framework" in specifications:
            requested_framework = specifications["framework"].lower()
            if requested_framework in self.FRAMEWORKS:
                return requested_framework
        
        # Use LLM to analyze requirements if complex
        if self._is_complex_specification(specifications):
            return self._analyze_with_llm(specifications)
        
        # Otherwise use rule-based selection
        return self._rule_based_selection(specifications)
    
    def _is_complex_specification(self, specifications: Dict[str, Any]) -> bool:
        """
        Determine if the specifications are complex enough to warrant LLM analysis
        
        Args:
            specifications: Dictionary containing user specifications for the agent
            
        Returns:
            True if complex, False otherwise
        """
        # Check if there are multiple capabilities requested
        capabilities = specifications.get("capabilities", [])
        if isinstance(capabilities, list) and len(capabilities) > 3:
            return True
        
        # Check if there are custom requirements
        if "custom_requirements" in specifications:
            return True
        
        return False
    
    def _analyze_with_llm(self, specifications: Dict[str, Any]) -> str:
        """
        Use the LLM to analyze complex specifications and recommend a framework
        
        Args:
            specifications: Dictionary containing user specifications for the agent
            
        Returns:
            Name of the selected framework
        """
        system_prompt = """You are an expert in LLM agent frameworks. Your task is to analyze the
provided specifications and recommend the most appropriate framework from the following options:
- LlamaIndex: Best for document retrieval and RAG applications
- LangChain: Best for workflow and chain-of-thought operations
- SmallAgents: Best for lightweight, specific-purpose agents
- OpenAI Assistants: Best for leveraging OpenAI's agent capabilities

Respond with ONLY the name of the recommended framework in lowercase, with no additional text."""
        
        prompt = f"""Based on the following agent specifications, which framework would be most appropriate?

Specifications:
{specifications}

Consider the strengths and weaknesses of each framework and choose the one that best aligns with these requirements."""
        
        response = self.llm_provider.generate(prompt, system_prompt, temperature=0.1)
        
        # Parse the response to get the framework name
        response = response.strip().lower()
        for framework in self.FRAMEWORKS:
            if framework in response:
                return framework
        
        # Default to langchain if the response doesn't match any framework
        return "langchain"
    
    def _rule_based_selection(self, specifications: Dict[str, Any]) -> str:
        """
        Use rule-based selection to determine the most appropriate framework
        
        Args:
            specifications: Dictionary containing user specifications for the agent
            
        Returns:
            Name of the selected framework
        """
        scores = {framework: 0.0 for framework in self.FRAMEWORKS}
        
        # Extract relevant information from specifications
        capabilities = specifications.get("capabilities", [])
        use_case = specifications.get("use_case", "")
        
        # Score each framework based on capabilities
        for capability in capabilities:
            capability = capability.lower()
            for framework, framework_caps in self.framework_capabilities.items():
                for cap_name, cap_score in framework_caps.items():
                    if cap_name in capability:
                        scores[framework] += cap_score
        
        # Score based on use case
        use_case = use_case.lower()
        for framework, framework_caps in self.framework_capabilities.items():
            for cap_name, cap_score in framework_caps.items():
                if cap_name in use_case:
                    scores[framework] += cap_score * 0.5  # Lower weight for use case
        
        # Check for specific requirements
        if "document" in use_case or "retrieval" in use_case or "rag" in use_case:
            scores["llamaindex"] += 2.0
        
        if "workflow" in use_case or "chain" in use_case or "orchestration" in use_case:
            scores["langchain"] += 2.0
        
        if "lightweight" in use_case or "simple" in use_case or "specific" in use_case:
            scores["smallagents"] += 2.0
        
        if "openai" in use_case or "function_calling" in use_case or "vision" in use_case:
            scores["openai_assistants"] += 2.0
        
        # Return the framework with the highest score
        return max(scores.items(), key=lambda x: x[1])[0]
