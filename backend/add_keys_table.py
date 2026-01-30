from database import get_db_connection

def add_keys_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("Creating user_keys table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_keys (
                user_id BIGINT PRIMARY KEY,
                public_key TEXT, -- Identity Key (Public)
                pre_key_bundle TEXT, -- JSON bundle of pre-keys
                timestamp TEXT,
                synced BOOLEAN DEFAULT FALSE
            )
        ''')
        print("user_keys table created.")
            
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_keys_table()
