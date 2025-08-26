# 🧭 Workday PM Role Demo - Contract Intelligence

**This repository has been reorganized! The main application is now in the `contractcopilot/` directory.**

## 🎯 **New Structure**

The project has been reorganized into a clean, professional structure:

```
📁 contractcopilot/          # Main application directory
├── app.py                   # ContractCopilot application (unified agentic pipeline)
├── components/              # UI components (clause_input)
├── utils/                   # Core utilities (LLM client, config)
├── agents.py               # Agentic AI pipeline (classify→retrieve→synthesize→propose)
├── assets/                  # Sample data
├── docs/                    # Documentation
└── README.md               # Comprehensive documentation
```

## 🚀 **Quick Start**

```bash
# Navigate to the main application
cd contractcopilot

# Install dependencies
pip install -r requirements.txt

# Set up API keys (at least one required)
export OPENAI_API_KEY=sk-...      # or
export COHERE_API_KEY=...         # or  
export GROQ_API_KEY=...           # or
export GEMINI_API_KEY=...

# Run the application
streamlit run app.py
```

## 📋 **What's in ContractCopilot**

**ContractCopilot** is an AI-powered contract intelligence platform that demonstrates:

- **🤖 Unified Agentic Pipeline**: Single "Run Agentic Analysis" CTA for both single clauses and multi-contract corpus
- **🎯 Intent Classification**: Automatically detects QA, Extract, or Redline intent
- **📊 Business Outcomes**: Next-step actions (Insert, Track, Export, Copy) tied to business value
- **🔍 Explainability**: Citations with relevance scores and technical transparency
- **🛡️ Governance**: Policy lens configuration, template governance, export capabilities

## 🎯 **For Hiring Managers**

This demo showcases the technical product management skills, AI/ML expertise, and strategic thinking required for the **Workday Contract Intelligence PM role**.

**Key Demonstrations:**
- ✅ **AI/ML Integration & Innovation**: Multi-LLM architecture with fallback strategies
- ✅ **Technical Architecture & Scalability**: Modular design with agentic pipeline
- ✅ **Legal Document Analysis & Business Value**: Risk assessment, compliance checking, safer clause proposals
- ✅ **Product Strategy & Market Understanding**: Outcome-oriented design with business actions
- ✅ **Alignment with Workday Values**: Professional presentation, governance focus, explainability

## 🚀 **Agentic Features**

### **Unified Pipeline:**
- **Input**: Paste clause or upload files (tabs interface)
- **Configuration**: Optional policy lens (GDPR, CCPA, SOX, HIPAA, PCI-DSS)
- **Analysis**: "Run Agentic Analysis" button triggers complete pipeline
- **Output**: AI answer, citations, safer clause proposals, next-step actions

### **Business Actions:**
- **📋 Insert Safer Clause**: Adds to revisions buffer
- **📊 Create Tracker**: Creates tracking items for findings
- **📄 Export Decision**: Downloads comprehensive reports
- **📋 Copy Answer**: Copies analysis to clipboard

### **Technical Excellence:**
- **Intent Classification**: QA vs Extract vs Redline
- **Retrieval**: BM25 with keyword fallback
- **Synthesis**: Grounded answers with citations
- **Proposal**: Governed template-based safer clauses

## 📖 **Documentation**

- **Main README**: `contractcopilot/README.md` - Comprehensive project documentation
- **Technical Docs**: `contractcopilot/docs/` - Architecture and strategy documentation
- **Deployment**: `DEPLOYMENT.md` - Technical deployment guide
- **Feedback**: `contractcopilot/feedback` - Implementation status and UX recommendations

## 🔄 **Migration Notes**

The original scattered structure has been consolidated into a professional, organized codebase that demonstrates:
- **Clean Architecture**: Modular design with clear separation of concerns
- **Professional Documentation**: Comprehensive setup and usage guides
- **Production-Ready Organization**: Scalable structure for enterprise deployment
- **Agentic AI Implementation**: Modern AI architecture with business outcomes

---

**Navigate to `contractcopilot/` to explore the main application and comprehensive documentation.**
