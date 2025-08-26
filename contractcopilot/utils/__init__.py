"""
ContractCopilot Utilities

Core utilities for the contract analysis application:
- llm_client: Multi-provider LLM integration
- config: Configuration management
"""

from .llm_client import LLMClient
from .config import load_config

__all__ = [
    "LLMClient",
    "load_config"
] 