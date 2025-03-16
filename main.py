#!/usr/bin/env python3
"""
LLM Agent Generation Engine
Main application entry point
"""

import os
import argparse
from dotenv import load_dotenv

from agent_generator.core.engine import AgentGenerationEngine
from agent_generator.ui.cli import CLI

# Load environment variables from .env file
load_dotenv()

def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(description="LLM Agent Generation Engine")
    parser.add_argument("--ui", choices=["cli", "web"], default="cli",
                        help="User interface type (cli or web)")
    parser.add_argument("--model", choices=["gpt-4", "claude"], default="gpt-4",
                        help="LLM model to use for generation")
    args = parser.parse_args()
    
    # Initialize the agent generation engine
    engine = AgentGenerationEngine(model=args.model)
    
    # Launch the appropriate UI
    if args.ui == "cli":
        ui = CLI(engine)
        ui.run()
    else:
        ui = WebUI(engine)
        ui.run()

if __name__ == "__main__":
    main()
