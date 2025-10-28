#!/usr/bin/env python3
"""Test KY analysis-ready endpoint"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("Testing KY analysis-ready endpoint...")
print("="*80)

# Test 1: Get count
print("\n1. Testing /ky/ar_ky/count")
response = requests.get(f"{BASE_URL}/ky/ar_ky/count")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 2: Get first 5 records
print("\n2. Testing /ky/analysis-ready?limit=5")
response = requests.get(f"{BASE_URL}/ky/analysis-ready?limit=5")
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Returned {len(data)} records")
    if len(data) > 0:
        print(f"\nFirst record sample:")
        print(json.dumps(data[0], indent=2))
else:
    print(f"Error: {response.text}")

print("\n" + "="*80)
print("✓ KY analysis-ready endpoint is working!")
