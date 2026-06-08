#!/usr/bin/env python

import sys
from ai_intent_classifier import classify_intent_ai

test_queries = [
    "What is Sewa Setu?",  # Should be FAQ
    "How do I apply for a certificate?",  # Should be FAQ
    "What documents are needed?",  # Should be FAQ
    "Show all pending applications",  # Should be SQL
    "List citizens from Delhi",  # Should be SQL
    "How many approved certificates today?",  # Could be SQL
    "कैसे आवेदन करें?",  # Hindi FAQ
    "सभी पेंडिंग आवेदन दिखाएं",  # Hindi SQL
]

print("Testing AI-based Intent Classification\n" + "=" * 50)

for query in test_queries:
    try:
        intent = classify_intent_ai(query)
        print(f"Query: {query}")
        print(f"Classification: {intent}\n")
    except Exception as e:
        print(f"Query: {query}")
        print(f"Error: {str(e)}\n")
