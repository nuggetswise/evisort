## 🧠 Agentic AI Feature (Most Value)

**What to implement:**
**Ask AI Across All Contracts (Agentic Q&A + Auto‑Redline)** – a single tab that answers natural‑language questions over the entire uploaded corpus, cites source clauses, and can propose safer language. Under the hood, an agent performs multi‑step reasoning:

1) **Intent & scope** → determine if the user wants Q&A, extraction, or a redline suggestion
2) **Retrieve** → rank relevant clauses across all files (BM25 now; swap to embeddings later)
3) **Analyze** → run rule/regex extractors + (optional) LLM to explain the answer with citations
4) **Propose** → if risk detected, suggest a safer clause from a governed template
5) **Assemble** → return a concise answer + top citations + one‑click insert/ export

This aligns with Workday/Evisort value props and is the highest‑leverage addition to the demo.

### Quick Enable (Demo‑mode, offline‑friendly)
Add the **Ask AI** tab without external LLMs:

- Retrieval: `rank_bm25` over clause chunks stored in memory
- Analysis: regex/rule extractors already in the repo
- Proposal: template library (e.g., limitation of liability, renewal, notice)

### Optional: Enable LLMs
Add these to `requirements.txt` as needed:

```txt
rank-bm25>=0.2.2
faiss-cpu>=1.8.0.post1    # optional for vector search
openai>=1.40.0            # optional LLM
cohere>=5.5.8             # optional LLM
```

Set env flags:
```bash
export AGENT_ENABLED=true
export RAG_ENABLED=true           # enable corpus Q&A
export EMBEDDINGS_PROVIDER=none   # or 'openai' | 'cohere'
export OPENAI_API_KEY=...
export COHERE_API_KEY=...
```

### Local Development Steps
```bash
# 1) Install extras (if you want FAISS or an LLM)
pip install rank-bm25 faiss-cpu openai cohere

# 2) Build a tiny index (demo)
python scripts/build_index.py  # reads ./sample_data/* and writes ./cache/index.pkl

# 3) Run the app
streamlit run app.py
```

### Streamlit Cloud Notes
- Add the same env vars in **Secrets**
- If using FAISS, prefer CPU wheel; or fall back to BM25 only
- Keep index small; rebuild at startup if needed

### Docker Notes
Add these lines to the Dockerfile if enabling RAG/LLM:

```dockerfile
# Optional extras
RUN pip install --no-cache-dir rank-bm25 faiss-cpu openai cohere
ENV AGENT_ENABLED=true RAG_ENABLED=true EMBEDDINGS_PROVIDER=none
```

### Minimal App Wiring (pseudocode)
```python
# tabs/ask_ai.py
query = st.text_input("Ask AI about your contracts…")
if query:
    intents = agent.classify(query)
    hits = retriever.search(query, top_k=5)        # BM25 now
    analysis = analyzer.explain(hits)              # regex/rules
    proposal = suggester.maybe_propose(analysis)   # template clause
    ui.render_answer(analysis, hits, proposal)     # citations & redline button
```

### Acceptance Criteria & Metrics
- p95 Q&A latency < **2s** on 100–500 documents (BM25)
- ≥ **90% precision** for targeted trackers (renewal, notice days, liability cap)
- **Redline acceptance rate** tracked via UI feedback

### Security & Privacy
- Demo runs offline by default (no keys required)
- When LLMs are enabled, use env‑vars/Secrets; never commit keys

**Optional packages for Agentic AI**

```dockerfile
# (Optional) install retrieval/LLM libs
RUN pip install --no-cache-dir rank-bm25 faiss-cpu openai cohere
ENV AGENT_ENABLED=true RAG_ENABLED=true EMBEDDINGS_PROVIDER=none
```
- `AGENT_ENABLED`: Toggle the Ask AI agent (true/false)
- `RAG_ENABLED`: Enable corpus Q&A over uploaded files
- `EMBEDDINGS_PROVIDER`: none | openai | cohere

**Note**: This app is designed for demonstration purposes. For production use, implement appropriate security measures and monitoring.