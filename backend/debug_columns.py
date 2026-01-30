import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:deb172006@localhost:5432/teamchat")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages LIMIT 0")
    print([desc[0] for desc in cur.description])
    conn.close()
except Exception as e:
    print(e)
