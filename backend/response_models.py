from pydantic import BaseModel
from typing import Any, Dict, List, Literal


class ChatRequest(BaseModel):
    prompt: str


class FAQResponse(BaseModel):
    response_type: Literal["faq"]
    answer: str
    sources: List[str]


class SQLResponse(BaseModel):
    response_type: Literal["sql"]
    generated_sql: str
    columns: List[str]
    rows: List[Dict[str, Any]]


class QueryRequest(BaseModel):
    prompt: str


class QueryResponse(BaseModel):
    sql: str
    raw_response: str
    results: List[Dict[str, Any]]
