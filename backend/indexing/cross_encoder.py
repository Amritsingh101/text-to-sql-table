from sentence_transformers import CrossEncoder
import pickle
from pathlib import Path

_DATA_DIR = Path(__file__).parent.parent / "data"
_MODEL_DIR = _DATA_DIR / "models" / "ms-marco-MiniLM-L6-v2"

# Load from local directory if available (offline), else download and save
if _MODEL_DIR.exists():
    reranker = CrossEncoder(str(_MODEL_DIR))
else:
    reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")
    _MODEL_DIR.mkdir(parents=True, exist_ok=True)
    reranker.save(str(_MODEL_DIR))
    print(f"CrossEncoder saved to {_MODEL_DIR}")

if __name__ == "__main__":
    with open(_DATA_DIR / "reranker.pkl", "wb") as f:
        pickle.dump(reranker, f)
    print("CrossEncoder pickled.")