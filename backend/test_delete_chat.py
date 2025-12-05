import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_delete_chat():
    # 1. Create a chat
    print("Creating chat...")
    chat_data = {
        "name": "Test Delete Chat",
        "type": "group",
        "participants": [],
        "isPrivate": True
    }
    res = requests.post(f"{BASE_URL}/chats", json=chat_data)
    if res.status_code != 200:
        print(f"Failed to create chat: {res.text}")
        return
    
    chat = res.json()
    chat_id = chat["id"]
    print(f"Chat created with ID: {chat_id}")

    # 2. Add a message
    print("Adding message...")
    msg = {
        "text": "Message to be deleted",
        "sender": "test_script",
        "time": "12:00 PM"
    }
    requests.post(f"{BASE_URL}/chats/{chat_id}/messages", json=msg)

    # 3. Delete chat
    print("Deleting chat...")
    res = requests.delete(f"{BASE_URL}/chats/{chat_id}")
    if res.status_code == 200:
        print("Chat deleted successfully.")
    else:
        print(f"Failed to delete chat: {res.text}")
        return

    # 4. Verify deletion
    print("Verifying...")
    # Try to get messages (should fail or return empty/404)
    # Our get_messages returns empty list if chat not found, which is fine.
    # But let's check if the chat exists in the list
    res = requests.get(f"{BASE_URL}/chats")
    all_chats = res.json()
    found = any(c["id"] == chat_id for c in all_chats)
    
    if not found:
        print("Verification successful: Chat not found in list.")
    else:
        print("Verification failed: Chat still exists.")

if __name__ == "__main__":
    test_delete_chat()
