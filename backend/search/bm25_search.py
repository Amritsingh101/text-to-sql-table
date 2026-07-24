import numpy as np
from indexing.bm25 import bm25
from matadata import table_names, tokenize


def bm25_search(query, top_k=8):
    query_tokens = tokenize(query)
    scores = bm25.get_scores(query_tokens)
    ranked = np.argsort(scores)[::-1]
    results = []
    for rank, idx in enumerate(ranked[:top_k], start=1):
        if scores[idx] <= 0:
            continue
        results.append({
            "table": table_names[idx],
            "rank": rank,
            "score": float(scores[idx]),
            "idx": int(idx)
        })
    return results