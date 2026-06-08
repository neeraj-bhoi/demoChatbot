#!/usr/bin/env python

from faq.faq_loader import load_faq_documents

try:
    docs = load_faq_documents()
    print(f"✓ Successfully loaded {len(docs)} FAQ documents")
    print(f"\n--- First FAQ Entry ---")
    print(f"Question: {docs[0]['question']}")
    print(f"Answer: {docs[0]['answer'][:200]}...")
    print(f"\n--- Second FAQ Entry (if exists) ---")
    if len(docs) > 1:
        print(f"Question: {docs[1]['question']}")
        print(f"Answer: {docs[1]['answer'][:200]}...")
except Exception as e:
    print(f"✗ Error loading FAQ documents: {e}")
    import traceback
    traceback.print_exc()
