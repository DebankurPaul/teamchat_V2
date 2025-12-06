import sqlite3

def check_schema():
    conn = sqlite3.connect('teamchat.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(messages)")
    columns = cursor.fetchall()
    conn.close()
    
    print("Columns in 'messages' table:")
    for col in columns:
        print(f"- {col[1]} ({col[2]})")

if __name__ == "__main__":
    check_schema()
