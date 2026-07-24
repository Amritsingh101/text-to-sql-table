import pickle
from pathlib import Path
from search.rrf_search import hybrid_search
from indexing.cross_encoder import reranker  # reuse the already-loaded model

_DATA_DIR = Path(__file__).parent.parent / "data"

with open(_DATA_DIR / "table_names.pkl", "rb") as f:
    table_names = pickle.load(f)

with open(_DATA_DIR / "documents.pkl", "rb") as f:
    documents = pickle.load(f)


def rerank(query: str, top_k: int = 7) -> list[dict]:
    """
    Hybrid search (BM25 + embedding) followed by cross-encoder reranking.
    Returns a list of dicts with table name and score, best first.
    """
    # Step 1: hybrid retrieval - get candidate table indices
    hybrid_results = hybrid_search(
        query,
        embedding_weight=0.9,
        bm25_weight=0.1,
        top_k=15
    )
    candidate_indices = [idx for idx, _ in hybrid_results]

    if not candidate_indices:
        return []

    # Step 2: cross-encoder reranking
    pairs = [(query, documents[idx]) for idx in candidate_indices]
    scores = reranker.predict(pairs)

    reranked = sorted(
        zip(candidate_indices, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        {"table": table_names[idx], "score": float(score)}
        for idx, score in reranked[:top_k]
    ]