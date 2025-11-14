"""
AgentBeats Integration Package for PersonaGym-R

This package contains all necessary components to deploy PersonaGym-R
as a green agent on the AgentBeats platform.

Components:
-----------
- green_agent.py: A2A-compliant green agent web service
- controller.py: State management and reset handling
- config.yaml: Configuration and metadata
- requirements.txt: Additional dependencies for A2A protocol

Usage:
------
Run the green agent:
    python -m agentbeats.green_agent

Or import components:
    from agentbeats.green_agent import PersonaGymGreenAgent
    from agentbeats.controller import GreenAgentController
"""

__version__ = "1.0.0"
__author__ = "PersonaGym Team"

from pathlib import Path

# Package directory
PACKAGE_DIR = Path(__file__).parent

# Configuration file
CONFIG_FILE = PACKAGE_DIR / "config.yaml"

# Requirements file
REQUIREMENTS_FILE = PACKAGE_DIR / "requirements.txt"

__all__ = [
    "__version__",
    "PACKAGE_DIR",
    "CONFIG_FILE",
    "REQUIREMENTS_FILE",
]
