# LLM Agent Generation Engine

A powerful tool that generates custom LLM agents using GPT-4 or Claude, with adapters for popular frameworks.

## Features

- **Code Generation**: Generates Python/Javascript code with appropriate imports, classes, and methods
- **Framework Adapters**: Standardized interface between generated agents and underlying frameworks
  - LlamaIndex Adapter: For document retrieval and RAG applications
  - LangChain Adapter: For workflow and chain-of-thought operations
  - SmalAgents Adapter: For lightweight, specific-purpose agents
  - OpenAI Assistants Adapter: For leveraging OpenAI's agent capabilities
- **User-friendly Interface**: Collect specifications through UI/CLI
- **Framework Selection**: Automatically determine appropriate framework based on requirements

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/agent-generator.git
cd agent-generator

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (optional)
# Create a .env file with your API keys:
# OPENAI_API_KEY=your_openai_key
# ANTHROPIC_API_KEY=your_anthropic_key
```

## Running the Application

### Command Line Interface (CLI)

```bash
# Run with CLI (default)
python main.py

# Explicitly specify CLI and model
python main.py --ui cli --model gpt-4
```

### Web Interface (Streamlit)

```bash
# Run with web UI
python main.py --ui web

# Specify a different model
python main.py --ui web --model claude
```

## Command Line Arguments

- `--ui`: User interface type (`cli` or `web`, default: `cli`)
- `--model`: LLM model to use for generation (`gpt-4` or `claude`, default: `gpt-4`)

## Using the Generated Agent

After generating an agent:

1. Navigate to the output directory (default: `./generated_agent`)
2. Follow the instructions in the generated README.md file
3. Install any additional dependencies required by the generated agent
4. Run the agent using the provided entry point

## Requirements

- Python 3.8+
- Required packages listed in requirements.txt:
  - openai
  - anthropic
  - langchain
  - llama-index
  - streamlit
  - pydantic
  - python-dotenv
  - requests
  - jinja2
