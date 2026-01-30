from database import get_db_connection

def add_blocked_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("Adding blocked_users table...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blocked_users (
            blocker_id BIGINT,
            blocked_id BIGINT,
            timestamp TEXT,
            PRIMARY KEY (blocker_id, blocked_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Table 'blocked_users' created successfully.")

if __name__ == "__main__":
    add_blocked_users_table()
