import streamlit as st
import sys
import os

# Import from utils
from utils.llm_client import LLMClient

def compliance_checker():
    """Compliance checking component using LLM analysis."""
    st.subheader("⚖️ Compliance Analysis")
    
    # Initialize LLM client
    if 'llm_client' not in st.session_state:
        st.session_state.llm_client = LLMClient()
    
    llm_client = st.session_state.llm_client
    
    # Get clause text from session state
    clause_text = st.session_state.get('clause_text', '')
    
    if not clause_text:
        st.info("Please enter a clause in the input section above.")
        return
    
    # Compliance frameworks to check
    frameworks = {
        "GDPR": "General Data Protection Regulation",
        "CCPA": "California Consumer Privacy Act", 
        "SOX": "Sarbanes-Oxley Act",
        "HIPAA": "Health Insurance Portability and Accountability Act",
        "PCI-DSS": "Payment Card Industry Data Security Standard"
    }
    
    # Check compliance button
    if st.button("🔍 Check Compliance", type="secondary"):
        # Mark that compliance button was clicked
        st.session_state.compliance_clicked = True
        
        with st.spinner("Analyzing compliance requirements..."):
            try:
                # Get compliance analysis from LLM
                compliance_analysis = llm_client.analyze_compliance(clause_text, frameworks)
                
                # Display results
                st.markdown("### 📋 Compliance Assessment")
                
                # Overall compliance score
                overall_score = compliance_analysis.get('overall_score', 0)
                if overall_score >= 80:
                    st.success(f"✅ **Overall Compliance Score: {overall_score}%**")
                elif overall_score >= 60:
                    st.warning(f"⚠️ **Overall Compliance Score: {overall_score}%**")
                else:
                    st.error(f"🚨 **Overall Compliance Score: {overall_score}%**")
                
                # Framework-specific analysis
                st.markdown("### 🏛️ Framework Analysis")
                
                for framework, description in frameworks.items():
                    framework_data = compliance_analysis.get('frameworks', {}).get(framework, {})
                    
                    with st.expander(f"{framework} - {description}", expanded=False):
                        compliance_level = framework_data.get('compliance_level', 'Unknown')
                        issues = framework_data.get('issues', [])
                        recommendations = framework_data.get('recommendations', [])
                        
                        # Compliance level indicator
                        if compliance_level == 'Compliant':
                            st.success(f"✅ {compliance_level}")
                        elif compliance_level == 'Partial':
                            st.warning(f"⚠️ {compliance_level}")
                        else:
                            st.error(f"🚨 {compliance_level}")
                        
                        # Issues
                        if issues:
                            st.markdown("**Issues Found:**")
                            for issue in issues:
                                st.markdown(f"• {issue}")
                        
                        # Recommendations
                        if recommendations:
                            st.markdown("**Recommendations:**")
                            for rec in recommendations:
                                st.markdown(f"• {rec}")
                
                # Store results in session state
                st.session_state.compliance_analysis = compliance_analysis
                
            except Exception as e:
                st.error(f"Error during compliance analysis: {e}")
    
    # Display previous results only if button was clicked and analysis exists
    elif 'compliance_analysis' in st.session_state and st.session_state.get('compliance_clicked', False):
        compliance_analysis = st.session_state.compliance_analysis
        
        st.markdown("### 📋 Compliance Assessment")
        
        overall_score = compliance_analysis.get('overall_score', 0)
        if overall_score >= 80:
            st.success(f"✅ **Overall Compliance Score: {overall_score}%**")
        elif overall_score >= 60:
            st.warning(f"⚠️ **Overall Compliance Score: {overall_score}%**")
        else:
            st.error(f"🚨 **Overall Compliance Score: {overall_score}%**")
        
        st.markdown("### 🏛️ Framework Analysis")
        
        for framework, description in frameworks.items():
            framework_data = compliance_analysis.get('frameworks', {}).get(framework, {})
            
            with st.expander(f"{framework} - {description}", expanded=False):
                compliance_level = framework_data.get('compliance_level', 'Unknown')
                issues = framework_data.get('issues', [])
                recommendations = framework_data.get('recommendations', [])
                
                if compliance_level == 'Compliant':
                    st.success(f"✅ {compliance_level}")
                elif compliance_level == 'Partial':
                    st.warning(f"⚠️ {compliance_level}")
                else:
                    st.error(f"🚨 {compliance_level}")
                
                if issues:
                    st.markdown("**Issues Found:**")
                    for issue in issues:
                        st.markdown(f"• {issue}")
                
                if recommendations:
                    st.markdown("**Recommendations:**")
                    for rec in recommendations:
                        st.markdown(f"• {rec}") 