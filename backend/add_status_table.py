from database import get_db_connection

def add_status_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("Creating status table...")
        # SQLite usage in previous parts suggested TIMESTAMP might be text or int.
        # In PG, we can use TIMESTAMP, but let's stick to TEXT ISO format for consistency with existing code.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS status (
                id BIGINT PRIMARY KEY,
                user_id BIGINT, -- No foreign key constraint for simplicity allowing soft deletes/delays
                type TEXT, -- 'image', 'video', 'text'
                content TEXT, -- URL or text content
                caption TEXT,
                timestamp TEXT, -- Creation time
                expires_at TEXT, -- Expiration time (24h later)
                viewers TEXT DEFAULT '[]', -- JSON list of user_ids who viewed
                synced BOOLEAN DEFAULT FALSE
            )
        ''')
        print("status table created.")
            
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_status_table()
