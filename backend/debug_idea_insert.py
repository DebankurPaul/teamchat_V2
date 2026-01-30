from database import get_db_connection, init_db
from datetime import datetime

def debug_insert():
    try:
        # 1. Ensure DB init
        print("Running init_db()...")
        init_db()
        
        # 2. Try Insert
        print("Attempting Insert...")
        conn = get_db_connection()
        cursor = conn.cursor()
        
        new_id = int(datetime.now().timestamp() * 1000)
        timestamp = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO ideas (id, text, category, votes, timestamp, is_analyzed, synced)
            VALUES (%s, %s, %s, %s, %s, %s, FALSE)
        ''', (
            new_id,
            "Debug Idea Text",
            "General",
            0,
            timestamp,
            True
        ))
        conn.commit()
        conn.close()
        print("Insert Successful!")
        
        # 3. Read Back
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ideas WHERE id = %s", (new_id,))
        row = cursor.fetchone()
        print("Read Back:", row)
        conn.close()
        
    except Exception as e:
        print(f"DEBUG ERROR: {e}")

if __name__ == "__main__":
    debug_insert()
