import requests
import json
import time

def test_post_message():
    chat_id = 1764991531567 # from screenshot
    url = f"http://localhost:8000/chats/{chat_id}/messages"
    
    # Payload matching frontend exactly
    payload = {
        "text": "Hello Test",
        "sender": "me", # Testing fallback string
        "time": "10:00 AM",
        "status": "sent",
        "replyTo": None
    }
    
    print(f"Sending POST to {url}...")
    try:
        r = requests.post(url, json=payload)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
    except Exception as e:
        print(f"Request failed: {e}")

    # Test with Integer ID
    payload["sender"] = 123
    print("\nSending POST with int sender...")
    try:
        r = requests.post(url, json=payload)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_post_message()
