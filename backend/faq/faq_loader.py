import re
from pathlib import Path
from typing import Dict, List


def _parse_faq_text(raw_text: str, language: str) -> List[Dict]:
    sections = []
    
    # Split by numbered question pattern like **1. Question**
    # Match pattern: **NUMBER. Question Text**
    lines = raw_text.split('\n')
    current_question = None
    current_answer = []
    
    for line in lines:
        # Check if this line starts a new question (pattern: **1. Text**)
        match = re.match(r'^\s*\*\*\d+\.\s+(.*?)\*\*\s*$', line)
        if match:
            # If we have a previous question, save it
            if current_question is not None:
                answer_text = '\n'.join(current_answer).strip()
                # Remove markdown and clean up
                answer_text = re.sub(r'\*\*', '', answer_text)
                answer_text = answer_text.strip()
                
                sections.append(
                    {
                        "id": f"{language}-{len(sections) + 1}",
                        "language": language,
                        "question": current_question,
                        "answer": answer_text,
                        "text": f"Q: {current_question}\nA: {answer_text}",
                        "source": "FAQ Knowledge Base",
                    }
                )
            
            # Start a new question
            current_question = match.group(1).strip()
            current_answer = []
        elif current_question is not None:
            # This is part of the answer for current question
            if line.strip():  # Only add non-empty lines
                current_answer.append(line)
    
    # Don't forget the last question
    if current_question is not None:
        answer_text = '\n'.join(current_answer).strip()
        # Remove markdown and clean up
        answer_text = re.sub(r'\*\*', '', answer_text)
        answer_text = answer_text.strip()
        
        sections.append(
            {
                "id": f"{language}-{len(sections) + 1}",
                "language": language,
                "question": current_question,
                "answer": answer_text,
                "text": f"Q: {current_question}\nA: {answer_text}",
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
