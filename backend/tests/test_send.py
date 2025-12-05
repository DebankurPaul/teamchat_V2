import requests
import json

url = "http://localhost:8000/chats/1/messages"
headers = {"Content-Type": "application/json"}
data = {
    "text": "Test message",
    "sender": "me",
    "time": "10:00 AM",
    "status": "sent"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
