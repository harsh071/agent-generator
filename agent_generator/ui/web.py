"""
Web interface for the agent generation engine using Streamlit
"""

import os
import json
import tempfile
import streamlit as st
from typing import Dict, Any, List, Optional

from agent_generator.core.engine import AgentGenerationEngine


class WebUI:
    """
    Web interface for the agent generation engine using Streamlit
    """
    
    def __init__(self, engine: AgentGenerationEngine):
        """
        Initialize the web UI
        
        Args:
            engine: Agent generation engine
        """
        self.engine = engine
    
    def run(self):
        """
        Run the web UI using Streamlit
        """
        # Create a temporary file for the Streamlit app
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            f.write(self._get_streamlit_code().encode())
            app_path = f.name
        
        # Run the Streamlit app
        os.system(f"streamlit run {app_path}")
    
    def _get_streamlit_code(self) -> str:
        """
        Get the Streamlit app code
        
        Returns:
            Streamlit app code as a string
        """
        return """
import os
import sys
import json
import streamlit as st
from typing import Dict, Any, List, Optional

# Add the parent directory to sys.path to import the agent_generator package
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agent_generator.core.engine import AgentGenerationEngine

# Set page configuration
st.set_page_config(
    page_title="LLM Agent Generation Engine",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize the engine
@st.cache_resource
def get_engine():
    return AgentGenerationEngine(model=st.session_state.get("model", "gpt-4"))

# Initialize session state
if "specifications" not in st.session_state:
    st.session_state.specifications = {
        "name": "",
        "description": "",
        "language": "python",
        "capabilities": [],
        "use_case": "",
        "model": "gpt-4"
    }

if "generated_agent" not in st.session_state:
    st.session_state.generated_agent = None

if "current_step" not in st.session_state:
    st.session_state.current_step = "basic_info"

# Sidebar
with st.sidebar:
    st.title("🤖 Agent Generator")
    st.markdown("---")
    
    # Navigation
    st.subheader("Navigation")
    steps = [
        ("basic_info", "1. Basic Information"),
        ("framework", "2. Framework Selection"),
        ("capabilities", "3. Agent Capabilities"),
        ("use_case", "4. Use Case"),
        ("advanced", "5. Advanced Options"),
        ("generate", "6. Generate Agent")
    ]
    
    for step_id, step_name in steps:
        if st.button(step_name, key=f"nav_{step_id}"):
            st.session_state.current_step = step_id
    
    st.markdown("---")
    
    # About section
    st.subheader("About")
    st.markdown("""
    The LLM Agent Generation Engine creates custom agents using GPT-4 or Claude,
    with adapters for popular frameworks.
    
    **Frameworks:**
    - LlamaIndex
    - LangChain
    - SmallAgents
    - OpenAI Assistants
    """)

# Main content
st.title("LLM Agent Generation Engine")

# Basic Information step
if st.session_state.current_step == "basic_info":
    st.header("Basic Information")
    
    st.session_state.specifications["name"] = st.text_input(
        "Agent Name",
        value=st.session_state.specifications.get("name", ""),
        help="A descriptive name for your agent"
    )
    
    st.session_state.specifications["description"] = st.text_area(
        "Agent Description",
        value=st.session_state.specifications.get("description", ""),
        help="A detailed description of what your agent does"
    )
    
    st.session_state.specifications["language"] = st.selectbox(
        "Programming Language",
        options=["python", "javascript"],
        index=0 if st.session_state.specifications.get("language", "python") == "python" else 1,
        help="The programming language for your agent"
    )
    
    if st.button("Next: Framework Selection", key="next_framework"):
        st.session_state.current_step = "framework"

# Framework Selection step
elif st.session_state.current_step == "framework":
    st.header("Framework Selection")
    
    st.markdown("""
    Select the framework that best suits your agent's needs:
    
    - **LlamaIndex**: Best for document retrieval and RAG applications
    - **LangChain**: Best for workflow and chain-of-thought operations
    - **SmallAgents**: Best for lightweight, specific-purpose agents
    - **OpenAI Assistants**: Best for leveraging OpenAI's agent capabilities
    - **Auto-select**: Let the engine choose based on your requirements
    """)
    
    framework_options = [
        "Auto-select",
        "LlamaIndex",
        "LangChain",
        "SmallAgents",
        "OpenAI Assistants"
    ]
    
    framework_map = {
        "LlamaIndex": "llamaindex",
        "LangChain": "langchain",
        "SmallAgents": "smallagents",
        "OpenAI Assistants": "openai_assistants"
    }
    
    selected_framework = st.selectbox(
        "Framework",
        options=framework_options,
        index=0
    )
    
    if selected_framework != "Auto-select":
        st.session_state.specifications["framework"] = framework_map[selected_framework]
    elif "framework" in st.session_state.specifications:
        del st.session_state.specifications["framework"]
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous: Basic Information", key="prev_basic"):
            st.session_state.current_step = "basic_info"
    with col2:
        if st.button("Next: Agent Capabilities", key="next_capabilities"):
            st.session_state.current_step = "capabilities"

# Agent Capabilities step
elif st.session_state.current_step == "capabilities":
    st.header("Agent Capabilities")
    
    st.markdown("Select the capabilities your agent should have:")
    
    capability_options = {
        "document_retrieval": "Document Retrieval",
        "question_answering": "Question Answering",
        "web_browsing": "Web Browsing",
        "tool_usage": "Tool Usage",
        "memory_retention": "Memory/Context Retention",
        "chain_of_thought": "Chain-of-Thought Reasoning"
    }
    
    selected_capabilities = []
    for cap_id, cap_name in capability_options.items():
        if st.checkbox(cap_name, value=cap_id in st.session_state.specifications.get("capabilities", [])):
            selected_capabilities.append(cap_id)
    
    custom_capability = st.text_input(
        "Custom Capability (optional)",
        value=""
    )
    
    if custom_capability:
        selected_capabilities.append(custom_capability)
    
    st.session_state.specifications["capabilities"] = selected_capabilities
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous: Framework Selection", key="prev_framework"):
            st.session_state.current_step = "framework"
    with col2:
        if st.button("Next: Use Case", key="next_use_case"):
            st.session_state.current_step = "use_case"

# Use Case step
elif st.session_state.current_step == "use_case":
    st.header("Use Case")
    
    st.markdown("Describe the specific use case for your agent:")
    
    st.session_state.specifications["use_case"] = st.text_area(
        "Use Case Description",
        value=st.session_state.specifications.get("use_case", ""),
        help="A detailed description of how your agent will be used"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous: Agent Capabilities", key="prev_capabilities"):
            st.session_state.current_step = "capabilities"
    with col2:
        if st.button("Next: Advanced Options", key="next_advanced"):
            st.session_state.current_step = "advanced"

# Advanced Options step
elif st.session_state.current_step == "advanced":
    st.header("Advanced Options")
    
    st.subheader("Model Selection")
    st.session_state.specifications["model"] = st.selectbox(
        "LLM Model",
        options=["gpt-4", "gpt-3.5-turbo", "claude-2", "claude-instant"],
        index=0 if st.session_state.specifications.get("model", "gpt-4") == "gpt-4" else 
              1 if st.session_state.specifications.get("model") == "gpt-3.5-turbo" else
              2 if st.session_state.specifications.get("model") == "claude-2" else 3,
        help="The LLM model to use for your agent"
    )
    
    st.subheader("Custom Requirements")
    st.session_state.specifications["custom_requirements"] = st.text_area(
        "Custom Requirements (optional)",
        value=st.session_state.specifications.get("custom_requirements", ""),
        help="Any additional requirements for your agent"
    )
    
    st.subheader("API Keys")
    api_keys = st.session_state.specifications.get("api_keys", {})
    
    api_keys["openai"] = st.text_input(
        "OpenAI API Key (optional)",
        value=api_keys.get("openai", ""),
        type="password",
        help="Your OpenAI API key"
    )
    
    api_keys["anthropic"] = st.text_input(
        "Anthropic API Key (optional)",
        value=api_keys.get("anthropic", ""),
        type="password",
        help="Your Anthropic API key"
    )
    
    # Only add non-empty keys
    st.session_state.specifications["api_keys"] = {k: v for k, v in api_keys.items() if v}
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous: Use Case", key="prev_use_case"):
            st.session_state.current_step = "use_case"
    with col2:
        if st.button("Next: Generate Agent", key="next_generate"):
            st.session_state.current_step = "generate"

# Generate Agent step
elif st.session_state.current_step == "generate":
    st.header("Generate Agent")
    
    # Display specifications
    st.subheader("Agent Specifications")
    st.json(st.session_state.specifications)
    
    # Generate button
    if st.button("Generate Agent", key="btn_generate"):
        with st.spinner("Generating agent code..."):
            engine = get_engine()
            try:
                # Update the engine model if needed
                engine.llm_provider.model = st.session_state.specifications.get("model", "gpt-4")
                
                # Generate the agent
                agent_data = engine.generate_agent(st.session_state.specifications)
                st.session_state.generated_agent = agent_data
                
                st.success("Agent generated successfully!")
            except Exception as e:
                st.error(f"Error generating agent: {str(e)}")
    
    # Display generated agent
    if st.session_state.generated_agent:
        st.subheader("Generated Agent")
        
        # Display framework
        st.markdown(f"**Framework:** {st.session_state.generated_agent['framework']}")
        
        # Display code
        st.code(st.session_state.generated_agent["code"], language=st.session_state.specifications.get("language", "python"))
        
        # Save button
        if st.button("Save Agent", key="btn_save"):
            # Create a temporary directory
            output_dir = tempfile.mkdtemp(prefix="agent_")
            
            # Save the agent
            engine = get_engine()
            saved_path = engine.save_agent(st.session_state.generated_agent, output_dir)
            
            # Create a zip file
            import shutil
            zip_path = f"{output_dir}.zip"
            shutil.make_archive(output_dir, 'zip', output_dir)
            
            # Provide download link
            with open(zip_path, "rb") as f:
                st.download_button(
                    label="Download Agent",
                    data=f,
                    file_name=f"{st.session_state.specifications['name']}.zip",
                    mime="application/zip"
                )
    
    if st.button("Previous: Advanced Options", key="prev_advanced"):
        st.session_state.current_step = "advanced"

# Footer
st.markdown("---")
st.markdown("© 2025 LLM Agent Generation Engine")
"""
        return code
