import requests
import json

def test_api():
    chat_id = 1764991531567
    url = f"http://localhost:8000/chats/{chat_id}/messages"
    try:
        res = requests.get(url)
        messages = res.json()
        print(f"Fetched {len(messages)} messages.")
        
        target_id = 1764996567915
        target_msg = next((m for m in messages if m['id'] == target_id), None)
        
        if target_msg:
            print("Target Message Found.")
            print(f"ReplyTo: {target_msg.get('replyTo')}")
            if target_msg.get('replyTo'):
                print(f"ReplyTo keys: {target_msg['replyTo'].keys()}")
                print(f"ReplyTo sender: {target_msg['replyTo'].get('sender')} (Type: {type(target_msg['replyTo'].get('sender'))})")
        else:
            print("Target message not found in API response.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
