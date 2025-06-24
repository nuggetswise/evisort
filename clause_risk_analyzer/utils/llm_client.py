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
        
        # Setup OpenAI (Priority 1)
        if self.config.get('openai_api_key'):
            try:
                openai.api_key = self.config['openai_api_key']
                self.clients['openai'] = openai
                st.success("✅ OpenAI client configured")
            except Exception as e:
                st.warning(f"OpenAI client setup failed: {e}")
        
        # Setup Cohere (Priority 2)
        if self.config.get('cohere_api_key'):
            try:
                self.clients['cohere'] = cohere.Client(self.config['cohere_api_key'])
                st.success("✅ Cohere client configured")
            except Exception as e:
                st.warning(f"Cohere client setup failed: {e}")
        
        # Setup Groq (Priority 3)
        if self.config.get('groq_api_key'):
            try:
                import groq
                self.clients['groq'] = groq.Groq(api_key=self.config['groq_api_key'])
                st.success("✅ Groq client configured")
            except ImportError:
                st.warning("Groq package not installed. Install with: pip install groq")
            except Exception as e:
                st.warning(f"Groq client setup failed: {e}")
        
        # Setup Gemini (Priority 4)
        if self.config.get('gemini_api_key'):
            try:
                genai.configure(api_key=self.config['gemini_api_key'])
                self.clients['gemini'] = genai
                st.success("✅ Gemini client configured")
            except Exception as e:
                st.warning(f"Gemini client setup failed: {e}")
        
        # Log available clients
        if self.clients:
            st.info(f"🤖 Available AI providers: {', '.join(self.clients.keys())}")
        else:
            st.info("🤖 Running in demo mode (no API keys configured)")
    
    def analyze_clause_risk(self, clause_text: str) -> Dict[str, Any]:
        """
        Analyze clause risk using LLM with structured output.
        """
        system_prompt = """
        You are an expert legal analyst specializing in contract risk assessment. 
        Analyze the provided contract clause and return a JSON response with the following structure:
        
        {
            "risk_level": "high|medium|low",
            "confidence": 85,
            "explanation": "Detailed explanation of why this clause is risky...",
            "key_risks": ["risk1", "risk2", "risk3"],
            "recommendations": ["rec1", "rec2", "rec3"],
            "clause_type": "indemnification|termination|confidentiality|payment|liability|general"
        }
        
        Risk levels:
        - HIGH: Contains unlimited liability, broad indemnification, severe penalties
        - MEDIUM: Contains termination clauses, payment terms, standard legal provisions
        - LOW: Contains standard confidentiality, governing law, or general terms
        
        Be specific about why the clause is risky and provide actionable recommendations.
        """
        
        user_prompt = f"""
        Analyze this contract clause for risk level:
        
        "{clause_text}"
        
        Return only valid JSON with the specified structure.
        """
        
        response = self.generate_response(user_prompt, system_prompt)
        
        # Try to parse JSON response
        try:
            # Extract JSON from response (in case there's extra text)
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                result = json.loads(json_str)
                return result
        except json.JSONDecodeError:
            pass
        
        # Fallback to mock response if JSON parsing fails
        return self._generate_mock_risk_analysis(clause_text)
    
    def extract_metadata(self, clause_text: str) -> Dict[str, Any]:
        """
        Extract metadata from clause using LLM.
        """
        system_prompt = """
        You are an expert contract analyst. Extract key metadata from the contract clause and return a JSON response:
        
        {
            "effective_date": "January 15, 2024" or null,
            "termination_notice": "30 days" or null,
            "contract_value": "$500,000" or null,
            "liability_cap": "$100,000" or null,
            "payment_terms": "Net 30" or null,
            "clause_type": "indemnification|termination|confidentiality|payment|liability|general",
            "parties_mentioned": ["Client", "Provider"],
            "jurisdiction": "California" or "Not specified"
        }
        
        Only extract information that is explicitly stated in the clause. Return null for missing information.
        """
        
        user_prompt = f"""
        Extract metadata from this contract clause:
        
        "{clause_text}"
        
        Return only valid JSON with the specified structure.
        """
        
        response = self.generate_response(user_prompt, system_prompt)
        
        # Try to parse JSON response
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                result = json.loads(json_str)
                return result
        except json.JSONDecodeError:
            pass
        
        # Fallback to mock response if JSON parsing fails
        return self._generate_mock_metadata(clause_text)
    
    def analyze_compliance(self, clause_text: str, frameworks: Dict[str, str]) -> Dict[str, Any]:
        """
        Analyze clause compliance against regulatory frameworks using LLM.
        """
        system_prompt = """
        You are an expert compliance analyst specializing in regulatory frameworks. 
        Analyze the provided contract clause against multiple compliance frameworks and return a JSON response:
        
        {
            "overall_score": 85,
            "frameworks": {
                "GDPR": {
                    "compliance_level": "Compliant|Partial|Non-Compliant",
                    "issues": ["issue1", "issue2"],
                    "recommendations": ["rec1", "rec2"]
                },
                "CCPA": {
                    "compliance_level": "Compliant|Partial|Non-Compliant", 
                    "issues": ["issue1", "issue2"],
                    "recommendations": ["rec1", "rec2"]
                }
            }
        }
        
        Compliance levels:
        - Compliant: Meets all requirements
        - Partial: Meets some requirements but has gaps
        - Non-Compliant: Significant compliance issues
        
        Be specific about compliance issues and provide actionable recommendations.
        """
        
        user_prompt = f"""
        Analyze this contract clause for compliance with these frameworks:
        
        Frameworks: {', '.join([f'{k} ({v})' for k, v in frameworks.items()])}
        
        Clause: "{clause_text}"
        
        Return only valid JSON with the specified structure.
        """
        
        response = self.generate_response(user_prompt, system_prompt)
        
        # Try to parse JSON response
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                result = json.loads(json_str)
                return result
        except json.JSONDecodeError:
            pass
        
        # Fallback to mock response if JSON parsing fails
        return self._generate_mock_compliance_analysis(clause_text, frameworks)
    
    def generate_response(self, prompt: str, system_prompt: str = "", model: str = "auto") -> str:
        """
        Generate response using available LLM clients in priority order:
        1. OpenAI
        2. Cohere
        3. Groq
        4. Gemini
        Falls back to mock responses if no API keys are available.
        """
        if self.config.get('demo_mode', True) or not self.clients:
            return self._generate_mock_response(prompt, system_prompt)
        
        # Try clients in priority order
        client_order = ['openai', 'cohere', 'groq', 'gemini']
        
        for client_name in client_order:
            if client_name in self.clients:
                try:
                    if client_name == 'openai':
                        return self._call_openai(prompt, system_prompt, model)
                    elif client_name == 'cohere':
                        return self._call_cohere(prompt, system_prompt)
                    elif client_name == 'groq':
                        return self._call_groq(prompt, system_prompt)
                    elif client_name == 'gemini':
                        return self._call_gemini(prompt, system_prompt)
                except Exception as e:
                    st.warning(f"Error with {client_name}: {e}")
                    continue
        
        # Fallback to mock response
        return self._generate_mock_response(prompt, system_prompt)
    
    def _call_openai(self, prompt: str, system_prompt: str, model: str) -> str:
        """Call OpenAI API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = openai.ChatCompletion.create(
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
            temperature=0.3
        )
        return response.generations[0].text
    
    def _call_groq(self, prompt: str, system_prompt: str) -> str:
        """Call Groq API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.clients['groq'].chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            max_tokens=1000,
            temperature=0.3
        )
        return response.choices[0].message.content
    
    def _call_gemini(self, prompt: str, system_prompt: str) -> str:
        """Call Gemini API."""
        model = genai.GenerativeModel('gemini-pro')
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = model.generate_content(full_prompt)
        return response.text
    
    def _generate_mock_response(self, prompt: str, system_prompt: str) -> str:
        """Generate mock responses for demo purposes."""
        return """
        {
            "risk_level": "medium",
            "confidence": 75,
            "explanation": "This clause contains standard legal provisions that require careful review.",
            "key_risks": ["Standard legal terms", "Requires review"],
            "recommendations": ["Review against company policies", "Ensure compliance"],
            "clause_type": "general"
        }
        """
    
    def _generate_mock_risk_analysis(self, clause_text: str) -> Dict[str, Any]:
        """Generate mock risk analysis for demo purposes."""
        clause_lower = clause_text.lower()
        
        if 'indemnify' in clause_lower or 'unlimited' in clause_lower:
            return {
                "risk_level": "high",
                "confidence": 90,
                "explanation": "This clause contains high-risk indemnification language that could expose your organization to unlimited liability.",
                "key_risks": ["Unlimited liability", "Broad indemnification", "Financial exposure"],
                "recommendations": ["Immediate legal review required", "Negotiate liability caps", "Limit indemnification scope"],
                "clause_type": "indemnification"
            }
        elif 'termination' in clause_lower or 'payment' in clause_lower:
            return {
                "risk_level": "medium",
                "confidence": 80,
                "explanation": "This clause contains standard business terms that require review against company policies.",
                "key_risks": ["Business continuity", "Cash flow impact", "Operational considerations"],
                "recommendations": ["Review against policies", "Ensure alignment with business needs", "Document concerns"],
                "clause_type": "termination" if 'termination' in clause_lower else "payment"
            }
        else:
            return {
                "risk_level": "low",
                "confidence": 70,
                "explanation": "This clause contains standard legal provisions that present minimal risk to your organization.",
                "key_risks": ["Standard terms", "Minimal risk"],
                "recommendations": ["Standard review", "No immediate action required"],
                "clause_type": "general"
            }
    
    def _generate_mock_metadata(self, clause_text: str) -> Dict[str, Any]:
        """Generate mock metadata for demo purposes."""
        return {
            "effective_date": None,
            "termination_notice": None,
            "contract_value": None,
            "liability_cap": None,
            "payment_terms": None,
            "clause_type": "general",
            "parties_mentioned": [],
            "jurisdiction": "Not specified"
        }
    
    def _generate_mock_compliance_analysis(self, clause_text: str, frameworks: Dict[str, str]) -> Dict[str, Any]:
        """Generate mock compliance analysis for demo purposes."""
        clause_lower = clause_text.lower()
        
        # Simple keyword-based compliance checking
        compliance_data = {
            "overall_score": 75,
            "frameworks": {}
        }
        
        for framework, description in frameworks.items():
            if framework == "GDPR":
                if 'personal data' in clause_lower or 'privacy' in clause_lower:
                    compliance_data["frameworks"][framework] = {
                        "compliance_level": "Partial",
                        "issues": ["Data processing terms need review"],
                        "recommendations": ["Add explicit consent mechanisms", "Include data subject rights"]
                    }
                else:
                    compliance_data["frameworks"][framework] = {
                        "compliance_level": "Compliant",
                        "issues": [],
                        "recommendations": ["Standard review recommended"]
                    }
            elif framework == "CCPA":
                if 'california' in clause_lower or 'consumer' in clause_lower:
                    compliance_data["frameworks"][framework] = {
                        "compliance_level": "Partial",
                        "issues": ["California-specific terms identified"],
                        "recommendations": ["Review CCPA compliance requirements"]
                    }
                else:
                    compliance_data["frameworks"][framework] = {
                        "compliance_level": "Compliant",
                        "issues": [],
                        "recommendations": ["Standard review recommended"]
                    }
            else:
                compliance_data["frameworks"][framework] = {
                    "compliance_level": "Partial",
                    "issues": ["Standard compliance review required"],
                    "recommendations": ["Review with legal counsel", "Ensure framework-specific requirements"]
                }
        
        return compliance_data 