import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:deb172006@localhost:5432/teamchat")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT phone, COUNT(*) FROM users GROUP BY phone HAVING COUNT(*) > 1")
    rows = cur.fetchall()
    print("Duplicate Phones:")
    print(rows)

    cur.execute("SELECT * FROM users WHERE phone IN (SELECT phone FROM users GROUP BY phone HAVING COUNT(*) > 1)")
    rows = cur.fetchall()
    print("Duplicate User Rows:")
    for row in rows:
        print(row)
    conn.close()
except Exception as e:
    print(f"Error: {e}")
