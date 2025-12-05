import sqlite3

def migrate():
    conn = sqlite3.connect('teamchat.db')
    cursor = conn.cursor()
    
    print("Adding call columns to messages table...")
    
    try:
        cursor.execute("ALTER TABLE messages ADD COLUMN callRoomName TEXT")
        print("Added callRoomName")
    except sqlite3.OperationalError:
        print("callRoomName already exists")
        
    try:
        cursor.execute("ALTER TABLE messages ADD COLUMN callStatus TEXT")
        print("Added callStatus")
    except sqlite3.OperationalError:
        print("callStatus already exists")
        
    try:
        cursor.execute("ALTER TABLE messages ADD COLUMN isVoice BOOLEAN DEFAULT 0")
        print("Added isVoice")
    except sqlite3.OperationalError:
        print("isVoice already exists")
        
    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
