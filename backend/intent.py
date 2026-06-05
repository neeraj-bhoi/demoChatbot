import re


SQL_INDICATORS = [
    "show",
    "list",
    "find",
    "count",
    "total",
    "records",
    "applications",
    "citizen",
    "certificate",
    "issued",
    "status",
    "arn",
    "aadhar",
    "aadhaar",
    "report",
    "pending",
    "approved",
    "rejected",
    "today",
    "number",
    "track",
]
FAQ_INDICATORS = [
    "how",
    "what",
    "why",
    "when",
    "where",
    "which",
    "document",
    "process",
    "apply",
    "procedure",
    "help",
    "contact",
    "support",
    "policy",
    "eligibility",
    "fee",
    "service",
    "website",
    "portal",
    "need",
    "required",
    "guide",
    "steps",
    "instructions",
]


def detect_language(text: str) -> str:
    if re.search(r"[\u0900-\u097F]", text):
        return "Hindi"
    return "English"


def classify_intent(text: str) -> str:
    content = text.lower()
    if not content.strip():
        return "faq"

    has_sql = any(re.search(rf"\b{re.escape(word)}\b", content) for word in SQL_INDICATORS)
    has_faq = any(re.search(rf"\b{re.escape(word)}\b", content) for word in FAQ_INDICATORS)

    # If the user explicitly asks for data, records, lists, counts, or certificates, prefer SQL
    if has_sql and not has_faq:
        return "sql"

    # If the user asks a question that appears informational, prefer FAQ
    if has_faq and not has_sql:
        return "faq"

    # If both appear, use stronger SQL signals for data queries
    if has_sql and has_faq:
        if re.search(r"\b(show|list|find|count|records|applications|pending|approved|rejected|today)\b", content):
            return "sql"
        return "faq"

    # Default to FAQ for question-like prompts, else SQL
    if content.startswith(("what", "how", "why", "when", "where", "which", "can", "is", "are")):
        return "faq"

    return "faq"
