
import psycopg2
from database import get_db_connection

def add_username_column():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("Adding username column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS username TEXT UNIQUE")
        conn.commit()
        print("Successfully added username column.")
    except Exception as e:
        print(f"Error adding username column: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_username_column()
