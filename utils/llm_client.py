import streamlit as st
import json
import time
from typing import Dict, Any, List, Optional
import google.generativeai as genai
import openai
import cohere

class LLMClient:
    def __init__(self):
        self.config = st.session_state.get('config', {})
        self.setup_clients()
    
    def setup_clients(self):
        """Initialize LLM clients based on available API keys."""
        self.clients = {}
        
        # Setup Groq (Priority 1)
        if self.config.get('groq_api_key'):
            try:
                import groq
                self.clients['groq'] = groq.Groq(api_key=self.config['groq_api_key'])
            except ImportError:
                pass
            except Exception:
                pass
        
        # Setup Gemini (Priority 2)
        if self.config.get('gemini_api_key'):
            try:
                genai.configure(api_key=self.config['gemini_api_key'])
                self.clients['gemini'] = genai
            except Exception:
                pass
        
        # Setup OpenAI (Priority 3)
        if self.config.get('openai_api_key'):
            try:
                from openai import OpenAI
                test_client = OpenAI(api_key=self.config['openai_api_key'])
                self.clients['openai'] = test_client
            except Exception:
                pass
        
        # Setup Cohere (Priority 4)
        if self.config.get('cohere_api_key'):
            try:
                self.clients['cohere'] = cohere.Client(self.config['cohere_api_key'])
            except Exception:
                pass
    
    def generate_response(self, prompt: str, system_prompt: str = "", model: str = "auto") -> str:
        """
        Generate response using available LLM clients in priority order:
        1. Groq (fastest)
        2. Gemini
        3. OpenAI
        4. Cohere
        Falls back to mock responses if no API keys are available.
        """
        if self.config.get('demo_mode', True) or not self.clients:
            return self._generate_mock_response(prompt, system_prompt)
        
        # Try clients in priority order
        client_order = ['groq', 'gemini', 'openai', 'cohere']
        
        for client_name in client_order:
            if client_name in self.clients:
                try:
                    if client_name == 'groq':
                        return self._call_groq(prompt, system_prompt)
                    elif client_name == 'gemini':
                        return self._call_gemini(prompt, system_prompt)
                    elif client_name == 'openai':
                        return self._call_openai(prompt, system_prompt, model)
                    elif client_name == 'cohere':
                        return self._call_cohere(prompt, system_prompt)
                except Exception:
                    continue
        
        # Fallback to mock response
        return self._generate_mock_response(prompt, system_prompt)
    
    def _call_groq(self, prompt: str, system_prompt: str) -> str:
        """Call Groq API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.clients['groq'].chat.completions.create(
            model="llama3-8b-8192",  # Fast and reliable model
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    
    def _call_gemini(self, prompt: str, system_prompt: str) -> str:
        """Call Gemini API."""
        model = genai.GenerativeModel('gemini-pro')
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = model.generate_content(full_prompt)
        return response.text
    
    def _call_openai(self, prompt: str, system_prompt: str, model: str) -> str:
        """Call OpenAI API using the new 1.0.0+ format."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # Use the stored OpenAI client
        client = self.clients['openai']
        
        response = client.chat.completions.create(
            model=model if model != "auto" else "gpt-4",
            messages=messages,
            max_tokens=1000,
            temperature=0.3  # Lower temperature for more consistent legal analysis
        )
        return response.choices[0].message.content
    
    def _call_cohere(self, prompt: str, system_prompt: str) -> str:
        """Call Cohere API."""
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = self.clients['cohere'].generate(
            prompt=full_prompt,
            max_tokens=1000,
            temperature=0.7
        )
        return response.generations[0].text
    
    def _generate_mock_response(self, prompt: str, system_prompt: str) -> str:
        """Generate mock responses for demo purposes."""
        prompt_lower = prompt.lower()
        
        # Role decoder responses
        if "responsibilities" in prompt_lower or "core" in prompt_lower:
            return """
            **Core Responsibilities:**
            • Lead AI-powered contract intelligence product strategy
            • Drive development of LLM-based contract parsing capabilities
            • Define and track contract analysis accuracy metrics
            • Collaborate with legal teams on compliance requirements
            • Prioritize features based on business impact and technical feasibility
            
            **AI/ML Focus:**
            • Large language model integration for contract understanding
            • Natural language processing for clause extraction
            • Machine learning for risk assessment and compliance checking
            • Enterprise workflow automation for legal teams
            """
        
        elif "skills" in prompt_lower or "requirements" in prompt_lower:
            return """
            **Required Skills:**
            • 5+ years PM experience in AI/ML products
            • Expertise with LLMs and NLP technologies
            • Enterprise software workflow understanding
            • Strong analytical and metrics-driven approach
            • Legal tech or compliance background preferred
            
            **Key Competencies:**
            • Product strategy and roadmap development
            • Cross-functional team collaboration
            • User research and stakeholder management
            • Technical understanding of AI/ML systems
            """
        
        elif "metrics" in prompt_lower or "kpis" in prompt_lower:
            return """
            **Key Metrics & KPIs:**
            • Contract analysis accuracy rate (>95% target)
            • Processing time reduction (50% improvement goal)
            • User adoption rate (legal team usage)
            • Feature utilization and engagement
            • Customer satisfaction scores
            • Revenue impact from efficiency gains
            """
        
        # Contract simulator responses
        elif "contract" in prompt_lower and ("extract" in prompt_lower or "analyze" in prompt_lower):
            return """
            **Contract Analysis Results:**
            
            **Extracted Clauses:**
            • Termination Clause: 30-day notice required
            • Payment Terms: Net 30 days
            • Liability Limits: $500,000 cap
            • Confidentiality: 5-year term
            
            **Key Metadata:**
            • Contract Type: Service Agreement
            • Effective Date: January 15, 2024
            • Expiration Date: January 15, 2025
            • Renewal Terms: Auto-renewal with 30-day notice
            
            **Risk Assessment:**
            • Medium Risk: Payment terms may impact cash flow
            • Low Risk: Standard confidentiality terms
            • High Risk: Liability cap may be insufficient for large projects
            """
        
        # Agent copilot responses
        elif "roadmap" in prompt_lower or "features" in prompt_lower:
            return """
            **Strategic Roadmap Recommendations:**
            
            **Phase 1 (Q1-Q2):**
            • Enhanced clause extraction with 99% accuracy
            • Real-time contract risk scoring
            • Integration with legal workflow tools
            
            **Phase 2 (Q3-Q4):**
            • Multi-language contract support
            • Advanced compliance checking
            • Predictive analytics for contract outcomes
            
            **Priority Rationale:**
            Focus on accuracy and speed first, then expand to advanced features.
            Legal teams need reliable, fast analysis before advanced capabilities.
            """
        
        elif "prioritize" in prompt_lower:
            return """
            **Feature Prioritization Strategy:**
            
            **High Priority:**
            • Clause extraction accuracy (core value prop)
            • Processing speed (user experience)
            • Integration capabilities (adoption)
            
            **Medium Priority:**
            • Risk assessment algorithms
            • Compliance checking
            • Advanced analytics
            
            **Low Priority:**
            • Nice-to-have features
            • Experimental AI capabilities
            
            **Decision Framework:**
            Impact on user workflow × Technical feasibility × Business value
            """
        
        # Default response
        return """
        **AI Analysis Complete**
        
        Based on the provided information, here are the key insights:
        
        • The role requires strong AI/ML product management experience
        • Focus on contract intelligence and legal tech workflows
        • Emphasis on metrics-driven product development
        • Need for technical understanding of LLMs and NLP
        
        This demonstrates the intersection of product management, AI technology, and legal domain expertise.
        """
    
    def analyze_document(self, content: str, analysis_type: str = "contract") -> Dict[str, Any]:
        """Analyze document content and return structured results."""
        if self.config.get('demo_mode', True):
            return self._generate_mock_analysis(content, analysis_type)
        
        # Real analysis would go here
        return self._generate_mock_analysis(content, analysis_type)
    
    def _generate_mock_analysis(self, content: str, analysis_type: str) -> Dict[str, Any]:
        """Generate mock document analysis results."""
        if analysis_type == "contract":
            return {
                "clauses": [
                    {"type": "Termination", "content": "Either party may terminate with 30 days written notice", "confidence": 0.95},
                    {"type": "Payment", "content": "Payment due within 30 days of invoice", "confidence": 0.92},
                    {"type": "Liability", "content": "Liability limited to amount paid under this agreement", "confidence": 0.88}
                ],
                "metadata": {
                    "contract_type": "Service Agreement",
                    "parties": ["Company A", "Company B"],
                    "effective_date": "2024-01-15",
                    "expiration_date": "2025-01-15",
                    "value": "$500,000"
                },
                "risks": [
                    {"level": "Medium", "description": "Payment terms may impact cash flow", "mitigation": "Consider shorter payment terms"},
                    {"level": "Low", "description": "Standard confidentiality terms", "mitigation": "No action required"}
                ],
                "summary": "Standard service agreement with typical terms. No major red flags identified."
            }
        else:
            return {
                "summary": "Document analysis complete",
                "key_points": ["Point 1", "Point 2", "Point 3"],
                "confidence": 0.85
            } 