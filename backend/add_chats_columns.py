import sqlite3

def add_columns():
    conn = sqlite3.connect('teamchat.db')
    cursor = conn.cursor()
    
    # Check for createdBy
    try:
        cursor.execute("ALTER TABLE chats ADD COLUMN createdBy TEXT")
        print("Added createdBy column")
    except sqlite3.OperationalError as e:
        print(f"createdBy might exist: {e}")
        
    # Check for synced
    try:
        cursor.execute("ALTER TABLE chats ADD COLUMN synced BOOLEAN DEFAULT 0")
        print("Added synced column")
    except sqlite3.OperationalError as e:
        print(f"synced might exist: {e}")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_columns()
