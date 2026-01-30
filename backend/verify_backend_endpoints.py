import requests
import json
import os
from datetime import datetime

API_URL = "http://localhost:8000"

def test_endpoint(name, url, method="GET", payload=None):
    try:
        if method == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url, json=payload)
            
        print(f"[{name}] Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                sample = str(data)[:100] if data else "Empty"
                print(f"[{name}] Success. Data Sample: {sample}")
                return True
            except:
                print(f"[{name}] Success but invalid JSON.")
                return False
        else:
            print(f"[{name}] Failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"[{name}] Error: {e}")
        return False

# 1. Test Chats
test_endpoint("Get Chats", f"{API_URL}/chats")

# 2. Test Ideas
test_endpoint("Get Ideas", f"{API_URL}/ideas")

# 3. Test Analysis (Mock Text)
payload = {
    "text": "Startup Idea: A mobile app that connects local farmers directly with consumers to sell fresh produce.",
    "sender": "test_user"
}
test_endpoint("Analyze Message", f"{API_URL}/analyze-message", "POST", payload)
