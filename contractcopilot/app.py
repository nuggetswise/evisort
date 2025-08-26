import streamlit as st
import os
import time

# Import from local utils
from utils.config import load_config
from utils.llm_client import LLMClient
from components.clause_input import clause_input

from agents import Agent, split_into_clauses

# Page configuration
st.set_page_config(
    page_title="ContractCopilot - AI Contract Intelligence",
    page_icon="🤖",
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

# -----------------------------
# Helpers: file reading & retrieval
# -----------------------------

def _read_file(uploaded) -> str:
    name = uploaded.name.lower()
    if name.endswith(".txt"):
        return uploaded.read().decode("utf-8", errors="ignore")
    if name.endswith(".md"):
        return uploaded.read().decode("utf-8", errors="ignore")
    if name.endswith(".docx"):
        try:
            from docx import Document
            doc = Document(uploaded)
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception:
            return ""
    if name.endswith(".pdf"):
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(uploaded)
            text = ""
            for p in reader.pages:
                text += p.extract_text() or ""
            return text
        except Exception:
            return ""
    return uploaded.read().decode("utf-8", errors="ignore")

def load_compliance_contracts():
    """Load compliance contract files with user-friendly names"""
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    compliance_files = {
        # GDPR Contracts
        "🛡️ GDPR Data Processing Agreement": "gdpr_data_processing_agreement.md",
        "🛡️ GDPR SaaS Subscription Agreement": "gdpr_saas_subscription_agreement.md",
        
        # CCPA Contracts
        "🔒 CCPA Data Sharing Addendum": "ccpa_data_sharing_addendum.md",
        "🔒 CCPA Marketing Services Agreement": "ccpa_marketing_services_agreement.md",
        
        # HIPAA Contracts
        "🏥 HIPAA Business Associate Agreement": "hipaa_business_associate_agreement.md",
        "🏥 HIPAA Telehealth Services Agreement": "hipaa_telehealth_services_agreement.md"
    }
    
    loaded_contracts = {}
    for display_name, filename in compliance_files.items():
        file_path = os.path.join(assets_dir, filename)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                loaded_contracts[display_name] = content
            except Exception as e:
                st.warning(f"Could not load {display_name}: {e}")
    
    return loaded_contracts


def main():
    # Initialize configuration
    if 'config' not in st.session_state:
        st.session_state.config = load_config()
    
    # Initialize LLM client
    if 'llm_client' not in st.session_state:
        st.session_state.llm_client = LLMClient()
    
    # Test agent functionality
    if 'agent_tested' not in st.session_state:
        try:
            test_agent = Agent(st.session_state.llm_client)
            test_result = test_agent.classify("test query")
            st.session_state.agent_tested = True
        except Exception as e:
            st.error(f"Agent initialization failed: {e}")
            st.session_state.agent_tested = False
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 ContractCopilot</h1>
        <p>Your AI-powered contract intelligence partner</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with information
    with st.sidebar:
        st.markdown("### 🎯 How to Use This Tool")
        st.markdown("""
        **Input Contract Data:**
        - **📄 Select Contract** – Choose from 6 compliance contracts
        - **📝 Paste Text** – Custom clause or contract text

        **Run Agentic Analysis:**
        - Policy lens auto-detected from selected contract
        - Click "Run Agentic Analysis" for comprehensive review
        - Get grounded answers with citations and safer clause proposals

        **Next Actions:**
        - Insert safer clauses, create trackers, export decisions
        """)
        
        # API Status
        st.success("✅ **AI Mode**")
        st.markdown("Real AI analysis enabled!")
        
        # Agent Status
        if st.session_state.get('agent_tested', False):
            st.success("🤖 **Agentic Pipeline Ready**")
        else:
            st.error("❌ **Agentic Pipeline Failed**")
            st.info("Check API keys and dependencies")
        
        # Revisions Buffer
        if st.session_state.get('revisions_buffer'):
            st.markdown("---")
            st.markdown("### 📋 Revisions Buffer")
            for i, revision in enumerate(st.session_state.revisions_buffer[-3:], 1):  # Show last 3
                with st.expander(f"Revision {i} ({revision['timestamp']})", expanded=False):
                    st.markdown("**Original:**")
                    st.code(revision['original'][:200] + "..." if len(revision['original']) > 200 else revision['original'])
                    st.markdown("**Safer Clause:**")
                    st.code(revision['safer_clause'])
            
            if len(st.session_state.revisions_buffer) > 3:
                st.caption(f"... and {len(st.session_state.revisions_buffer) - 3} more revisions")
            
            if st.button("🗑️ Clear Buffer", type="secondary"):
                st.session_state.revisions_buffer = []
                st.rerun()

    # Main content area
    st.subheader("🤖 Agentic Contract Intelligence")
    
    # Unified input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Single unified input area
        st.markdown("### 📝 Input Contract Data")
        
        # Unified input section
        st.markdown("#### 📋 Select Contract or Paste Text")
        
        # Load compliance contracts
        compliance_contracts = load_compliance_contracts()
        
        # Input method selection
        input_method = st.radio(
            "Choose input method:",
            ["📄 Select from Compliance Contracts", "📝 Paste Custom Text"],
            horizontal=True
        )
        
        clauses = []
        analysis_type = ""
        file_map = []
        
        if input_method == "📄 Select from Compliance Contracts":
            if compliance_contracts:
                # Single dropdown with all contracts
                selected_contract = st.selectbox(
                    "Choose a compliance contract:",
                    ["Select a contract..."] + list(compliance_contracts.keys()),
                    help="Select one of the pre-loaded GDPR, CCPA, or HIPAA compliance contracts"
                )
                
                if selected_contract != "Select a contract...":
                    text = compliance_contracts[selected_contract]
                    contract_clauses = split_into_clauses(text)
                    clauses = contract_clauses
                    file_map = [(selected_contract, 0, len(contract_clauses))]
                    analysis_type = "Compliance Contract"
                    
                    st.success(f"✅ Loaded: {selected_contract}")
                else:
                    st.info("👆 Please select a compliance contract to analyze")
            else:
                st.error("❌ No compliance contracts found. Please ensure the contract files are in the assets directory.")
        
        else:  # Paste Custom Text
            clause_input()
            clause_text = st.session_state.get('clause_text', '')
            if clause_text:
                clauses = [clause_text]
                analysis_type = "Custom Text"
                
                # Policy lens selection for custom text
                st.markdown("---")
                st.markdown("#### 🎯 Select Compliance Framework")
                policy_lens = st.multiselect(
                    "Choose applicable compliance frameworks:",
                    ["GDPR", "CCPA", "HIPAA", "General Compliance"],
                    help="Select the compliance frameworks that apply to your text"
                )
        
        # Run Agentic Analysis
        if clauses:
            # Auto-detect policy lens from selected contracts
            if analysis_type == "Compliance Contract":
                policy_lens = []
                if "GDPR" in selected_contract:
                    policy_lens.append("GDPR")
                if "CCPA" in selected_contract:
                    policy_lens.append("CCPA")
                if "HIPAA" in selected_contract:
                    policy_lens.append("HIPAA")
            # For Custom Text, policy_lens is already defined
            elif analysis_type == "Custom Text" and not policy_lens:
                # Fallback if no policy lens selected
                policy_lens = ["General Compliance"]
            
            st.markdown("---")
            st.markdown("### 🤖 Agentic Analysis")
            
            # Primary CTA with dynamic label
            cta_label = "🚀 Run Agentic Analysis"
            if st.button(cta_label, type="primary", use_container_width=True):
                # Create question based on policy lens
                if policy_lens:
                    policy_text = ", ".join(policy_lens)
                    question = (
                        f"Analyze this contract data for risk level, compliance with {policy_text}, and suggest specific improvements to make it safer and more protective."
                    )
                else:
                    question = (
                        "Analyze this contract data for risk level, compliance with regulatory frameworks, and suggest specific improvements to make it safer and more protective."
                    )
                
                # Helper copy
                st.caption("Classify → Retrieve → Synthesize → Propose (with citations).")
                st.caption("Grounded in retrieved clauses; every answer includes citations.")
                st.caption("Safer clause proposals use governed templates (no free-form drafting).")
                
                # Run agentic analysis
                try:
                    with st.spinner("Running agentic analysis..."):
                        agent = Agent(st.session_state.llm_client)
                        # Pass file_map for contract analysis
                        file_map_to_pass = file_map if analysis_type == "Compliance Contract" else None
                        result = agent.run(question, clauses, top_k=5, file_map=file_map_to_pass)
                    
                    # Dynamic CTA label based on intent
                    intent = result['intent']
                    if intent == 'qa':
                        cta_label = "🚀 Run Agentic Analysis"
                    elif intent == 'extract':
                        cta_label = "📊 Extract & Summarize"
                    elif intent == 'redline':
                        cta_label = "💡 Propose Safer Clause"
                    else:
                        cta_label = "🚀 Run Agentic Analysis"
                    
                    # Show detected intent
                    st.caption(f"Intent: {intent.upper()} → Steps: {' → '.join(result['steps'])}")
                    
                    # Display AI analysis
                    st.markdown("**🤖 AI Answer:**")
                    st.write(result['answer'])
                    
                    # Display safer clause only if relevant
                    if result['proposal'] and (result['intent'] == 'redline' or any(word in question.lower() for word in ['risk', 'safer', 'improve', 'better', 'liability', 'indemn'])):
                        st.markdown("**💡 Suggested Safer Clause:**")
                        st.write(result['proposal'])
                    
                    # Next Actions
                    st.markdown("---")
                    st.markdown("### 🎯 Next Actions")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if result['proposal']:
                            if st.button("📋 Insert Safer Clause", help="Add to revisions buffer"):
                                if 'revisions_buffer' not in st.session_state:
                                    st.session_state.revisions_buffer = []
                                st.session_state.revisions_buffer.append({
                                    'original': clauses[0] if len(clauses) == 1 else "Multiple clauses",
                                    'safer_clause': result['proposal'],
                                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                                })
                                st.success("✅ Added to revisions buffer!")
                    with col2:
                        if st.button("📊 Create Tracker", help="Create tracking item for this finding"):
                            st.info("📊 Tracker created: " + intent.upper() + " Analysis")
                    with col3:
                        if st.button("📄 Export Decision", help="Export analysis to Markdown/PDF"):
                            export_data = f"""
# Contract Analysis Report

## AI Answer
{result['answer']}

## Intent
{result['intent'].upper()}

## Pipeline Steps
{' → '.join(result['steps'])}

## Citations
{chr(10).join([f"- Score: {c['score']:.2f}" for c in result['citations']])}

## Safer Clause Proposal
{result['proposal'] if result['proposal'] else 'None provided'}

---
Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}
                            """
                            st.download_button(
                                label="📄 Download Report",
                                data=export_data,
                                file_name=f"contract_analysis_{time.strftime('%Y%m%d_%H%M%S')}.md",
                                mime="text/markdown"
                            )
                    with col4:
                        if st.button("📋 Copy Answer", help="Copy answer to clipboard"):
                            st.success("📋 Answer copied to clipboard!")
                        
                except Exception as e:
                    st.error(f"Error in agentic analysis: {e}")
                    st.info("Debug info: Check if LLM client is properly initialized and API keys are set.")
    
    with col2:
        # Sample data download section
        st.markdown("### 📄 Sample Data")
        st.markdown("Download all sample contracts as a single zip file:")
        
        # Create zip file with all contracts
        import zipfile
        import io
        
        def create_contracts_zip():
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
                
                # Add compliance contracts
                compliance_files = {
                    "GDPR_Data_Processing_Agreement.md": "gdpr_data_processing_agreement.md",
                    "GDPR_SaaS_Subscription_Agreement.md": "gdpr_saas_subscription_agreement.md",
                    "CCPA_Data_Sharing_Addendum.md": "ccpa_data_sharing_addendum.md",
                    "CCPA_Marketing_Services_Agreement.md": "ccpa_marketing_services_agreement.md",
                    "HIPAA_Business_Associate_Agreement.md": "hipaa_business_associate_agreement.md",
                    "HIPAA_Telehealth_Services_Agreement.md": "hipaa_telehealth_services_agreement.md"
                }
                
                for display_name, filename in compliance_files.items():
                    file_path = os.path.join(assets_dir, filename)
                    if os.path.exists(file_path):
                        zip_file.write(file_path, display_name)
            
            zip_buffer.seek(0)
            return zip_buffer.getvalue()
        
        # Download button for zip file
        try:
            zip_data = create_contracts_zip()
            st.download_button(
                label="📦 Download All Contracts (ZIP)",
                data=zip_data,
                file_name="contractcopilot_sample_contracts.zip",
                mime="application/zip",
                help="Download all sample contracts and compliance agreements"
            )
            st.caption("Contains all 6 GDPR, CCPA, and HIPAA compliance contracts")
        except Exception as e:
            st.error(f"Error creating zip file: {e}")
        
        st.markdown("---")
        
        # Compliance contracts info
        st.markdown("### 🛡️ Compliance Contracts")
        st.info("""
        **Available for Multi-Selection:**
        - 🛡️ GDPR Data Processing & SaaS Agreements
        - 🔒 CCPA Data Sharing & Marketing Contracts  
        - 🏥 HIPAA Business Associate & Telehealth Agreements
        
        Select from the "📋 Compliance Contracts" tab!
        """)

if __name__ == "__main__":
    main()