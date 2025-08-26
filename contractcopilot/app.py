import streamlit as st
import sys
import os

from typing import List, Dict, Tuple
import re

# Import from local utils
from utils.config import load_config
from utils.llm_client import LLMClient
from components.clause_input import clause_input
from components.risk_classifier import risk_classifier
from components.compliance_checker import compliance_checker

from agents import Agent, split_into_clauses, build_bm25_index, retrieve, propose_redline

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
        <h1>🤖 ContractCopilot</h1>
        <p>Your AI-powered contract intelligence partner</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with information
    with st.sidebar:
        st.markdown("### 🎯 How to Use This Tool")
        st.markdown("""
        **Choose your input method:**
        
        **📝 Paste Clause:**
        1. Paste a contract clause in the text area
        2. Click "🚀 Analyze Risk" for risk assessment
        3. Click "🔍 Check Compliance" for regulatory analysis
        
        **📁 Upload Files:**
        1. Upload multiple contract files
        2. Ask natural language questions
        3. Get AI answers with citations and safer clause suggestions
        """)
        
        # API Status
        st.success("✅ **AI Mode**")
        st.markdown("Real AI analysis enabled!")

    # Main content area
    st.subheader("🤖 Ask AI - Contract Intelligence")
    
    # Input method selection
    input_method = st.radio(
        "Choose your input method:",
        ["📝 Paste Clause", "📁 Upload Files"],
        horizontal=True
    )

    if input_method == "📝 Paste Clause":
        # Single clause analysis
        col1, col2 = st.columns([2, 1])
        with col1:
            # Clause input section
            clause_input()
            # Analysis sections
            st.markdown("---")
            # Risk analysis
            risk_classifier()
            st.markdown("---")
            # Compliance analysis
            compliance_checker()
        with col2:
            # Sample data download section
            st.markdown("### 📄 Sample Data")
            st.markdown("Download sample files for testing:")
            
            # Sample clauses for single clause analysis
            sample_clauses_path = os.path.join(os.path.dirname(__file__), 'assets', 'sample_clauses.md')
            if os.path.exists(sample_clauses_path):
                with open(sample_clauses_path, 'r') as file:
                    sample_clauses_data = file.read()
                st.download_button(
                    label="📥 Sample Clauses",
                    data=sample_clauses_data,
                    file_name="sample_clauses.md",
                    mime="text/markdown",
                    help="Individual clauses for single clause analysis"
                )
                st.caption("Individual clauses for risk & compliance analysis")
            
            st.markdown("---")
            
            # Sample contract for multi-contract analysis
            sample_contract_path = os.path.join(os.path.dirname(__file__), 'assets', 'sample_contract.md')
            if os.path.exists(sample_contract_path):
                with open(sample_contract_path, 'r') as file:
                    sample_contract_data = file.read()
                st.download_button(
                    label="📥 Sample Contract (MSA)",
                    data=sample_contract_data,
                    file_name="sample_contract.md",
                    mime="text/markdown",
                    help="Complete MSA contract for multi-contract analysis"
                )
                st.caption("Complete MSA for multi-contract Q&A testing")
    
    else:  # Upload Files
        st.markdown("### 📁 Upload Multiple Contracts")
        up_files = st.file_uploader("Upload contracts (TXT/PDF/DOCX/MD)", type=["txt","pdf","docx","md"], accept_multiple_files=True)
        if up_files:
            all_clauses = []
            file_map = []  # (filename, start_idx, end_idx)
            for f in up_files:
                text = _read_file(f)
                clauses = split_into_clauses(text)
                start = len(all_clauses)
                all_clauses.extend(clauses)
                file_map.append((f.name, start, len(all_clauses)))
            st.success(f"Indexed {len(all_clauses)} clauses from {len(up_files)} file(s).")
            idx, toks = build_bm25_index(all_clauses)
            q = st.text_input("Ask a question about your contracts (e.g., 'Which contracts have auto‑renewal with >60 days notice?')")
            if q:
                ranked = retrieve(q, all_clauses, idx, toks, k=5)
                top_clauses = []
                cites = []
                for i, score in ranked:
                    # find file for clause i
                    src_file = None
                    for name, s, e in file_map:
                        if s <= i < e:
                            src_file = name
                            break
                    snippet = all_clauses[i][:400] + ("..." if len(all_clauses[i])>400 else "")
                    top_clauses.append(all_clauses[i])
                    cites.append((src_file or "uploaded", i, score, snippet))
                # Use Agent to get answer
                agent = Agent(st.session_state.llm_client)
                analysis = agent.answer(q, top_clauses)
                answer = analysis.get("answer", "")
                st.markdown("### 🤖 AI Answer")
                st.write(answer)
                st.markdown("### 📋 Citations")
                for idx_pair, (fname, ci, sc, snip) in enumerate(cites, start=1):
                    st.markdown(f"**[{idx_pair}]** *{fname}* — clause #{ci} — score: {sc:.2f}")
                    st.code(snip)
                # Safer clause proposal
                proposed = propose_redline(top_clauses)
                st.markdown("---")
                st.markdown("### 💡 Suggested Safer Clause")
                st.write(proposed)

if __name__ == "__main__":
    main()