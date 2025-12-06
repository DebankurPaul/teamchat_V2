import sqlite3
import os

DB_PATH = 'teamchat.db'

def check():
    if not os.path.exists(DB_PATH):
        print(f"DB not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"Checking {DB_PATH}")
    cursor.execute("PRAGMA table_info(chats)")
    cols = cursor.fetchall()
    for c in cols:
        print(c)
        
    conn.close()

if __name__ == "__main__":
    check()
