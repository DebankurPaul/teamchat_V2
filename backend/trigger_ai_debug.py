import requests

print("Triggering AI analysis...")
try:
    response = requests.post("http://localhost:8000/analyze-message", json={
        "text": "My idea is a new app that helps people find parking spots in crowded cities.",
        "sender": "debug_user"
    })
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
