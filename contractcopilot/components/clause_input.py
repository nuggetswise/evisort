import streamlit as st
from typing import Optional

def clause_input():
    """
    Render the clause input interface and return the entered text.
    """
    # Check if we have a clause from session state (from sample buttons)
    if 'clause_text' in st.session_state:
        default_text = st.session_state.clause_text
        # Clear it after use
        del st.session_state.clause_text
    else:
        default_text = ""
    
    # Input area
    clause_text = st.text_area(
        "Paste your legal clause here:",
        value=default_text,
        height=200,
        placeholder="Example: INDEMNIFICATION. The Client shall indemnify, defend, and hold harmless...",
        help="Paste any legal clause to analyze its risk level and extract key metadata."
    )
    
    # Store in session state for other components
    if clause_text:
        # Check if text has changed from previous analysis
        previous_text = st.session_state.get('previous_clause_text', '')
        if clause_text != previous_text:
            # Clear previous analysis results when text changes
            if 'risk_analysis' in st.session_state:
                del st.session_state.risk_analysis
            if 'compliance_analysis' in st.session_state:
                del st.session_state.compliance_analysis
            if 'risk_clicked' in st.session_state:
                del st.session_state.risk_clicked
            if 'compliance_clicked' in st.session_state:
                del st.session_state.compliance_clicked
            # Update previous text
            st.session_state.previous_clause_text = clause_text
        
        st.session_state.clause_text = clause_text
    
    # Character count
    if clause_text:
        char_count = len(clause_text)
        word_count = len(clause_text.split())
        st.caption(f"📊 {char_count} characters, {word_count} words")
    
    # Quick actions
    if clause_text:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Clear", type="secondary"):
                if 'clause_text' in st.session_state:
                    del st.session_state.clause_text
                st.rerun()
        with col2:
            if st.button("📋 Copy", type="secondary"):
                st.write("📋 Copied to clipboard!")
    
    return clause_text 