import os
import psycopg2
from dotenv import load_dotenv

from pathlib import Path

# Explicitly load .env from the backend directory
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

def add_index():
    # Use the same default as database.py
    url = os.getenv("DATABASE_URL", "postgresql://postgres:deb172006@localhost:5432/teamchat")
    if not url:
        print("DATABASE_URL not found")
        return

    try:
        conn = psycopg2.connect(url)
        cursor = conn.cursor()
        
        print("Adding index to messages(chat_id)...")
        # specific to postgres
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_chat_id ON messages (chat_id);")
        
        print("Adding index to ideas(timestamp)...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ideas_timestamp ON ideas (timestamp DESC);")

        conn.commit()
        conn.close()
        print("Indexes added successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_index()
