from sentence_transformers import SentenceTransformer
import pickle
import faiss
import numpy as np
from pathlib import Path

_DATA_DIR = Path(__file__).parent.parent / "data"
_MODEL_DIR = _DATA_DIR / "models" / "bge-base-en-v1.5"

with open(_DATA_DIR / "documents.pkl", "rb") as f:
    documents = pickle.load(f)

# Load from local directory if available (offline), else download and save
if _MODEL_DIR.exists():
    model = SentenceTransformer(str(_MODEL_DIR))
else:
    model = SentenceTransformer("BAAI/bge-base-en-v1.5")
    _MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model.save(str(_MODEL_DIR))
    print(f"SentenceTransformer saved to {_MODEL_DIR}")

embeddings = model.encode(
    documents,
    convert_to_numpy=True,
    show_progress_bar=True,
    normalize_embeddings=True
)

np.save(str(_DATA_DIR / "embeddings.npy"), embeddings)

dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

faiss.write_index(index, str(_DATA_DIR / "embedding_index.faiss"))
print("Embedding index saved.")