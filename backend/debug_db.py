import sqlite3
import json

def inspect_chats():
    conn = sqlite3.connect('teamchat.db')
    cursor = conn.cursor()
    
    print("--- Chats Table Info ---")
    cursor.execute("PRAGMA table_info(chats)")
    columns = cursor.fetchall()
    for col in columns:
        print(col)
        
    print("\n--- Testing Deletion (Simulation) ---")
    # Simulate finding the 'Game' chat
    target_id = None
    for row in rows:
        if row[1] == "Game":
            target_id = row[0]
            print(f"Found 'Game' chat with ID: {target_id} (Type: {type(target_id)})")
            
    conn.close()

if __name__ == "__main__":
    inspect_chats()
