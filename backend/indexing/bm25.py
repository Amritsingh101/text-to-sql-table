from rank_bm25 import BM25Okapi
import pickle
from pathlib import Path

_DATA_DIR = Path(__file__).parent.parent / "data"

with open(_DATA_DIR / "tokenized_docs.pkl", "rb") as f:
    tokenized_documents = pickle.load(f)

bm25 = BM25Okapi(tokenized_documents)

# Persist if run as a script
if __name__ == "__main__":
    with open(_DATA_DIR / "bm25.pkl", "wb") as f:
        pickle.dump(bm25, f)
    print("BM25 index saved.")