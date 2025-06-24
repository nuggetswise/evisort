import streamlit as st
import sys
import os

# Add the current directory to the path to import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.config import load_config
from utils.llm_client import LLMClient
from components.clause_input import clause_input
from components.risk_classifier import risk_classifier
from components.metadata_extractor import metadata_extractor
from components.compliance_checker import compliance_checker

# Page configuration
st.set_page_config(
    page_title="Clause Risk Analyzer",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    .risk-high {
        border-left-color: #ff4b4b !important;
        background: #fff5f5 !important;
    }
    .risk-medium {
        border-left-color: #ffa726 !important;
        background: #fff8e1 !important;
    }
    .risk-low {
        border-left-color: #66bb6a !important;
        background: #f1f8e9 !important;
    }
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        font-weight: bold;
    }
    .sample-button {
        width: 60px !important;
        height: 30px !important;
        font-size: 12px !important;
        padding: 4px 8px !important;
        border-radius: 15px !important;
    }
    .info-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize configuration
    if 'config' not in st.session_state:
        st.session_state.config = load_config()
    
    # Initialize LLM client
    if 'llm_client' not in st.session_state:
        st.session_state.llm_client = LLMClient()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📋 Clause Risk Analyzer</h1>
        <p>AI-Powered Contract Clause Analysis for Legal Professionals</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with information
    with st.sidebar:
        st.markdown("### 🎯 About This Tool")
        st.markdown("""
        This Clause Risk Analyzer uses advanced AI to:
        
        🔍 **Analyze Risk Levels**
        - High, Medium, Low risk classification
        - Confidence scoring
        - Detailed explanations
        
        💡 **Provide Recommendations**
        - Actionable insights
        - Risk mitigation strategies
        - Best practices guidance
        """)
        
        st.markdown("### 🚀 How to Use")
        st.markdown("""
        1. **Enter Clause Text** - Paste your contract clause
        2. **Analyze Risk** - Get AI-powered risk assessment
        3. **Review Results** - Understand implications and next steps
        """)
        
        # Demo mode indicator
        if st.session_state.config.get('demo_mode', True):
            st.warning("🤖 **Demo Mode**")
            st.markdown("""
            Currently running with mock responses.
            
            To enable real AI analysis, add your API keys:
            - OpenAI API Key
            - Cohere API Key
            - Groq API Key
            - Gemini API Key
            """)
        else:
            st.success("✅ **AI Mode**")
            st.markdown("Real AI analysis enabled!")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Clause input section
        clause_input()
        
        # Analysis sections
        if st.session_state.get('clause_text'):
            st.markdown("---")
            
            # Risk analysis
            risk_classifier()
            
            st.markdown("---")
            
            # Compliance analysis
            compliance_checker()
    
    with col2:
        # Sample clauses for quick testing
        st.markdown("### 🧪 Quick Test")
        st.markdown("Try these sample clauses:")
        
        sample_clauses = {
            "High Risk - Indemnification": "The Client shall indemnify, defend, and hold harmless the Provider against any and all claims, damages, losses, and expenses, including attorneys' fees, arising from or relating to the Client's use of the services, regardless of the cause.",
            "Medium Risk - Termination": "Either party may terminate this agreement upon 30 days written notice. Upon termination, all outstanding payments shall become immediately due and payable.",
            "Low Risk - Confidentiality": "Both parties agree to maintain the confidentiality of any proprietary information shared during the course of this agreement. This obligation shall survive termination of the agreement."
        }
        
        # Create smaller, more compact buttons
        for title, clause in sample_clauses.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{title}**")
            with col2:
                if st.button("Try", key=f"sample_{title}", help=f"Load {title} sample"):
                    st.session_state.clause_text = clause
                    st.rerun()
            # Reduce space between rows
            st.markdown("<div style='margin-bottom: 0.2rem;'></div>", unsafe_allow_html=True)
        
        # Sample data download section
        st.markdown("---")
        st.markdown("### 📄 Sample Data")
        st.markdown("""
        Download comprehensive sample clauses for testing:
        - 20+ clauses across all risk levels
        - Compliance-focused examples
        - Financial and time-based clauses
        """)
        
        # Robust sample file path
        sample_file_paths = [
            os.path.join(os.getcwd(), 'sample_clauses.md'),
            os.path.join(os.getcwd(), 'clause_risk_analyzer', 'sample_clauses.md')
        ]
        sample_data = None
        for path in sample_file_paths:
            if os.path.exists(path):
                with open(path, 'r') as file:
                    sample_data = file.read()
                break
        if sample_data:
            st.download_button(
                label="📥 Download Sample Clauses",
                data=sample_data,
                file_name="sample_contract_clauses.md",
                mime="text/markdown",
                help="Download comprehensive sample clauses for testing"
            )
        else:
            st.info("📄 Sample data file not found")

if __name__ == "__main__":
    main() 