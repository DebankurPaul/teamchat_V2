import sqlite3

def cleanup_test():
    conn = sqlite3.connect('teamchat.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chats WHERE name LIKE 'Test Group%'")
    conn.commit()
    print(f"Deleted {cursor.rowcount} test chats.")
    conn.close()

if __name__ == "__main__":
    cleanup_test()
