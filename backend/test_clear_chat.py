import requests
import json
import time

BASE_URL = "http://localhost:8000"
CHAT_ID = 1 # Assuming chat 1 exists

def test_clear_chat():
    # 1. Add a message
    print("Adding message...")
    msg = {
        "text": "Message to be deleted",
        "sender": "test_script",
        "time": "12:00 PM"
    }
    res = requests.post(f"{BASE_URL}/chats/{CHAT_ID}/messages", json=msg)
    if res.status_code != 200:
        print(f"Failed to add message: {res.text}")
        return

    print("Message added.")
    
    # 2. Clear chat
    print("Clearing chat...")
    res = requests.delete(f"{BASE_URL}/chats/{CHAT_ID}/messages")
    if res.status_code == 200:
        print("Chat cleared successfully.")
    else:
        print(f"Failed to clear chat: {res.text}")

    # 3. Verify empty
    print("Verifying...")
    res = requests.get(f"{BASE_URL}/chats/{CHAT_ID}/messages")
    messages = res.json()
    if len(messages) == 0:
        print("Verification successful: Chat is empty.")
    else:
        print(f"Verification failed: {len(messages)} messages found.")

if __name__ == "__main__":
    test_clear_chat()
