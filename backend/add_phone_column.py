from database import get_db_connection

def add_phone_column():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='users' AND column_name='phone'")
        if not cursor.fetchone():
            print("Adding phone column...")
            cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT UNIQUE")
            # Also drop NOT NULL constraint on email if it exists (it was created as TEXT UNIQUE, which allows NULLs in Postgres unless specified otherwise)
            # But let's be sure
            print("Phone column added.")
        else:
            print("Phone column already exists.")
            
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_phone_column()
