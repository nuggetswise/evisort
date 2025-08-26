from __future__ import annotations
from typing import List, Dict, Tuple, Optional
import re

class Agent:
    def __init__(self, llm_client):
        """Initialize agent with LLM client for contract analysis."""
        self.llm = llm_client

    # --- Intent classification ---
    def classify(self, query: str) -> str:
        """Classify the intent of the user query."""
        q = query.lower()
        if any(k in q for k in ["improve", "rewrite", "redline", "safer clause", "propose", "better"]):
            return "redline"
        if any(k in q for k in ["extract", "pull", "list", "show fields", "tracker", "find"]):
            return "extract"
        return "qa"

    # --- Planning based on intent ---
    def plan(self, query: str) -> List[str]:
        """Returns the step sequence based on intent."""
        intent = self.classify(query)
        
        if intent == "qa":
            return ["classify", "retrieve", "synthesize"]
        elif intent == "extract":
            return ["classify", "retrieve", "extract"]  # placeholder for future structured extractors
        elif intent == "redline":
            return ["classify", "retrieve", "synthesize", "propose"]
        else:
            return ["classify", "retrieve", "synthesize"]

    # --- Answer synthesis ---
    def answer(self, query: str, clauses: List[str], file_map: List[Tuple[str, int, int]] = None) -> str:
        """Compose a grounded answer using the provided clauses."""
        if not clauses:
            return "No relevant clauses found to answer this question."
        
        # If we have file mapping information, use it to provide contract context
        if file_map:
            context_parts = []
            for i, clause in enumerate(clauses):
                # Find which contract this clause belongs to
                contract_name = "Unknown Contract"
                for contract_name, start_idx, end_idx in file_map:
                    if start_idx <= i < end_idx:
                        contract_name = contract_name
                        break
                
                context_parts.append(f"[{i+1}] ({contract_name}) {clause}")
            
            context = "\n\n".join(context_parts)
            prompt = (
                "You are a senior contract analyst analyzing multiple contracts. Answer the user question using ONLY the provided clauses. "
                "Be concise (2–4 sentences) and include short references like [1], [2] when you rely on a clause. "
                "When referencing clauses, mention which contract they come from.\n\n"
                f"Question: {query}\n\nClauses:\n{context}\n"
            )
        else:
            context = "\n\n".join([f"[{i+1}] {c}" for i, c in enumerate(clauses)])
            prompt = (
                "You are a senior contract analyst. Answer the user question using ONLY the provided clauses. "
                "Be concise (2–4 sentences) and include short references like [1], [2] when you rely on a clause.\n\n"
                f"Question: {query}\n\nClauses:\n{context}\n"
            )
        
        return self._call_llm(prompt)

    # --- Main orchestration method ---
    def run(self, query: str, clauses: List[str], top_k: int = 5, file_map: List[Tuple[str, int, int]] = None) -> Dict[str, Any]:
        """
        Orchestrate the complete agentic pipeline:
        1. classify → plan
        2. retrieve top-k clauses (BM25/keyword fallback)
        3. synthesize an answer grounded in those clauses
        4. optionally propose a safer clause
        5. returns a structured dict: intent, steps, citations (with index/score/text), answer, proposal
        """
        # Step 1: Classify intent and plan
        intent = self.classify(query)
        steps = self.plan(query)
        
        # Step 2: Retrieve relevant clauses
        try:
            idx, toks = build_bm25_index(clauses)
            ranked = retrieve(query, clauses, idx, toks, k=top_k)
            retrieved_clauses = [clauses[i] for i, _ in ranked] if ranked else []
            citations = []
            for i, score in ranked:
                snippet = clauses[i][:400] + ("..." if len(clauses[i]) > 400 else "")
                citations.append({
                    "index": i,
                    "score": float(score),
                    "text": snippet
                })
        except Exception as e:
            # Fallback to simple keyword matching
            ranked = self._keyword_fallback(query, clauses, top_k)
            retrieved_clauses = [clauses[i] for i, _ in ranked] if ranked else []
            citations = []
            for i, score in ranked:
                snippet = clauses[i][:400] + ("..." if len(clauses[i]) > 400 else "")
                citations.append({
                    "index": i,
                    "score": score,
                    "text": snippet
                })
        
        # Step 3: Generate grounded answer
        answer = self.answer(query, retrieved_clauses, file_map)
        
        # Step 4: Optionally propose safer clause
        proposal = None
        if intent == "redline" or any(k in query.lower() for k in ["liability", "indemn", "renewal", "notice", "risk"]):
            try:
                proposal = propose_redline(retrieved_clauses, self.llm)
            except Exception as e:
                proposal = f"Error generating safer clause: {e}"
        
        return {
            "intent": intent,
            "steps": steps,
            "citations": citations,
            "answer": answer,
            "proposal": proposal
        }

    def _keyword_fallback(self, query: str, clauses: List[str], top_k: int) -> List[Tuple[int, float]]:
        """Simple keyword fallback when BM25 is not available."""
        query_words = set(query.lower().split())
        scored_clauses = []
        
        for i, clause in enumerate(clauses):
            clause_words = set(clause.lower().split())
            score = len(query_words.intersection(clause_words))
            if score > 0:
                scored_clauses.append((i, float(score)))
        
        # Sort by score and return top_k with indices
        scored_clauses.sort(key=lambda x: x[1], reverse=True)
        return scored_clauses[:top_k]

    # --- internal ---
    def _call_llm(self, prompt: str) -> str:
        """Call LLM with proper error handling."""
        try:
            # Use the generate_response method from our LLMClient
            return self.llm.generate_response(prompt)
        except Exception as e:
            raise Exception(f"LLM error: {e}")


try:
    from rank_bm25 import BM25Okapi
except Exception:
    BM25Okapi = None



_split = re.compile(r"\n{2,}|\n\s*(SECTION\s+\d+\.|ARTICLE\s+\d+\.|\d+\.\d+\.|\d+\.)\s+", re.IGNORECASE)

def split_into_clauses(text: str) -> List[str]:
    if not text:
        return []
    t = text.replace("\r", "")
    parts = _split.split(t)
    if len(parts) <= 1:
        parts = re.split(r"\n{2,}", t)
    return [p.strip() for p in parts if p and p.strip()]


def build_bm25_index(clauses: List[str]):
    if not clauses:
        return None, []
    if BM25Okapi is None:
        raise Exception("BM25 retrieval not available. Please install rank_bm25: pip install rank_bm25")
    tokenized = [c.lower().split() for c in clauses]
    return BM25Okapi(tokenized), tokenized


def retrieve(query: str, clauses: List[str], index_obj, tokenized, k: int = 5) -> List[Tuple[int, float]]:
    if not clauses:
        return []
    q = query.lower().split()
    if BM25Okapi is not None and index_obj is not None:
        scores = index_obj.get_scores(q)
        ranked = sorted(list(enumerate(scores)), key=lambda x: x[1], reverse=True)
        return ranked[:k]
    else:
        # Require BM25 for proper retrieval
        raise Exception("BM25 retrieval not available. Please install rank_bm25: pip install rank_bm25")


def propose_redline(clauses: List[str], llm_client) -> str:
    """Generate safer clause suggestions using AI."""
    context = "\n\n".join([f"[{i+1}] {c}" for i, c in enumerate(clauses)])
    prompt = (
        "You are a senior contract attorney. Analyze the provided clauses and suggest a safer, "
        "more protective version. Focus on limiting liability, adding protections, and improving clarity. "
        "Provide a complete, professional clause that addresses the key risks identified.\n\n"
        f"Original clauses:\n{context}\n\n"
        "Suggested safer clause:"
    )
    try:
        return llm_client.generate_response(prompt)
    except Exception as e:
        raise Exception(f"Error generating safer clause: {e}")
