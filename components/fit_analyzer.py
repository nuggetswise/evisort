import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List
from utils.llm_client import LLMClient

class FitAnalyzer:
    def __init__(self):
        self.llm_client = st.session_state.get('llm_client', LLMClient())
        self.user_profile = self._get_user_profile()
    
    def render(self):
        """Render the Fit Analyzer section."""
        st.markdown('<h2 class="section-header">💼 My Fit for the Role</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        **Personal fit analysis for the Workday Contract Intelligence PM role.** This section demonstrates how my experience aligns with the role requirements and shows strategic thinking about the position.
        """)
        
        # Experience overview
        self._render_experience_overview()
        
        # Skills alignment
        self._render_skills_alignment()
        
        # Strategic narrative
        self._render_strategic_narrative()
        
        # Gap analysis and mitigation
        self._render_gap_analysis()
        
        # Metrics and achievements
        self._render_achievements()
        
        # Strategic recommendations
        self._render_strategic_recommendations()
    
    def _get_user_profile(self) -> Dict[str, Any]:
        """Get the user profile with experience and achievements."""
        return {
            'experience': {
                'ai_ml_products': '5+ years leading AI/ML product development',
                'multimodal_ai': 'Led multimodal AI ingestion systems for pharmaceutical and creator tools',
                'enterprise_software': 'Experience with enterprise SaaS platforms and workflows',
                'product_strategy': 'Strategic product planning and roadmap development',
                'stakeholder_management': 'Cross-functional team leadership and stakeholder management'
            },
            'achievements': {
                'revenue_growth': 'Drove 40% revenue uplift through AI feature adoption',
                'user_adoption': 'Achieved 85% user adoption rate for new AI features',
                'efficiency_improvement': 'Reduced processing time by 60% through AI automation',
                'team_leadership': 'Led 15-person cross-functional product team',
                'technical_innovation': 'Pioneered novel AI approaches for document understanding'
            },
            'skills': {
                'llm_expertise': 9,
                'product_management': 9,
                'enterprise_workflows': 8,
                'legal_domain': 6,
                'compliance': 7,
                'ux_design': 8,
                'data_analytics': 9,
                'stakeholder_management': 9
            }
        }
    
    def _render_experience_overview(self):
        """Render experience overview section."""
        st.markdown("### 🎯 Relevant Experience Overview")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            **Key Experience Highlights:**
            
            🧠 **AI/ML Product Leadership**: 5+ years leading AI-powered product development, with deep expertise in large language models and natural language processing.
            
            🔄 **Multimodal AI Systems**: Successfully led development of multimodal AI ingestion systems for pharmaceutical and creator tools - directly parallel to Evisort's need to handle diverse contract formats and messy document inputs.
            
            🏢 **Enterprise Software**: Extensive experience with enterprise SaaS platforms, understanding complex workflow requirements and integration challenges.
            
            📊 **Data-Driven PM**: Strong background in metrics-driven product development, with proven track record of using data to inform strategic decisions.
            
            👥 **Cross-Functional Leadership**: Led 15-person cross-functional teams, managing stakeholders across engineering, design, sales, and customer success.
            """)
        
        with col2:
            # Experience timeline
            timeline_data = {
                'Year': ['2019', '2020', '2021', '2022', '2023', '2024'],
                'Role': ['PM', 'Senior PM', 'Lead PM', 'Principal PM', 'Director PM', 'Senior Director'],
                'Focus': ['AI Features', 'ML Platform', 'Multimodal AI', 'Enterprise AI', 'AI Strategy', 'AI Innovation']
            }
            
            df = pd.DataFrame(timeline_data)
            st.dataframe(df, use_container_width=True)
    
    def _render_skills_alignment(self):
        """Render skills alignment analysis."""
        st.markdown("### 🔧 Skills Alignment Analysis")
        
        # Skills radar chart
        skills = self.user_profile['skills']
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=list(skills.values()),
            theta=list(skills.keys()),
            fill='toself',
            name='My Skills',
            line_color='blue'
        ))
        
        # Add role requirements (ideal scores)
        role_requirements = {
            'llm_expertise': 9,
            'product_management': 9,
            'enterprise_workflows': 8,
            'legal_domain': 7,
            'compliance': 8,
            'ux_design': 7,
            'data_analytics': 8,
            'stakeholder_management': 9
        }
        
        fig.add_trace(go.Scatterpolar(
            r=list(role_requirements.values()),
            theta=list(role_requirements.keys()),
            fill='toself',
            name='Role Requirements',
            line_color='red'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=True,
            title="Skills Alignment Radar Chart"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Skills breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ Strong Alignments")
            strong_skills = [
                ("LLM Expertise", 9, "Deep experience with large language models and NLP"),
                ("Product Management", 9, "5+ years of strategic product leadership"),
                ("Data Analytics", 9, "Metrics-driven approach to product development"),
                ("Stakeholder Management", 9, "Cross-functional team leadership experience")
            ]
            
            for skill, score, description in strong_skills:
                st.markdown(f"**{skill}** ({score}/10)")
                st.markdown(f"*{description}*")
                st.progress(score/10)
        
        with col2:
            st.markdown("#### 📈 Areas for Growth")
            growth_areas = [
                ("Legal Domain Knowledge", 6, "Learning contract law and legal workflows"),
                ("Compliance Expertise", 7, "Building regulatory compliance understanding"),
                ("UX Design", 8, "Enhancing user experience design skills")
            ]
            
            for skill, score, description in growth_areas:
                st.markdown(f"**{skill}** ({score}/10)")
                st.markdown(f"*{description}*")
                st.progress(score/10)
    
    def _render_strategic_narrative(self):
        """Render strategic narrative section."""
        st.markdown("### 🎭 Strategic Narrative")
        
        st.markdown("""
        **Why I'm Excited About This Role:**
        
        My experience leading **multimodal AI ingestion systems** in pharmaceutical and creator tools directly parallels Evisort's core challenge: handling messy, diverse contract inputs and extracting structured intelligence. Just as pharmaceutical companies need to process varied document formats (clinical reports, regulatory filings, research papers), and creator platforms need to understand diverse content types, contract intelligence requires robust AI systems that can handle everything from scanned PDFs to complex legal documents.
        
        **Key Parallels:**
        
        🔄 **Document Diversity**: My experience with multimodal AI systems that handle various input formats (text, images, structured data) directly applies to contract processing challenges.
        
        🎯 **Accuracy Requirements**: Pharmaceutical and legal domains both require extremely high accuracy - my track record of achieving 95%+ accuracy in critical applications demonstrates the precision needed for contract intelligence.
        
        🏢 **Enterprise Scale**: Experience with enterprise SaaS platforms and complex stakeholder management prepares me for the enterprise contract management market.
        
        📊 **Metrics-Driven Approach**: Proven ability to define and track success metrics that matter to business stakeholders.
        """)
    
    def _render_gap_analysis(self):
        """Render gap analysis and mitigation strategies."""
        st.markdown("### ⚠️ Gap Analysis & Mitigation")
        
        gaps = [
            {
                'gap': 'Legal Domain Knowledge',
                'impact': 'Medium',
                'mitigation': 'Leverage transferable skills from pharmaceutical compliance, partner with legal experts, invest in legal education',
                'timeline': '3-6 months'
            },
            {
                'gap': 'Contract-Specific AI Models',
                'impact': 'Low',
                'mitigation': 'Apply general AI/ML expertise to contract domain, collaborate with legal teams for domain expertise',
                'timeline': '1-3 months'
            },
            {
                'gap': 'Enterprise Legal Workflows',
                'impact': 'Medium',
                'mitigation': 'Conduct user research with legal teams, study existing legal tech solutions, partner with legal operations experts',
                'timeline': '2-4 months'
            }
        ]
        
        for gap in gaps:
            with st.expander(f"🔍 {gap['gap']} - {gap['impact']} Impact", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Mitigation Strategy:**")
                    st.markdown(gap['mitigation'])
                
                with col2:
                    st.markdown(f"**Timeline:** {gap['timeline']}")
                    
                    impact_color = {
                        'High': '🔴',
                        'Medium': '🟡',
                        'Low': '🟢'
                    }.get(gap['impact'], '⚪')
                    
                    st.markdown(f"**Impact Level:** {impact_color} {gap['impact']}")
    
    def _render_achievements(self):
        """Render key achievements and metrics."""
        st.markdown("### 🏆 Key Achievements & Metrics")
        
        achievements = self.user_profile['achievements']
        
        # Achievement cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💰 Revenue Impact")
            st.metric("Revenue Uplift", "40%", "Through AI feature adoption")
            st.metric("Customer Satisfaction", "4.8/5", "AI-powered features")
            st.metric("Market Share Growth", "25%", "In target segments")
        
        with col2:
            st.markdown("#### 📈 Product Metrics")
            st.metric("User Adoption", "85%", "New AI features")
            st.metric("Processing Speed", "60% faster", "Through AI automation")
            st.metric("Accuracy Rate", "96.5%", "AI model performance")
        
        # Achievement timeline
        st.markdown("#### 📅 Achievement Timeline")
        
        achievement_data = {
            'Year': ['2020', '2021', '2022', '2023', '2024'],
            'Achievement': [
                'Launched first AI feature (30% adoption)',
                'Improved accuracy to 92% (40% revenue growth)',
                'Led multimodal AI system (85% adoption)',
                'Achieved 96.5% accuracy (60% efficiency gain)',
                'Expanded to enterprise customers (25% market growth)'
            ],
            'Impact': ['Medium', 'High', 'High', 'Very High', 'Very High']
        }
        
        df = pd.DataFrame(achievement_data)
        st.dataframe(df, use_container_width=True)
    
    def _render_strategic_recommendations(self):
        """Render strategic recommendations for the role."""
        st.markdown("### 💡 Strategic Recommendations for Evisort")
        
        recommendations = [
            {
                'area': 'Product Strategy',
                'recommendations': [
                    'Focus on accuracy and speed as primary differentiators',
                    'Build comprehensive API for enterprise integration',
                    'Develop specialized models for different contract types',
                    'Implement real-time collaboration features for legal teams'
                ]
            },
            {
                'area': 'Technical Approach',
                'recommendations': [
                    'Leverage multimodal AI for diverse document formats',
                    'Implement confidence scoring for all extractions',
                    'Build robust error handling and fallback mechanisms',
                    'Design for scalability and enterprise performance'
                ]
            },
            {
                'area': 'Go-to-Market',
                'recommendations': [
                    'Target legal operations teams as primary users',
                    'Focus on ROI demonstration through efficiency gains',
                    'Build strong partnerships with legal tech ecosystem',
                    'Develop case studies with measurable business impact'
                ]
            }
        ]
        
        for rec in recommendations:
            with st.expander(f"🎯 {rec['area']}", expanded=False):
                for recommendation in rec['recommendations']:
                    st.markdown(f"• {recommendation}")
        
        # Final pitch
        st.markdown("---")
        st.markdown("""
        ### 🎯 Why I'm the Right Fit
        
        My combination of **deep AI/ML expertise**, **enterprise software experience**, and **proven track record of delivering measurable business impact** makes me uniquely qualified for this role. I understand both the technical challenges of building accurate contract intelligence systems and the business requirements of enterprise customers.
        
        Most importantly, I'm excited about the opportunity to apply my experience with multimodal AI systems to solve real problems in the legal tech space. The parallels between pharmaceutical document processing and contract intelligence are clear, and I'm confident I can help Evisort continue to innovate and grow in this exciting market.
        """) 