from database import get_db_connection

def add_settings_column():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("Adding settings column to users table...")
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS settings TEXT DEFAULT '{}'")
        conn.commit()
        print("Column 'settings' added successfully.")
    except Exception as e:
        print(f"Error adding column: {e}")
        conn.rollback()
    
    conn.close()

if __name__ == "__main__":
    add_settings_column()
