import streamlit as st
import sys
import os

# Add the parent directory to the path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.llm_client import LLMClient

def metadata_extractor():
    """Metadata extraction component using LLM analysis."""
    st.subheader("📊 Metadata Extraction")
    
    # Initialize LLM client
    if 'llm_client' not in st.session_state:
        st.session_state.llm_client = LLMClient()
    
    llm_client = st.session_state.llm_client
    
    # Get clause text from session state
    clause_text = st.session_state.get('clause_text', '')
    
    if not clause_text:
        st.info("Please enter a clause in the input section above.")
        return
    
    # Extract button
    if st.button("🔍 Extract Metadata", type="secondary"):
        with st.spinner("Extracting metadata with AI..."):
            try:
                # Get metadata from LLM
                metadata = llm_client.extract_metadata(clause_text)
                
                # Display results in a clean format
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📅 Effective Date:**")
                    effective_date = metadata.get('effective_date', 'Not specified')
                    if effective_date:
                        st.info(effective_date)
                    else:
                        st.info("Not specified")
                    
                    st.markdown("**⏰ Termination Notice:**")
                    termination_notice = metadata.get('termination_notice', 'Not specified')
                    if termination_notice:
                        st.info(termination_notice)
                    else:
                        st.info("Not specified")
                    
                    st.markdown("**💰 Contract Value:**")
                    contract_value = metadata.get('contract_value', 'Not specified')
                    if contract_value:
                        st.info(contract_value)
                    else:
                        st.info("Not specified")
                    
                    st.markdown("**🛡️ Liability Cap:**")
                    liability_cap = metadata.get('liability_cap', 'Not specified')
                    if liability_cap:
                        st.info(liability_cap)
                    else:
                        st.info("Not specified")
                
                with col2:
                    st.markdown("**💳 Payment Terms:**")
                    payment_terms = metadata.get('payment_terms', 'Not specified')
                    if payment_terms:
                        st.info(payment_terms)
                    else:
                        st.info("Not specified")
                    
                    st.markdown("**📋 Clause Type:**")
                    clause_type = metadata.get('clause_type', 'Not specified')
                    if clause_type:
                        st.info(clause_type.title())
                    else:
                        st.info("Not specified")
                    
                    st.markdown("**🏛️ Jurisdiction:**")
                    jurisdiction = metadata.get('jurisdiction', 'Not specified')
                    if jurisdiction:
                        st.info(jurisdiction)
                    else:
                        st.info("Not specified")
                    
                    st.markdown("**👥 Parties Mentioned:**")
                    parties = metadata.get('parties_mentioned', [])
                    if parties:
                        for party in parties:
                            st.info(party)
                    else:
                        st.info("Not specified")
                
                # Store results in session state
                st.session_state.metadata = metadata
                
            except Exception as e:
                st.error(f"Error during extraction: {e}")
                st.info("Falling back to demo mode...")
                
                # Fallback to mock metadata
                metadata = llm_client._generate_mock_metadata(clause_text)
                st.session_state.metadata = metadata
                
                # Display fallback results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📅 Effective Date:**")
                    st.info("Not specified")
                    
                    st.markdown("**⏰ Termination Notice:**")
                    st.info("Not specified")
                    
                    st.markdown("**💰 Contract Value:**")
                    st.info("Not specified")
                    
                    st.markdown("**🛡️ Liability Cap:**")
                    st.info("Not specified")
                
                with col2:
                    st.markdown("**💳 Payment Terms:**")
                    st.info("Not specified")
                    
                    st.markdown("**📋 Clause Type:**")
                    st.info("General")
                    
                    st.markdown("**🏛️ Jurisdiction:**")
                    st.info("Not specified")
                    
                    st.markdown("**👥 Parties Mentioned:**")
                    st.info("Not specified")
    
    # Display previous results if available
    elif 'metadata' in st.session_state:
        metadata = st.session_state.metadata
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📅 Effective Date:**")
            effective_date = metadata.get('effective_date', 'Not specified')
            if effective_date:
                st.info(effective_date)
            else:
                st.info("Not specified")
            
            st.markdown("**⏰ Termination Notice:**")
            termination_notice = metadata.get('termination_notice', 'Not specified')
            if termination_notice:
                st.info(termination_notice)
            else:
                st.info("Not specified")
            
            st.markdown("**💰 Contract Value:**")
            contract_value = metadata.get('contract_value', 'Not specified')
            if contract_value:
                st.info(contract_value)
            else:
                st.info("Not specified")
            
            st.markdown("**🛡️ Liability Cap:**")
            liability_cap = metadata.get('liability_cap', 'Not specified')
            if liability_cap:
                st.info(liability_cap)
            else:
                st.info("Not specified")
        
        with col2:
            st.markdown("**💳 Payment Terms:**")
            payment_terms = metadata.get('payment_terms', 'Not specified')
            if payment_terms:
                st.info(payment_terms)
            else:
                st.info("Not specified")
            
            st.markdown("**📋 Clause Type:**")
            clause_type = metadata.get('clause_type', 'Not specified')
            if clause_type:
                st.info(clause_type.title())
            else:
                st.info("Not specified")
            
            st.markdown("**🏛️ Jurisdiction:**")
            jurisdiction = metadata.get('jurisdiction', 'Not specified')
            if jurisdiction:
                st.info(jurisdiction)
            else:
                st.info("Not specified")
            
            st.markdown("**👥 Parties Mentioned:**")
            parties = metadata.get('parties_mentioned', [])
            if parties:
                for party in parties:
                    st.info(party)
            else:
                st.info("Not specified")
    
    # Show demo mode indicator
    if st.session_state.get('config', {}).get('demo_mode', True):
        st.info("🤖 **Demo Mode**: Using AI-powered extraction with fallback responses. Add API keys for real LLM analysis.") 