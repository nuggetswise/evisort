# 🤖 ContractCopilot - AI-Powered Contract Intelligence

**Professional AI contract analysis platform demonstrating technical product management excellence.**

## 🎯 **Project Structure**

```
📁 contractcopilot/          # Main application directory
├── app.py                   # Streamlit application with unified agentic pipeline
├── agents.py               # AI agent pipeline (classify→retrieve→synthesize→propose)
├── components/              # UI components (clause input, risk classifier, compliance checker)
├── utils/                   # Core utilities (LLM client, config)
├── assets/                  # Compliance contract templates (GDPR, CCPA, HIPAA)
├── docs/                    # Technical documentation
└── README.md               # Project documentation
```

## 🚀 **Quick Start**

```bash
# Navigate to the main application
cd contractcopilot

# Install dependencies
pip install -r requirements.txt

# Configure API keys (required for AI analysis)
# Option 1: Environment variables
export GEMINI_API_KEY="your_gemini_api_key"
export GROQ_API_KEY="your_groq_api_key"

# Option 2: Streamlit secrets file (.streamlit/secrets.toml)
GEMINI_API_KEY = "your_gemini_api_key"
GROQ_API_KEY = "your_groq_api_key"

# Run the application
streamlit run app.py
```

## 📋 **Key Features**

**ContractCopilot** is an AI-powered contract intelligence platform that demonstrates:

- **🤖 Agentic AI Pipeline**: Intelligent analysis with intent classification and grounded responses
- **🎯 Multi-LLM Architecture**: Gemini (primary) + Groq (fallback) for reliability
- **📊 Business Actions**: Insert safer clauses, create trackers, export decisions
- **🔍 Explainability**: Citations with relevance scores and technical transparency
- **🛡️ Compliance Focus**: GDPR, CCPA, HIPAA contract templates and analysis

## 🎯 **Technical Excellence**

This platform demonstrates advanced technical product management capabilities:

- ✅ **AI/ML Integration**: Multi-LLM architecture with intelligent fallback strategies
- ✅ **Technical Architecture**: Modular design with clean separation of concerns
- ✅ **Legal Domain Expertise**: Risk assessment, compliance checking, safer clause proposals
- ✅ **Product Strategy**: Outcome-oriented design with business value focus
- ✅ **Professional Quality**: Production-ready code organization and documentation

## 🚀 **How It Works**

### **Analysis Pipeline:**
1. **Input**: Select from compliance contracts or paste custom text
2. **Configuration**: Optional policy lens (GDPR, CCPA, HIPAA)
3. **Analysis**: "Run Agentic Analysis" triggers intelligent pipeline
4. **Output**: AI answer with citations and safer clause proposals

### **Business Actions:**
- **📋 Insert Safer Clause**: Adds AI-generated clauses to revisions buffer
- **📊 Create Tracker**: Creates tracking items for follow-up on findings
- **📄 Export Decision**: Downloads comprehensive analysis reports
- **📋 Copy Answer**: Copies analysis to clipboard for easy sharing

### **Technical Architecture:**
- **Intent Classification**: Automatically detects QA, Extract, or Redline intent
- **Retrieval**: BM25 search with keyword fallback for relevant clauses
- **Synthesis**: Grounded answers with citations and relevance scores
- **Proposal**: Template-based safer clause generation

## 📖 **Documentation**

- **Technical Docs**: `contractcopilot/docs/` - Architecture and strategy documentation
- **Deployment**: `DEPLOYMENT.md` - Technical deployment guide
- **Sample Contracts**: `contractcopilot/assets/` - GDPR, CCPA, HIPAA compliance templates

## 🔧 **API Configuration**

### **Required API Keys:**
- **Gemini API Key**: https://makersuite.google.com/app/apikey (Primary)
- **Groq API Key**: https://console.groq.com/ (Fallback)

### **Configuration Methods:**
1. **Environment Variables** (Recommended):
   ```bash
   export GEMINI_API_KEY="your_gemini_api_key"
   export GROQ_API_KEY="your_groq_api_key"
   ```

2. **Streamlit Secrets** (`.streamlit/secrets.toml`):
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key"
   GROQ_API_KEY = "your_groq_api_key"
   ```

## 🎯 **For Demo Purposes**

This platform demonstrates:
- **Professional AI Integration**: Multi-LLM architecture with intelligent fallback
- **Technical Product Management**: Clean architecture and modular design
- **Legal Domain Expertise**: Contract analysis and compliance checking
- **Business Value Focus**: Actionable insights and next-step recommendations

---

**Ready to run! Navigate to `contractcopilot/` and start the application.**
