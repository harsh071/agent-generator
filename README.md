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
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Requirements

- Python 3.8+
- Required packages listed in requirements.txt
