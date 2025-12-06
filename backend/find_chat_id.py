import sqlite3

def find_chat():
    conn = sqlite3.connect('teamchat.db')
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM messages WHERE id = 1764996567915")
    row = cursor.fetchone()
    print(f"Chat ID: {row[0] if row else 'Not Found'}")
    conn.close()

if __name__ == "__main__":
    find_chat()
