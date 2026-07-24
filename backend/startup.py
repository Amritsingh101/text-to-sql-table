import logging
import pickle
from pathlib import Path

logger = logging.getLogger(__name__)

_SCHEMA_PATH = Path(__file__).parent / "schema" / "schema.json"
if not _SCHEMA_PATH.exists():
    _SCHEMA_PATH = Path(__file__).parent.parent / "schema" / "schema.json"

_DATA_DIR = Path(__file__).parent / "data"   

_METADATA_FILES = [
    _DATA_DIR / "table_names.pkl",
    _DATA_DIR / "documents.pkl",
    _DATA_DIR / "tokenized_docs.pkl",
]
_FAISS_FILE = _DATA_DIR / "embedding_index.faiss"


def initialize():
    _DATA_DIR.mkdir(parents=True, exist_ok=True)


    # matadata.py                  
  
    if not all(p.exists() for p in _METADATA_FILES):
        logger.info("Metadata pickles not found - building from schema …")
        import matadata  # builds table_names, documents, tokenized_documents at import

        with open(_DATA_DIR / "table_names.pkl", "wb") as f:
            pickle.dump(matadata.table_names, f)
        with open(_DATA_DIR / "documents.pkl", "wb") as f:
            pickle.dump(matadata.documents, f)
        with open(_DATA_DIR / "tokenized_docs.pkl", "wb") as f:
            pickle.dump(matadata.tokenized_documents, f)

        logger.info("Metadata pickles saved (%d tables).", len(matadata.table_names))
    else:
        logger.info("Metadata pickles already exist – skipping build.")

    # indexing/bm25.py                    
    
    logger.info("Loading BM25 index …")
    import indexing.bm25 
    logger.info("BM25 ready.")

   
    # indexing/embedding.py      
    # Only runs when the index file is missing 
    if not _FAISS_FILE.exists():
        logger.info("FAISS index not found - encoding documents (this may take a while) …")
        import indexing.embedding
        logger.info("FAISS index saved.")
    else:
        logger.info("FAISS index already exists - skipping encoding.")

    #indexing/cross_encoder.py

    logger.info("Loading CrossEncoder model …")
    import indexing.cross_encoder 
    logger.info("CrossEncoder ready.")

    # Pre-load all search modules 
    logger.info("Loading search modules …")
    import search.bm25_search 
    import search.embedding_search 
    import search.reranker 
    logger.info("All models loaded - ready to serve.")
