#!/usr/bin/env python

import requests
import json

BASE_URL = "http://localhost:8000"

test_cases = [
    {
        "query": "What is Sewa Setu?",
        "type": "faq",
    },
    {
        "query": "How can citizens track their application status?",
        "type": "faq",
    },
    {
        "query": "Show pending applications",
        "type": "sql",
    },
]

print("Testing Chat API\n" + "=" * 60)

for test_case in test_cases:
    query = test_case["query"]
    expected_type = test_case["type"]
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"prompt": query},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            response_type = data.get("response_type", "unknown")
            
            print(f"\n✓ Query: {query}")
            print(f"  Expected Type: {expected_type}")
            print(f"  Response Type: {response_type}")
            
            if response_type == "faq":
                answer = data.get("answer", "")
                sources = data.get("sources", [])
                print(f"  Answer: {answer[:150]}...")
                print(f"  Sources: {sources}")
            elif response_type == "sql":
                sql = data.get("generated_sql", "")
                rows = data.get("rows", [])
                print(f"  SQL: {sql}")
                print(f"  Rows: {len(rows)} results")
        else:
            print(f"\n✗ Query: {query}")
            print(f"  Error: Status {response.status_code}")
            print(f"  Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"\n✗ Cannot connect to API at {BASE_URL}")
        print("  Make sure the backend server is running (python main.py)")
        break
    except Exception as e:
        print(f"\n✗ Query: {query}")
        print(f"  Error: {str(e)}")

print("\n" + "=" * 60)
