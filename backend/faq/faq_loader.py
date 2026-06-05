import re
from pathlib import Path
from typing import Dict, List


def _parse_faq_text(raw_text: str, language: str) -> List[Dict]:
    sections = []
    pattern = re.compile(r"\*\*\d+\.\s*(.*?)\*\*[\s\S]*?(?=(?:\n\*\*\d+\.|\Z))", re.MULTILINE)
    matches = re.finditer(pattern, raw_text)
    for idx, match in enumerate(matches, start=1):
        header = match.group(1).strip()
        # split header into question and answer if answer follows on same line
        if header.endswith('?'):
            question = header
            answer_text = raw_text[match.end():].split('\n**', 1)[0].strip()
        else:
            question = header
            answer_text = raw_text[match.end():].split('\n**', 1)[0].strip()
        # clean answer by stripping trailing numbering or markdown
        answer = re.sub(r"\*\*\d+\.$", "", answer_text).strip()
        sections.append(
            {
                "id": f"{language}-{idx}",
                "language": language,
                "question": question,
                "answer": answer,
                "text": f"Q: {question}\nA: {answer}",
                "source": "FAQ Knowledge Base",
            }
        )
    return sections


def load_faq_documents() -> List[Dict]:
    faq_dir = Path(__file__).resolve().parent / "knowledge"
    english_path = faq_dir / "english_faq.txt"
    hindi_path = faq_dir / "hindi_faq.txt"

    documents: List[Dict] = []

    if english_path.exists():
        raw_english = english_path.read_text(encoding="utf-8")
        documents.extend(_parse_faq_text(raw_english, "English"))
    else:
        raise FileNotFoundError(f"English FAQ file not found: {english_path}")

    if hindi_path.exists():
        raw_hindi = hindi_path.read_text(encoding="utf-8")
        documents.extend(_parse_faq_text(raw_hindi, "Hindi"))
    else:
        raise FileNotFoundError(f"Hindi FAQ file not found: {hindi_path}")

    return documents
