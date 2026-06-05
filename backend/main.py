from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import execute_query
from intent import classify_intent
from faq.faq_service import answer_faq
from ollama_service import generate_sql

app = FastAPI(title="E-District Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

SCHEMA_TEXT = """
Database schema for an E-District system with citizen records, certificate applications, and issued certificates.

Table citizens:
- id INT PRIMARY KEY AUTO_INCREMENT: unique citizen identifier
- full_name VARCHAR(200): citizen full legal name
- date_of_birth DATE: birth date for the citizen
- address VARCHAR(300): residential street address
- phone VARCHAR(50): contact phone number
- district VARCHAR(100): district or zone where the citizen resides

Table certificate_applications:
- id INT PRIMARY KEY AUTO_INCREMENT: unique application record ID
- citizen_id INT: foreign key referencing citizens(id), linking the application to a citizen
- certificate_type VARCHAR(100): certificate type such as 'Income', 'Residence', 'Birth', or 'Domicile'
- status VARCHAR(100): application status values like 'Pending', 'Approved', 'Rejected', or 'Cancelled'
- applied_at DATETIME: timestamp when the citizen submitted the application
- approved_at DATETIME: timestamp when the application was approved, null if not approved yet

Table issued_certificates:
- id INT PRIMARY KEY AUTO_INCREMENT: unique issued certificate ID
- application_id INT: foreign key referencing certificate_applications(id)
- issue_date DATE: date the certificate was issued
- expiration_date DATE: date when the certificate expires, if applicable
- details VARCHAR(400): additional notes or details about the issued certificate
"""


class ChatRequest(BaseModel):
    prompt: str


@app.post("/api/chat")
def handle_chat(request: ChatRequest):
    prompt = request.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")

    intent = classify_intent(prompt)
    if intent == "faq":
        try:
            answer, sources = answer_faq(prompt)
            return {"response_type": "faq", "answer": answer, "sources": sources}
        except Exception as exc:
            raise HTTPException(status_code=500, detail={"error": str(exc)})

    generated_sql = ''
    raw_response = ''
    try:
        generated_sql, raw_response = generate_sql(prompt, SCHEMA_TEXT)
        if not generated_sql.strip():
            raise RuntimeError("Generated SQL is empty")
        rows = execute_query(generated_sql)
        columns = list(rows[0].keys()) if rows else []
        return {
            "response_type": "sql",
            "generated_sql": generated_sql,
            "columns": columns,
            "rows": rows,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={"error": str(exc), "raw_response": raw_response, "sql": generated_sql},
        )


class QueryRequest(BaseModel):
    prompt: str


class QueryResponse(BaseModel):
    sql: str
    raw_response: str
    results: list[dict]


@app.post("/api/query", response_model=QueryResponse)
def handle_query(request: QueryRequest):
    generated_sql = ''
    raw_response = ''
    try:
        generated_sql, raw_response = generate_sql(request.prompt, SCHEMA_TEXT)
        if not generated_sql.strip():
            raise RuntimeError("Generated SQL is empty")
        results = execute_query(generated_sql)
        return {"sql": generated_sql, "raw_response": raw_response, "results": results}
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={"error": str(exc), "raw_response": raw_response, "sql": generated_sql},
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)