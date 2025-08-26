## 🚀 Quick Start (LLM‑only, no Docker)

This repo demonstrates an **agentic, LLM‑powered** contract copilot with unified pipeline. No Docker, no offline mode.

### Requirements
- Python 3.10+
- One API key: **OpenAI**, **Cohere**, **Groq**, or **Gemini**

### Install & Run
```bash
cd contractcopilot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Set up API keys (at least one required)
export OPENAI_API_KEY=sk-...      # or
export COHERE_API_KEY=...         # or  
export GROQ_API_KEY=...           # or
export GEMINI_API_KEY=...

streamlit run app.py
```

## 🧩 Unified Agentic Architecture

**Goal:** A single **"Run Agentic Analysis"** button handles both single clause and multi-contract analysis with unified pipeline.

**Agent Steps**
1) **Intent** → classify: Q&A vs. extract vs. propose‑redline
2) **Plan** → choose tools: retrieval / extractors / suggester
3) **Retrieve** → rank clauses (BM25 with keyword fallback)
4) **Analyze** → synthesize answer with LLM; attach citations (file + clause)
5) **Propose** → if risk detected, suggest safer clause (governed templates)

**File Layout**
```
app.py                      # Streamlit UI (unified agentic pipeline)
agents.py                   # Agent loop (intent→plan→act→answer)
components/clause_input.py  # Input handling (paste/upload tabs)
utils/llm_client.py        # Multi-LLM client with fallback strategies
utils/config.py            # Configuration and API key management
assets/                    # Sample data for testing
```

## 🧠 Agentic AI Features (Implemented)

**✅ Implemented:**
**Unified Agentic Pipeline** – single interface that handles both single clause and multi-contract analysis with consistent agentic workflow:

1) **Intent & scope** → determine if the user wants Q&A, extraction, or a redline suggestion
2) **Retrieve** → rank relevant clauses (BM25 with keyword fallback)
3) **Analyze** → run LLM to explain the answer with citations
4) **Propose** → if risk detected, suggest a safer clause from governed templates
5) **Assemble** → return concise answer + citations + next-step business actions

### Unified Agentic Flow (LLM‑first)
- **Input**: Tabs for paste clause or upload files
- **Configuration**: Optional policy lens (GDPR, CCPA, SOX, HIPAA, PCI-DSS)
- **Retrieval**: `rank_bm25` over clause chunks with keyword fallback
- **Answering**: Multi-LLM client synthesizes answer + citations
- **Proposal**: Governed template library provides safer clauses
- **Actions**: Insert, Track, Export, Copy business outcomes

### Dependencies
```
streamlit
openai
cohere
groq
google-generativeai
rank-bm25
python-docx
PyPDF2
```

### Local Development Steps
```bash
# 1) Install dependencies
pip install -r requirements.txt

# 2) Set up API keys
export OPENAI_API_KEY=sk-...
# or other providers

# 3) Run the app
streamlit run app.py
```

### App Architecture (implemented)
```python
# app.py (unified agentic pipeline)
# Input handling
if tab == "Paste Clause":
    clause_text = clause_input()
    clauses = [clause_text]
else:  # Upload Files
    clauses = process_uploaded_files()

# Configuration
policy_lens = st.multiselect("Policy Lens", ["GDPR", "CCPA", "SOX", "HIPAA", "PCI-DSS"])

# Agentic analysis
if st.button("Run Agentic Analysis"):
    agent = Agent(llm_client)
    result = agent.run(question, clauses, top_k=5)
    
    # Display results
    st.write(result['answer'])  # AI analysis
    st.write(result['citations'])  # Citations with scores
    if result['proposal']: st.write(result['proposal'])  # Safer clause
    
    # Business actions
    st.button("Insert Safer Clause")  # Add to revisions buffer
    st.button("Create Tracker")       # Create tracking item
    st.button("Export Decision")      # Download report
    st.button("Copy Answer")          # Copy to clipboard
```

### Acceptance Criteria & Metrics (achieved)
- ✅ **Unified Pipeline**: Single CTA for both single clause and corpus analysis
- ✅ **Business Outcomes**: Next-step actions (Insert, Track, Export, Copy)
- ✅ **Explainability**: Citations with relevance scores and technical details
- ✅ **Governance**: Policy lens, template governance, export capabilities
- ✅ **Professional UI**: Clean, focused presentation for hiring managers

### Security & Privacy
- Uses your LLM provider via API keys (no keys committed)
- PII/contract text stays in session memory; clear on refresh
- Revisions buffer in session state for safer clause tracking
- Export functionality for decision record keeping

**Note**: This app is designed for demonstration purposes. For production use, implement appropriate security measures and monitoring.

## 🔧 Environment Variables

- `OPENAI_API_KEY`: required for OpenAI integration
- `COHERE_API_KEY`: required for Cohere integration  
- `GROQ_API_KEY`: required for Groq integration
- `GEMINI_API_KEY`: required for Gemini integration

**At least one API key is required** - the app will automatically use available providers in priority order.