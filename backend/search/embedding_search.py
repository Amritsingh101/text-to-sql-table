import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

_DATA_DIR = Path(__file__).parent.parent / "data"

index = faiss.read_index(str(_DATA_DIR / "embedding_index.faiss"))

with open(_DATA_DIR / "table_names.pkl", "rb") as f:
    table_names = pickle.load(f)

_MODEL_DIR = _DATA_DIR / "models" / "bge-base-en-v1.5"

# Load from local directory if available (offline), else download and save
if _MODEL_DIR.exists():
    model = SentenceTransformer(str(_MODEL_DIR))
else:
    model = SentenceTransformer("BAAI/bge-base-en-v1.5")
    _MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model.save(str(_MODEL_DIR))


def embedding_search(query, top_k=8):
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
        convert_to_numpy=True
    )
    scores, indices = index.search(query_embedding, top_k)
    results = []
    for rank, (score, idx) in enumerate(
        zip(scores[0], indices[0]),
        start=1
    ):
        results.append({
            "table": table_names[idx],
            "rank": rank,
            "score": float(score),
            "idx": int(idx)
        })
    return results