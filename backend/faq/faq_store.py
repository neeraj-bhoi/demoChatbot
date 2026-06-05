from __future__ import annotations

# import math
# from pathlib import Path
from typing import Dict, List

import numpy as np
from sentence_transformers import SentenceTransformer

from .faq_loader import load_faq_documents


class FAQVectorStore:
    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)
        self.documents = load_faq_documents()
        self.embeddings = self._build_embeddings([doc["text"] for doc in self.documents])

    def _build_embeddings(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        return float(np.dot(a, b))

    def query(self, query_text: str, language: str, top_k: int = 3) -> List[Dict]:
        query_embedding = self._build_embeddings([query_text])[0]
        results = []
        for document, embedding in zip(self.documents, self.embeddings):
            if document["language"] != language:
                continue
            score = self._cosine_similarity(query_embedding, embedding)
            results.append({"document": document, "score": score})
        results.sort(key=lambda item: item["score"], reverse=True)
        return results[:top_k]


faq_store = FAQVectorStore()