import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List
import PyPDF2
import io
from utils.llm_client import LLMClient

class ContractSimulator:
    def __init__(self):
        self.llm_client = st.session_state.get('llm_client', LLMClient())
    
    def render(self):
        """Render the Contract AI Simulator section."""
        st.markdown('<h2 class="section-header">📄 Contract AI Simulator</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        **Simulate Evisort-style AI contract analysis capabilities.** Upload a contract document or use our sample data to see how AI would extract clauses, identify metadata, and assess risks.
        """)
        
        # File upload section
        self._render_upload_section()
        
        # Analysis results
        if 'contract_analysis' in st.session_state:
            self._render_analysis_results()
        
        # Sample contract option
        if st.button("🔬 Try with Sample Contract"):
            self._load_sample_contract()
    
    def _render_upload_section(self):
        """Render the file upload section."""
        st.markdown("### 📤 Upload Contract Document")
        
        uploaded_file = st.file_uploader(
            "Choose a contract file (PDF, DOCX, or TXT)",
            type=['pdf', 'docx', 'txt'],
            help="Upload a contract document to analyze"
        )
        
        if uploaded_file is not None:
            # Process the uploaded file
            content = self._extract_text_from_file(uploaded_file)
            
            if content:
                st.success(f"✅ Successfully processed {uploaded_file.name}")
                
                # Show preview
                with st.expander("📄 Document Preview", expanded=False):
                    st.text_area("Document Content", content, height=200)
                
                # Analyze button
                if st.button("🔍 Analyze Contract with AI"):
                    with st.spinner("AI is analyzing your contract..."):
                        analysis = self.llm_client.analyze_document(content, "contract")
                        st.session_state.contract_analysis = analysis
                        st.rerun()
    
    def _extract_text_from_file(self, uploaded_file) -> str:
        """Extract text content from uploaded file."""
        try:
            if uploaded_file.type == "application/pdf":
                return self._extract_pdf_text(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return self._extract_docx_text(uploaded_file)
            elif uploaded_file.type == "text/plain":
                return uploaded_file.getvalue().decode("utf-8")
            else:
                st.error("Unsupported file type")
                return ""
        except Exception as e:
            st.error(f"Error processing file: {e}")
            return ""
    
    def _extract_pdf_text(self, uploaded_file) -> str:
        """Extract text from PDF file."""
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
            return ""
    
    def _extract_docx_text(self, uploaded_file) -> str:
        """Extract text from DOCX file."""
        try:
            from docx import Document
            doc = Document(uploaded_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading DOCX: {e}")
            return ""
    
    def _load_sample_contract(self):
        """Load and analyze a sample contract."""
        sample_contract = """
        SERVICE AGREEMENT
        
        This Service Agreement (the "Agreement") is entered into as of January 15, 2024, by and between:
        
        COMPANY A, a corporation organized under the laws of Delaware ("Client")
        and
        COMPANY B, a corporation organized under the laws of California ("Provider")
        
        WHEREAS, Client desires to engage Provider to provide certain services;
        WHEREAS, Provider is willing to provide such services on the terms and conditions set forth herein;
        
        NOW, THEREFORE, in consideration of the mutual promises contained herein, the parties agree as follows:
        
        1. SERVICES
        Provider shall provide consulting services related to data analysis and machine learning implementation as described in Exhibit A.
        
        2. TERM
        This Agreement shall commence on January 15, 2024 and continue for a period of one (1) year, unless earlier terminated as provided herein.
        
        3. PAYMENT TERMS
        Client shall pay Provider $500,000 for the services, payable in monthly installments of $41,667, due within 30 days of invoice.
        
        4. TERMINATION
        Either party may terminate this Agreement with 30 days written notice to the other party.
        
        5. CONFIDENTIALITY
        Each party shall maintain the confidentiality of the other party's confidential information for a period of 5 years following termination.
        
        6. LIMITATION OF LIABILITY
        In no event shall either party's liability exceed the amount paid by Client under this Agreement.
        
        7. GOVERNING LAW
        This Agreement shall be governed by the laws of the State of California.
        
        IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.
        """
        
        st.session_state.sample_contract = sample_contract
        
        with st.spinner("AI is analyzing the sample contract..."):
            analysis = self.llm_client.analyze_document(sample_contract, "contract")
            st.session_state.contract_analysis = analysis
        
        st.success("✅ Sample contract analyzed!")
        st.rerun()
    
    def _render_analysis_results(self):
        """Render the contract analysis results."""
        analysis = st.session_state.contract_analysis
        
        st.markdown("### 🔍 AI Analysis Results")
        st.markdown("*This is a simulated analysis for demonstration purposes*")
        
        # Create tabs for different analysis views
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Clauses", "📊 Metadata", "⚠️ Risks", "📈 Analytics"])
        
        with tab1:
            self._render_clauses_tab(analysis)
        
        with tab2:
            self._render_metadata_tab(analysis)
        
        with tab3:
            self._render_risks_tab(analysis)
        
        with tab4:
            self._render_analytics_tab(analysis)
    
    def _render_clauses_tab(self, analysis: Dict[str, Any]):
        """Render the clauses analysis tab."""
        st.markdown("#### 📋 Extracted Clauses")
        
        clauses = analysis.get('clauses', [])
        
        for clause in clauses:
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**{clause['type']} Clause**")
                    st.markdown(f"*{clause['content']}*")
                
                with col2:
                    confidence = clause.get('confidence', 0.9)
                    st.metric("Confidence", f"{confidence:.1%}")
        
        # Confidence distribution chart
        if clauses:
            confidence_data = [clause.get('confidence', 0.9) for clause in clauses]
            clause_types = [clause['type'] for clause in clauses]
            
            fig = px.bar(
                x=clause_types,
                y=confidence_data,
                title="Clause Extraction Confidence",
                labels={'x': 'Clause Type', 'y': 'Confidence'},
                color=confidence_data,
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_metadata_tab(self, analysis: Dict[str, Any]):
        """Render the metadata analysis tab."""
        st.markdown("#### 📊 Contract Metadata")
        
        metadata = analysis.get('metadata', {})
        
        # Display metadata in a structured format
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Contract Details**")
            for key, value in metadata.items():
                if key != 'parties':
                    st.markdown(f"• **{key.replace('_', ' ').title()}**: {value}")
        
        with col2:
            if 'parties' in metadata:
                st.markdown("**Contracting Parties**")
                for party in metadata['parties']:
                    st.markdown(f"• {party}")
        
        # Timeline visualization
        if 'effective_date' in metadata and 'expiration_date' in metadata:
            st.markdown("#### 📅 Contract Timeline")
            
            # Create a simple timeline
            timeline_data = {
                'Event': ['Effective Date', 'Current Date', 'Expiration Date'],
                'Date': [metadata['effective_date'], '2024-06-15', metadata['expiration_date']],
                'Status': ['Start', 'Current', 'End']
            }
            
            df = pd.DataFrame(timeline_data)
            st.dataframe(df, use_container_width=True)
    
    def _render_risks_tab(self, analysis: Dict[str, Any]):
        """Render the risk analysis tab."""
        st.markdown("#### ⚠️ Risk Assessment")
        
        risks = analysis.get('risks', [])
        
        # Risk summary
        risk_levels = [risk['level'] for risk in risks]
        risk_counts = pd.Series(risk_levels).value_counts()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Risk details
            for risk in risks:
                risk_color = {
                    'High': '🔴',
                    'Medium': '🟡',
                    'Low': '🟢'
                }.get(risk['level'], '⚪')
                
                st.markdown(f"{risk_color} **{risk['level']} Risk**: {risk['description']}")
                st.markdown(f"*Mitigation: {risk['mitigation']}*")
                st.markdown("---")
        
        with col2:
            # Risk distribution pie chart
            if not risk_counts.empty:
                fig = px.pie(
                    values=risk_counts.values,
                    names=risk_counts.index,
                    title="Risk Distribution",
                    color_discrete_map={
                        'High': '#ff4444',
                        'Medium': '#ffaa00',
                        'Low': '#44ff44'
                    }
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
    
    def _render_analytics_tab(self, analysis: Dict[str, Any]):
        """Render the analytics tab."""
        st.markdown("#### 📈 Contract Analytics")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Clauses", len(analysis.get('clauses', [])))
        
        with col2:
            avg_confidence = sum([c.get('confidence', 0.9) for c in analysis.get('clauses', [])]) / max(len(analysis.get('clauses', [])), 1)
            st.metric("Avg Confidence", f"{avg_confidence:.1%}")
        
        with col3:
            high_risks = len([r for r in analysis.get('risks', []) if r['level'] == 'High'])
            st.metric("High Risks", high_risks)
        
        with col4:
            st.metric("Processing Time", "2.3s")
        
        # Contract summary
        st.markdown("#### 📝 AI Summary")
        summary = analysis.get('summary', 'No summary available.')
        st.info(summary)
        
        # Performance metrics
        st.markdown("#### 🎯 Performance Metrics")
        
        metrics_data = {
            'Metric': ['Clause Extraction', 'Risk Assessment', 'Metadata Accuracy', 'Overall Confidence'],
            'Score': [94.2, 87.5, 91.8, 89.3],
            'Benchmark': [95.0, 85.0, 90.0, 88.0]
        }
        
        df = pd.DataFrame(metrics_data)
        
        # Create a comparison chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Current Score',
            x=df['Metric'],
            y=df['Score'],
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            name='Benchmark',
            x=df['Metric'],
            y=df['Benchmark'],
            marker_color='lightcoral'
        ))
        
        fig.update_layout(
            title="Performance vs Benchmark",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True) 