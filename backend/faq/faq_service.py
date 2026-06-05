from typing import List, Tuple

from .faq_store import faq_store
from intent import detect_language


FAQ_SCORE_THRESHOLD = 0.55


def answer_faq(prompt: str) -> Tuple[str, List[str]]:
    language = detect_language(prompt)
    candidates = faq_store.query(prompt, language, top_k=3)

    if not candidates:
        fallback = (
            "Sorry, I could not find information related to your question."
            if language == "English"
            else "क्षमा करें, मुझे आपके प्रश्न से संबंधित जानकारी नहीं मिली।"
        )
        return fallback, ["FAQ Knowledge Base"]

    top_score = candidates[0]["score"]
    if top_score < FAQ_SCORE_THRESHOLD:
        fallback = (
            "Sorry, I could not find information related to your question."
            if language == "English"
            else "क्षमा करें, मुझे आपके प्रश्न से संबंधित जानकारी नहीं मिली।"
        )
        return fallback, ["FAQ Knowledge Base"]

    answers = []
    for item in candidates:
        if item["score"] >= FAQ_SCORE_THRESHOLD:
            answers.append(item["document"]["answer"])

    if not answers:
        fallback = (
            "Sorry, I could not find information related to your question."
            if language == "English"
            else "क्षमा करें, मुझे आपके प्रश्न से संबंधित जानकारी नहीं मिली।"
        )
        return fallback, ["FAQ Knowledge Base"]

    merged_answer = "\n\n".join(answers)
    return merged_answer, ["FAQ Knowledge Base"]
