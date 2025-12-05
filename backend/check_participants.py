import sqlite3
import json

def check_participants():
    conn = sqlite3.connect('teamchat.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("--- Checking Chats and Participants ---")
    cursor.execute("SELECT id, name, participants FROM chats")
    rows = cursor.fetchall()
    
    for row in rows:
        chat = dict(row)
        print(f"Chat ID: {chat['id']}, Name: {chat['name']}")
        try:
            participants = json.loads(chat['participants'])
            print(f"  Participants Count: {len(participants)}")
            for p in participants:
                print(f"    - {p.get('name')} (ID: {p.get('id')})")
        except Exception as e:
            print(f"  Error parsing participants: {e}")
            print(f"  Raw data: {chat['participants']}")
        
    conn.close()

if __name__ == "__main__":
    check_participants()
