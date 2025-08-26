from __future__ import annotations
from typing import List, Dict, Tuple, Optional
import re

# Minimal agent: classify → answer (LLM‑first)

INTENTS = ("qa", "extract", "redline")

class Agent:
    def __init__(self, llm_client):
        """llm_client must expose one of: complete(), chat(), generate(), invoke() returning str."""
        self.llm = llm_client

    # --- Intent classification (heuristic) ---
    def classify(self, query: str) -> str:
        q = query.lower()
        if any(k in q for k in ["improve", "rewrite", "redline", "safer clause", "propose"]):
            return "redline"
        if any(k in q for k in ["extract", "pull", "list", "show fields", "tracker"]):
            return "extract"
        return "qa"

    # --- Answer synthesis ---
    def answer(self, query: str, clauses: List[str]) -> Dict[str, str]:
        """Compose a grounded answer using the provided clauses.
        Returns dict with keys: 'answer', 'prompt'.
        """
        context = "\n\n".join([f"[{i+1}] {c}" for i, c in enumerate(clauses)])
        prompt = (
            "You are a senior contract analyst. Answer the user question using ONLY the provided clauses. "
            "Be concise (2–4 sentences) and include short references like [1], [2] when you rely on a clause.\n\n"
            f"Question: {query}\n\nClauses:\n{context}\n"
        )
        answer = self._call_llm(prompt)
        return {"answer": answer, "prompt": prompt}

    # --- internal ---
    def _call_llm(self, prompt: str) -> str:
        try:
            if hasattr(self.llm, "complete"):
                return self.llm.complete(prompt)
            if hasattr(self.llm, "chat"):
                return self.llm.chat(prompt)
            if hasattr(self.llm, "generate"):
                return self.llm.generate(prompt)
            if hasattr(self.llm, "invoke"):
                return self.llm.invoke(prompt)
        except Exception as e:
            return f"LLM error: {e}"
        return "(No LLM client available)"


try:
    from rank_bm25 import BM25Okapi
except Exception:
    BM25Okapi = None

try:
    from rank_bm25 import BM25Okapi
except Exception:
    BM25Okapi = None

SAFE_TEMPLATES: Dict[str, str] = {
    "liability": (
        "Limitation of Liability. Except for gross negligence, willful misconduct, or IP infringement, "
        "each party's aggregate liability arising out of or related to this Agreement shall not exceed "
        "the fees paid or payable by Customer in the twelve (12) months preceding the claim."
    ),
    "renewal": (
        "Renewal; Opt-Out. This Agreement renews for successive one-year terms unless either party provides "
        "written notice of non-renewal at least thirty (30) days prior to the end of the then-current term."
    ),
    "notice": (
        "Termination for Convenience. Either party may terminate this Agreement upon thirty (30) days' prior "
        "written notice to the other party."
    ),
    "indemn": (
        "Mutual Indemnification. Each party shall indemnify, defend, and hold the other party harmless from third-"
        "party claims arising from such indemnifying party's breach of this Agreement, gross negligence, or willful misconduct."
    ),
}

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
    tokenized = [c.lower().split() for c in clauses]
    if BM25Okapi is None:
        return None, tokenized
    return BM25Okapi(tokenized), tokenized


def retrieve(query: str, clauses: List[str], index_obj, tokenized, k: int = 5) -> List[Tuple[int, float]]:
    if not clauses:
        return []
    q = query.lower().split()
    if BM25Okapi is not None and index_obj is not None:
        scores = index_obj.get_scores(q)
        ranked = sorted(list(enumerate(scores)), key=lambda x: x[1], reverse=True)
        return ranked[:k]
    # fallback: simple keyword overlap score
    def score(c: str) -> float:
        cset = set(c.lower().split())
        return sum(1 for w in q if w in cset)
    ranked = sorted([(i, score(c)) for i, c in enumerate(clauses)], key=lambda x: x[1], reverse=True)
    return [r for r in ranked[:k] if r[1] > 0]


def propose_redline(clauses: List[str]) -> str:
    joined = " \n".join(clauses).lower()
    for key in ["liability", "indemn", "renewal", "notice"]:
        if key in joined:
            return SAFE_TEMPLATES[key]
    return SAFE_TEMPLATES["liability"]
