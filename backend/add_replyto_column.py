import sqlite3
import json

def migrate():
    print("Migrating database...")
    conn = sqlite3.connect('teamchat.db')
    cursor = conn.cursor()
    
    # Check if column exists
    cursor.execute("PRAGMA table_info(messages)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if "replyTo" not in columns:
        print("Adding replyTo column...")
        cursor.execute("ALTER TABLE messages ADD COLUMN replyTo TEXT")
        conn.commit()
    else:
        print("replyTo column already exists.")
        
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
