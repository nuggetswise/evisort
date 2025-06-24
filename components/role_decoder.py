import streamlit as st
import pandas as pd
from utils.config import get_workday_job_posting
from utils.llm_client import LLMClient

class RoleDecoder:
    def __init__(self):
        self.llm_client = st.session_state.get('llm_client', LLMClient())
        self.job_posting = get_workday_job_posting()
    
    def render(self):
        """Render the Role Decoder section."""
        st.markdown('<h2 class="section-header">🧭 Role Decoder</h2>', unsafe_allow_html=True)
        
        # Job posting display
        with st.expander("📋 View Original Job Posting", expanded=False):
            st.markdown(self.job_posting)
        
        # Analysis sections
        col1, col2 = st.columns([1, 1])
        
        with col1:
            self._render_core_analysis()
        
        with col2:
            self._render_skills_analysis()
        
        # Metrics and KPIs
        st.markdown("---")
        self._render_metrics_analysis()
        
        # Role fit assessment
        st.markdown("---")
        self._render_role_fit()
    
    def _render_core_analysis(self):
        """Render core responsibilities and AI/ML focus analysis."""
        st.markdown("### 🎯 Core Responsibilities & AI/ML Focus")
        
        with st.spinner("Analyzing core responsibilities..."):
            responsibilities_prompt = """
            Analyze the following job posting and extract:
            1. Core responsibilities
            2. AI/ML product focus areas
            3. Key technical requirements
            
            Job Posting:
            """ + self.job_posting
            
            response = self.llm_client.generate_response(
                responsibilities_prompt,
                system_prompt="You are an expert product manager analyzing job requirements. Provide clear, structured insights."
            )
            
            st.markdown(response)
    
    def _render_skills_analysis(self):
        """Render skills and requirements analysis."""
        st.markdown("### 🔧 Required Skills & Competencies")
        
        with st.spinner("Analyzing required skills..."):
            skills_prompt = """
            Extract and categorize the required skills and competencies from this job posting:
            1. Technical skills
            2. Product management skills
            3. Domain knowledge requirements
            4. Preferred qualifications
            
            Job Posting:
            """ + self.job_posting
            
            response = self.llm_client.generate_response(
                skills_prompt,
                system_prompt="You are a technical recruiter analyzing candidate requirements. Provide detailed skill breakdowns."
            )
            
            st.markdown(response)
    
    def _render_metrics_analysis(self):
        """Render metrics and KPIs analysis."""
        st.markdown("### 📊 Key Metrics & Success Indicators")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.spinner("Analyzing success metrics..."):
                metrics_prompt = """
                Based on this contract intelligence PM role, what would be the key metrics and KPIs to track success?
                Consider:
                1. Product metrics (accuracy, speed, adoption)
                2. Business metrics (revenue, customer satisfaction)
                3. Technical metrics (model performance, system reliability)
                4. User engagement metrics
                
                Job Posting:
                """ + self.job_posting
                
                response = self.llm_client.generate_response(
                    metrics_prompt,
                    system_prompt="You are a data-driven product manager. Focus on measurable, actionable metrics."
                )
                
                st.markdown(response)
        
        with col2:
            # Mock metrics visualization
            st.markdown("#### 📈 Sample Metrics Dashboard")
            
            metrics_data = {
                'Metric': ['Contract Accuracy', 'Processing Speed', 'User Adoption', 'Customer Satisfaction'],
                'Current': [94.2, 2.3, 78.5, 4.2],
                'Target': [95.0, 1.5, 85.0, 4.5],
                'Unit': ['%', 'min', '%', '/5']
            }
            
            df = pd.DataFrame(metrics_data)
            st.dataframe(df, use_container_width=True)
            
            # Progress bars
            st.markdown("#### 🎯 Progress Tracking")
            for i, row in df.iterrows():
                progress = (row['Current'] / row['Target']) * 100
                st.progress(min(progress, 100) / 100)
                st.caption(f"{row['Metric']}: {row['Current']}{row['Unit']} / {row['Target']}{row['Unit']}")
    
    def _render_role_fit(self):
        """Render role fit assessment."""
        st.markdown("### 🎯 Role Fit Assessment")
        
        # Role complexity analysis
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🧠 Technical Complexity")
            st.markdown("**High** - Requires deep AI/ML understanding")
            st.markdown("• LLM integration expertise")
            st.markdown("• NLP and contract parsing")
            st.markdown("• Enterprise software architecture")
        
        with col2:
            st.markdown("#### 🏢 Domain Complexity")
            st.markdown("**Medium-High** - Legal tech specialization")
            st.markdown("• Contract law understanding")
            st.markdown("• Compliance requirements")
            st.markdown("• Legal workflow optimization")
        
        with col3:
            st.markdown("#### 👥 Stakeholder Complexity")
            st.markdown("**High** - Cross-functional leadership")
            st.markdown("• Engineering teams")
            st.markdown("• Legal departments")
            st.markdown("• Enterprise customers")
        
        # Key challenges
        st.markdown("#### ⚠️ Key Challenges")
        challenges = [
            "Balancing AI accuracy with processing speed",
            "Navigating complex legal compliance requirements",
            "Managing enterprise customer expectations",
            "Scaling AI models for production use",
            "Integrating with existing legal workflows"
        ]
        
        for challenge in challenges:
            st.markdown(f"• {challenge}")
        
        # Success factors
        st.markdown("#### ✅ Success Factors")
        success_factors = [
            "Strong technical background in AI/ML",
            "Experience with enterprise software",
            "Understanding of legal domain",
            "Excellent stakeholder management",
            "Data-driven decision making"
        ]
        
        for factor in success_factors:
            st.markdown(f"• {factor}") 