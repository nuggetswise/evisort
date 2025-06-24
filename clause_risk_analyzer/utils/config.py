import streamlit as st
import os
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """
    Load configuration from Streamlit secrets or environment variables.
    Falls back to mock data for demo purposes.
    """
    config = {
        'openai_api_key': None,
        'cohere_api_key': None,
        'groq_api_key': None,
        'gemini_api_key': None,
        'demo_mode': True
    }
    
    # Try to load from Streamlit secrets
    try:
        if hasattr(st, 'secrets'):
            config['openai_api_key'] = st.secrets.get('openai_api_key')
            config['cohere_api_key'] = st.secrets.get('cohere_api_key')
            config['groq_api_key'] = st.secrets.get('groq_api_key')
            config['gemini_api_key'] = st.secrets.get('gemini_api_key')
    except Exception:
        pass
    
    # Fallback to environment variables
    if not config['openai_api_key']:
        config['openai_api_key'] = os.getenv('OPENAI_API_KEY')
    if not config['cohere_api_key']:
        config['cohere_api_key'] = os.getenv('COHERE_API_KEY')
    if not config['groq_api_key']:
        config['groq_api_key'] = os.getenv('GROQ_API_KEY')
    if not config['gemini_api_key']:
        config['gemini_api_key'] = os.getenv('GEMINI_API_KEY')
    
    # Check if we have any API keys
    has_api_keys = any([
        config['openai_api_key'],
        config['cohere_api_key'],
        config['groq_api_key'],
        config['gemini_api_key']
    ])
    
    config['demo_mode'] = not has_api_keys
    
    return config 