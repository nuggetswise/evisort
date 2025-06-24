import streamlit as st
import os
from components.role_decoder import RoleDecoder
from components.contract_simulator import ContractSimulator
from components.agent_copilot import AgentCopilot
from components.fit_analyzer import FitAnalyzer
from utils.config import load_config
from utils.llm_client import LLMClient

# Page configuration
st.set_page_config(
    page_title="Workday PM Role Demo - Contract Intelligence",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'llm_client' not in st.session_state:
        st.session_state.llm_client = LLMClient()
    
    if 'config' not in st.session_state:
        st.session_state.config = load_config()
    
    # Header
    st.markdown('<h1 class="main-header">🧭 Workday PM Role Demo</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Contract Intelligence Product Manager Simulation</p>', unsafe_allow_html=True)
    
    # Sidebar for navigation
    with st.sidebar:
        st.markdown("## 📋 Navigation")
        st.markdown("---")
        
        # Role information
        st.markdown("### 🎯 Target Role")
        st.markdown("**Product Manager - Contract Intelligence**")
        st.markdown("*Workday/Evisort - Vancouver, BC*")
        
        st.markdown("---")
        
        # App sections
        st.markdown("### 📖 App Sections")
        
        # Navigation tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🧭 Role Decoder", 
            "📄 Contract AI Simulator", 
            "🧠 Agent Copilot", 
            "💼 My Fit"
        ])
    
    # Main content area
    with tab1:
        RoleDecoder().render()
    
    with tab2:
        ContractSimulator().render()
    
    with tab3:
        AgentCopilot().render()
    
    with tab4:
        FitAnalyzer().render()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; font-size: 0.9rem;">
            <p>🔬 This is a demonstration app simulating contract intelligence capabilities.</p>
            <p>All AI-generated content is for illustrative purposes only.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 