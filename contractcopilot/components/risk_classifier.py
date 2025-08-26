import streamlit as st
import sys
import os

# Import from utils
from utils.llm_client import LLMClient

def risk_classifier():
    """Risk classification component using LLM analysis."""
    st.subheader("🔍 Risk Analysis")
    
    # Initialize LLM client
    if 'llm_client' not in st.session_state:
        st.session_state.llm_client = LLMClient()
    
    llm_client = st.session_state.llm_client
    
    # Get clause text from session state
    clause_text = st.session_state.get('clause_text', '')
    
    if not clause_text:
        st.info("Please enter a clause in the input section above.")
        return
    
    # Analyze button
    if st.button("🚀 Analyze Risk", type="primary"):
        with st.spinner("Analyzing clause risk with AI..."):
            try:
                # Get risk analysis from LLM
                risk_analysis = llm_client.analyze_clause_risk(clause_text)
                
                # Display results
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Risk level indicator
                    risk_level = risk_analysis.get('risk_level', 'unknown').upper()
                    confidence = risk_analysis.get('confidence', 0)
                    
                    if risk_level == 'HIGH':
                        st.error(f"🚨 {risk_level} RISK")
                        st.metric("Confidence", f"{confidence}%")
                    elif risk_level == 'MEDIUM':
                        st.warning(f"⚠️ {risk_level} RISK")
                        st.metric("Confidence", f"{confidence}%")
                    else:
                        st.success(f"✅ {risk_level} RISK")
                        st.metric("Confidence", f"{confidence}%")
                    
                    # Clause type
                    clause_type = risk_analysis.get('clause_type', 'Unknown')
                    st.info(f"**Clause Type:** {clause_type.title()}")
                
                with col2:
                    # Explanation
                    explanation = risk_analysis.get('explanation', 'No explanation available.')
                    st.markdown(f"**Analysis:** {explanation}")
                    
                    # Key risks
                    key_risks = risk_analysis.get('key_risks', [])
                    if key_risks:
                        st.markdown("**Key Risks:**")
                        for risk in key_risks:
                            st.markdown(f"• {risk}")
                    
                    # Recommendations
                    recommendations = risk_analysis.get('recommendations', [])
                    if recommendations:
                        st.markdown("**Recommendations:**")
                        for rec in recommendations:
                            st.markdown(f"• {rec}")
                
                # Store results in session state
                st.session_state.risk_analysis = risk_analysis
                
            except Exception as e:
                st.error(f"Error during analysis: {e}")
                st.info("Falling back to demo mode...")
                
                # Fallback to mock analysis
                risk_analysis = llm_client._generate_mock_risk_analysis(clause_text)
                st.session_state.risk_analysis = risk_analysis
                
                # Display fallback results
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    risk_level = risk_analysis.get('risk_level', 'unknown').upper()
                    confidence = risk_analysis.get('confidence', 0)
                    
                    if risk_level == 'HIGH':
                        st.error(f"🚨 {risk_level} RISK")
                        st.metric("Confidence", f"{confidence}%")
                    elif risk_level == 'MEDIUM':
                        st.warning(f"⚠️ {risk_level} RISK")
                        st.metric("Confidence", f"{confidence}%")
                    else:
                        st.success(f"✅ {risk_level} RISK")
                        st.metric("Confidence", f"{confidence}%")
                    
                    clause_type = risk_analysis.get('clause_type', 'Unknown')
                    st.info(f"**Clause Type:** {clause_type.title()}")
                
                with col2:
                    explanation = risk_analysis.get('explanation', 'No explanation available.')
                    st.markdown(f"**Analysis:** {explanation}")
                    
                    key_risks = risk_analysis.get('key_risks', [])
                    if key_risks:
                        st.markdown("**Key Risks:**")
                        for risk in key_risks:
                            st.markdown(f"• {risk}")
                    
                    recommendations = risk_analysis.get('recommendations', [])
                    if recommendations:
                        st.markdown("**Recommendations:**")
                        for rec in recommendations:
                            st.markdown(f"• {rec}")
    
    # Display previous results if available
    elif 'risk_analysis' in st.session_state:
        risk_analysis = st.session_state.risk_analysis
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            risk_level = risk_analysis.get('risk_level', 'unknown').upper()
            confidence = risk_analysis.get('confidence', 0)
            
            if risk_level == 'HIGH':
                st.error(f"🚨 {risk_level} RISK")
                st.metric("Confidence", f"{confidence}%")
            elif risk_level == 'MEDIUM':
                st.warning(f"⚠️ {risk_level} RISK")
                st.metric("Confidence", f"{confidence}%")
            else:
                st.success(f"✅ {risk_level} RISK")
                st.metric("Confidence", f"{confidence}%")
            
            clause_type = risk_analysis.get('clause_type', 'Unknown')
            st.info(f"**Clause Type:** {clause_type.title()}")
        
        with col2:
            explanation = risk_analysis.get('explanation', 'No explanation available.')
            st.markdown(f"**Analysis:** {explanation}")
            
            key_risks = risk_analysis.get('key_risks', [])
            if key_risks:
                st.markdown("**Key Risks:**")
                for risk in key_risks:
                    st.markdown(f"• {risk}")
            
            recommendations = risk_analysis.get('recommendations', [])
            if recommendations:
                st.markdown("**Recommendations:**")
                for rec in recommendations:
                    st.markdown(f"• {rec}")
    
    # Show demo mode indicator
    if st.session_state.get('config', {}).get('demo_mode', True):
        st.info("🤖 **Demo Mode**: Using AI-powered analysis with fallback responses. Add API keys for real LLM analysis.") 