from collections import defaultdict
from search.bm25_search import bm25_search
from search.embedding_search import embedding_search


def reciprocal_rank_fusion(
    bm25_results,
    embedding_results,
    embedding_weight=0.8,
    bm25_weight=0.2,
    k=60
):
    fused_scores = defaultdict(float)
    for result in bm25_results:
        fused_scores[result["idx"]] += (
            bm25_weight * (1 / (k + result["rank"] ** 2))
        )
    for result in embedding_results:
        fused_scores[result["idx"]] += (
            embedding_weight * (1 / (k + result["rank"] ** 2))
        )
    ranked = sorted(
        fused_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )
    return ranked


def hybrid_search(query, embedding_weight=0.8, bm25_weight=0.2, top_k=7):
    bm25_results = bm25_search(query, top_k=15)
    embedding_results = embedding_search(query, top_k=15)
    fused = reciprocal_rank_fusion(
        bm25_results,
        embedding_results,
        embedding_weight,
        bm25_weight
    )
    return fused[:top_k]