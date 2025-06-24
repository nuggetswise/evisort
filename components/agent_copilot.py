import streamlit as st
import pandas as pd
from typing import List, Dict, Any
from utils.llm_client import LLMClient

class AgentCopilot:
    def __init__(self):
        self.llm_client = st.session_state.get('llm_client', LLMClient())
        self.conversation_history = []
    
    def render(self):
        """Render the Agent Copilot section."""
        st.markdown('<h2 class="section-header">🧠 Agent Copilot</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        **Your AI-powered Product Manager assistant.** Ask strategic questions about contract intelligence product development, 
        roadmap planning, feature prioritization, and more. This simulates how an AI copilot would help a PM make data-driven decisions.
        """)
        
        # Initialize session state for conversation
        if 'copilot_conversation' not in st.session_state:
            st.session_state.copilot_conversation = []
        
        # Quick question buttons
        self._render_quick_questions()
        
        # Custom question input
        self._render_custom_question()
        
        # Conversation history
        self._render_conversation_history()
        
        # Strategic insights panel
        self._render_strategic_insights()
    
    def _render_quick_questions(self):
        """Render quick question buttons."""
        st.markdown("### 🚀 Quick Questions")
        
        quick_questions = [
            "What roadmap features would make contract analysis faster for legal teams?",
            "How would you prioritize clause extraction vs summarization?",
            "What metrics should we track for contract intelligence success?",
            "How can we improve AI accuracy while maintaining speed?",
            "What are the biggest challenges in enterprise contract management?",
            "How should we approach compliance requirements in different jurisdictions?"
        ]
        
        # Create columns for buttons
        cols = st.columns(2)
        for i, question in enumerate(quick_questions):
            col_idx = i % 2
            with cols[col_idx]:
                if st.button(f"❓ {question[:50]}...", key=f"quick_q_{i}"):
                    self._process_question(question)
    
    def _render_custom_question(self):
        """Render custom question input."""
        st.markdown("### 💭 Ask Your Own Question")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            user_question = st.text_area(
                "Ask a strategic question about contract intelligence product development:",
                placeholder="e.g., How should we approach international contract compliance?",
                height=100
            )
        
        with col2:
            st.markdown("")
            st.markdown("")
            if st.button("🤖 Ask AI Copilot", type="primary"):
                if user_question.strip():
                    self._process_question(user_question)
                else:
                    st.warning("Please enter a question.")
    
    def _process_question(self, question: str):
        """Process a user question and generate response."""
        with st.spinner("AI Copilot is thinking..."):
            # Generate response using LLM
            response = self._generate_copilot_response(question)
            
            # Add to conversation history
            conversation_entry = {
                'question': question,
                'response': response,
                'timestamp': pd.Timestamp.now()
            }
            
            st.session_state.copilot_conversation.append(conversation_entry)
            
            # Rerun to show the new response
            st.rerun()
    
    def _generate_copilot_response(self, question: str) -> str:
        """Generate a response using the LLM client."""
        system_prompt = """
        You are an expert Product Manager specializing in AI-powered contract intelligence products. 
        You have deep experience with:
        - Large language models and NLP
        - Enterprise software product development
        - Legal tech and compliance requirements
        - Data-driven product strategy
        - User research and stakeholder management
        
        Provide strategic, actionable advice that demonstrates deep understanding of the contract intelligence domain.
        Focus on practical insights that a PM could implement immediately.
        """
        
        return self.llm_client.generate_response(question, system_prompt)
    
    def _render_conversation_history(self):
        """Render the conversation history."""
        if not st.session_state.copilot_conversation:
            return
        
        st.markdown("### 💬 Conversation History")
        
        # Show recent conversations
        for i, entry in enumerate(reversed(st.session_state.copilot_conversation[-5:])):  # Show last 5
            with st.expander(f"Q: {entry['question'][:100]}...", expanded=False):
                st.markdown("**Question:**")
                st.markdown(entry['question'])
                
                st.markdown("**AI Copilot Response:**")
                st.markdown(entry['response'])
                
                st.caption(f"Asked at {entry['timestamp'].strftime('%H:%M:%S')}")
        
        # Clear conversation button
        if st.button("🗑️ Clear Conversation"):
            st.session_state.copilot_conversation = []
            st.rerun()
    
    def _render_strategic_insights(self):
        """Render strategic insights panel."""
        st.markdown("---")
        st.markdown("### 🎯 Strategic Insights Dashboard")
        
        # Key insights cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>🎯 Product Strategy</h4>
                <p>Focus on accuracy and speed as primary differentiators. Legal teams prioritize reliability over advanced features.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>📊 Success Metrics</h4>
                <p>Track contract processing time, accuracy rates, user adoption, and customer satisfaction as key KPIs.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h4>🚀 Growth Opportunities</h4>
                <p>Expand into compliance automation, risk assessment, and predictive analytics for contract outcomes.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Market analysis
        st.markdown("#### 📈 Market Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            **Contract Intelligence Market Trends:**
            
            • **Growing Demand**: Legal teams are increasingly adopting AI tools to handle contract volume
            • **Accuracy Focus**: 95%+ accuracy is table stakes for enterprise adoption
            • **Integration Needs**: Must work seamlessly with existing legal workflows
            • **Compliance Complexity**: Different jurisdictions require specialized handling
            • **ROI Pressure**: Clear efficiency gains needed to justify investment
            """)
        
        with col2:
            # Mock market data
            market_data = {
                'Segment': ['Enterprise', 'Mid-Market', 'SMB'],
                'Market Size': [45, 30, 25],
                'Growth Rate': [25, 35, 40]
            }
            
            df = pd.DataFrame(market_data)
            st.dataframe(df, use_container_width=True)
        
        # Competitive analysis
        st.markdown("#### 🏆 Competitive Landscape")
        
        competitors = [
            {
                'name': 'Evisort',
                'strengths': ['Strong AI accuracy', 'Enterprise focus', 'Workday integration'],
                'weaknesses': ['Limited international support', 'High cost']
            },
            {
                'name': 'ContractPodAi',
                'strengths': ['Comprehensive platform', 'Good compliance features'],
                'weaknesses': ['Complex UI', 'Long implementation time']
            },
            {
                'name': 'Icertis',
                'strengths': ['Enterprise scale', 'Strong compliance'],
                'weaknesses': ['Expensive', 'Complex setup']
            }
        ]
        
        for competitor in competitors:
            with st.expander(f"🏢 {competitor['name']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Strengths:**")
                    for strength in competitor['strengths']:
                        st.markdown(f"✅ {strength}")
                
                with col2:
                    st.markdown("**Weaknesses:**")
                    for weakness in competitor['weaknesses']:
                        st.markdown(f"❌ {weakness}")
        
        # Product recommendations
        st.markdown("#### 💡 Product Recommendations")
        
        recommendations = [
            {
                'area': 'Core Features',
                'recommendations': [
                    'Focus on 99%+ clause extraction accuracy',
                    'Implement real-time processing under 30 seconds',
                    'Build comprehensive metadata extraction'
                ]
            },
            {
                'area': 'User Experience',
                'recommendations': [
                    'Design intuitive interface for non-technical users',
                    'Provide clear confidence scores for all extractions',
                    'Enable easy export to legal workflow tools'
                ]
            },
            {
                'area': 'Enterprise Features',
                'recommendations': [
                    'Build robust API for system integration',
                    'Implement role-based access controls',
                    'Provide detailed audit trails and compliance reporting'
                ]
            }
        ]
        
        for rec in recommendations:
            with st.expander(f"📋 {rec['area']}", expanded=False):
                for recommendation in rec['recommendations']:
                    st.markdown(f"• {recommendation}") 