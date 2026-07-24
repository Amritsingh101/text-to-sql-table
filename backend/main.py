import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import startup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Build all indexes and load all models before serving requests."""
    startup.initialize()
    yield


from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(
    title="Text-to-SQL Table Finder",
    description="Given a natural language query, returns the most relevant table names for SQL generation.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static frontend directory if present
_FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
if _FRONTEND_DIR.exists():
    app.mount("/app", StaticFiles(directory=str(_FRONTEND_DIR), html=True), name="frontend")


class QueryRequest(BaseModel):
    query: str
    top_k: int = 7


class TableResult(BaseModel):
    table: str
    score: float


class SearchResponse(BaseModel):
    query: str
    tables: list[TableResult]


@app.get("/")
def root():
    return {"message": "Text-to-SQL Table Finder is running. POST to /search"}


@app.post("/search", response_model=SearchResponse)
def search_tables(request: QueryRequest):
   
    from search.reranker import rerank

    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    results = rerank(request.query, top_k=request.top_k)
    return SearchResponse(
        query=request.query,
        tables=[TableResult(**r) for r in results]
    )