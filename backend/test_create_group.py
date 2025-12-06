import requests
import json
import datetime

URL = "http://localhost:8000/chats"

def test_create():
    payload = {
        "name": "Test Group 123",
        "lastMessage": "Group created",
        "time": "Just now",
        "unread": 0,
        "avatar": "https://ui-avatars.com/api/?name=Test&background=random",
        "type": "group",
        "isPrivate": True,
        "participants": [{"id": 999, "name": "Test User", "email": "test@test.com"}],
        "members": 1,
        "createdBy": None
    }
    
    try:
        print(f"Sending POST to {URL}...")
        resp = requests.post(URL, json=payload)
        print(f"Status Code: {resp.status_code}")
        print(f"Response: {resp.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_create()
