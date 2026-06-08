import requests
import subprocess
import re
from typing import Optional

OLLAMA_HTTP_URL = "http://127.0.0.1:11434/completions?model=qwen2.5-coder:14b"

INTENT_SYSTEM_PROMPT = (
    "You are an intent classifier for a government service chatbot. "
    "Your job is to classify user queries into two categories: 'faq' or 'sql'. "
    "\n\nGuidelines:"
    "\n- 'faq': Questions asking for general information, procedures, processes, policies, eligibility, fees, documentation requirements, or how-to guidance. Examples: 'How do I apply?', 'What is Sewa Setu?', 'What documents do I need?'"
    "\n- 'sql': Queries asking for specific data retrieval, status checks, records, counts, or database lookups. Examples: 'Show pending applications', 'List all citizens', 'How many approved certificates?', 'Track application status'"
    "\n\nRespond with ONLY the word 'faq' or 'sql', nothing else. No explanation, no punctuation."
)


def build_intent_prompt(user_prompt: str) -> str:
    return f"{INTENT_SYSTEM_PROMPT}\n\nUser query: {user_prompt}\nClassification:"


def _generate_via_http(prompt_text: str) -> Optional[str]:
    try:
        payload = {"prompt": prompt_text, "max_tokens": 50, "temperature": 0}
        resp = requests.post(OLLAMA_HTTP_URL, json=payload, timeout=20)
        if resp.status_code != 200:
            return None
        data = resp.json()
        if isinstance(data, dict):
            if "completion" in data:
                return data["completion"].strip()
            if "choices" in data and isinstance(data["choices"], list) and data["choices"]:
                choice = data["choices"][0]
                if isinstance(choice, dict):
                    text = choice.get("text") or choice.get("message", {}).get("content")
                    if text:
                        return text.strip()
        return None
    except requests.RequestException:
        return None


def _strip_ansi(text: str) -> str:
    ansi_re = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    cleaned = ansi_re.sub("", text)
    return ''.join(ch for ch in cleaned if ord(ch) >= 32 or ch in '\n\r\t')


def _generate_via_cli(model: str, prompt_text: str) -> str:
    cmd = ["ollama", "run", model, prompt_text]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    if proc.returncode != 0:
        err = proc.stderr.decode('utf-8', errors='ignore').strip()
        raise RuntimeError(err or "Ollama CLI failed")
    stdout_text = proc.stdout.decode('utf-8', errors='ignore').strip()
    return _strip_ansi(stdout_text)


def _clean_classification(text: str) -> str:
    """Clean and extract classification from model output."""
    if not text:
        return "faq"  # Default to FAQ
    
    text = _strip_ansi(text).lower().strip()
    
    # Extract the first word that matches our classification
    words = text.split()
    for word in words:
        if word in ["faq", "sql"]:
            return word
    
    # Default to FAQ if no clear classification
    return "faq"


def classify_intent_ai(user_prompt: str) -> str:
    """
    Classify user prompt using AI (Ollama) as 'faq' or 'sql'.
    Falls back to 'faq' if classification fails.
    """
    if not user_prompt.strip():
        return "faq"
    
    prompt_text = build_intent_prompt(user_prompt)
    
    # First try HTTP endpoint
    http_result = _generate_via_http(prompt_text)
    if http_result:
        classification = _clean_classification(http_result)
        return classification
    
    # Fallback to CLI
    try:
        cli_result = _generate_via_cli("qwen2.5-coder:14b", prompt_text)
        classification = _clean_classification(cli_result)
        return classification
    except Exception:
        # If everything fails, default to FAQ
        return "faq"
