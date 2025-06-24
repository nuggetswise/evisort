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

def get_workday_job_posting() -> str:
    """
    Return the Workday job posting text for analysis.
    """
    return """
    Product Manager - Contract Intelligence (Evisort)
    
    About the Role:
    We are seeking a Product Manager to join our Contract Intelligence team at Evisort, a Workday company. 
    You will be responsible for driving the development of AI-powered contract analysis and intelligence features 
    that help legal teams extract insights from complex legal documents.
    
    Key Responsibilities:
    • Lead product strategy and roadmap for contract intelligence features
    • Collaborate with engineering teams to develop AI/ML-powered contract parsing capabilities
    • Define and track key metrics for contract analysis accuracy and user adoption
    • Work with legal and compliance teams to ensure product meets regulatory requirements
    • Conduct user research to understand pain points in contract review workflows
    • Prioritize features based on business impact and technical feasibility
    
    Required Skills:
    • 5+ years of product management experience, preferably in AI/ML products
    • Experience with large language models (LLMs) and natural language processing
    • Understanding of enterprise software workflows and compliance requirements
    • Strong analytical skills and experience with product metrics
    • Excellent communication and stakeholder management skills
    • Background in legal tech or contract management is a plus
    
    Preferred Qualifications:
    • Experience with contract analysis or legal document processing
    • Knowledge of machine learning model development and deployment
    • Familiarity with enterprise SaaS product development
    • Experience working with legal teams or in regulated industries
    
    Location: Vancouver, BC, Canada
    """ 