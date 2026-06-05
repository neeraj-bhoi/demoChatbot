import requests
import subprocess
import re
from typing import Optional

OLLAMA_HTTP_URL = "http://127.0.0.1:11434/completions?model=qwen2.5-coder:14b"

SYSTEM_PROMPT = (
    "You are an assistant that converts plain English questions into a single valid MySQL statement. "
    "Respond with exactly one SQL statement and nothing else. "
    "Do not add any explanation, commentary, or extra text before or after the SQL. "
    "Do not use backticks around identifiers. "
    "Do not include multiple statements or comments. "
    "Use only the provided schema and the user question to build the query."
)


def build_prompt(user_prompt: str, schema_text: str) -> str:
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Database schema:\n{schema_text}\n\n"
        f"Question: {user_prompt}\n"
        f"Query:"
    )


def _generate_via_http(prompt_text: str) -> Optional[str]:
    try:
        payload = {"prompt": prompt_text, "max_tokens": 200, "temperature": 0}
        resp = requests.post(OLLAMA_HTTP_URL, json=payload, timeout=20)
        if resp.status_code != 200:
            return None
        data = resp.json()
        # Ollama HTTP responses vary by version; try common keys
        if isinstance(data, dict):
            if "completion" in data:
                return data["completion"].strip()
            if "choices" in data and isinstance(data["choices"], list) and data["choices"]:
                # Try common shape
                choice = data["choices"][0]
                if isinstance(choice, dict):
                    # gpt style
                    text = choice.get("text") or choice.get("message", {}).get("content")
                    if text:
                        return text.strip()
        return None
    except requests.RequestException:
        return None


def _strip_ansi(text: str) -> str:
    # Remove ANSI escape sequences and control characters.
    ansi_re = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    cleaned = ansi_re.sub("", text)
    return ''.join(ch for ch in cleaned if ord(ch) >= 32 or ch in '\n\r\t')


def _strip_markdown(text: str) -> str:
    # Remove Markdown code fences and SQL block markers.
    text = re.sub(r"```(?:sql)?\n", "", text, flags=re.IGNORECASE)
    text = text.replace("```", "")
    return text


def _strip_sql_prefix(text: str) -> str:
    # Remove optional labels like 'SQL:' or 'Query:' at the beginning.
    return re.sub(r"(?i)^\s*(sql|query|answer)\s*[:\-]*\s*", "", text).strip()


def _generate_via_cli(model: str, prompt_text: str) -> str:
    # Use the Ollama CLI 'run' command which prints the model output to stdout.
    cmd = ["ollama", "run", model, prompt_text]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    if proc.returncode != 0:
        err = proc.stderr.decode('utf-8', errors='ignore').strip()
        raise RuntimeError(err or "Ollama CLI failed")
    stdout_text = proc.stdout.decode('utf-8', errors='ignore').strip()
    return _strip_ansi(stdout_text)


def _clean_sql_text(text: str) -> str:
    if not text:
        return ""
    text = _strip_ansi(text)
    text = _strip_markdown(text)
    text = _strip_sql_prefix(text)
    return text.strip()


def generate_sql(user_prompt: str, schema_text: str) -> tuple[str, str]:
    prompt_text = build_prompt(user_prompt, schema_text)

    # First try HTTP endpoint
    http_result = _generate_via_http(prompt_text)
    if http_result:
        cleaned_sql = _clean_sql_text(http_result)
        return cleaned_sql, http_result

    # Fallback to CLI. Model name should be provided as '<name>:<size>' like 'qwen2.5-coder:14b'
    try:
        cli_result = _generate_via_cli("qwen2.5-coder:14b", prompt_text)
        cleaned_sql = _clean_sql_text(cli_result)
        return cleaned_sql, cli_result
    except subprocess.SubprocessError as exc:
        raise RuntimeError(f"Ollama CLI error: {exc}")
