import sqlite3
import json

def dump_replies():
    conn = sqlite3.connect('teamchat.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, text, replyTo FROM messages WHERE replyTo IS NOT NULL ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()
    
    with open("dump_output.txt", "w", encoding="utf-8") as f:
        f.write(f"Found {len(rows)} messages with replyTo.\n")
        
        for row in rows:
            f.write("-" * 20 + "\n")
            f.write(f"Msg ID: {row['id']}\n")
            f.write(f"Text: {row['text']}\n")
            try:
                r = json.loads(row['replyTo'])
                f.write(f"ReplyTo Keys: {list(r.keys())}\n")
                f.write(f"ReplyTo Sender: {r.get('sender')} (Type: {type(r.get('sender'))})\n")
                f.write(f"ReplyTo Text: {r.get('text')}\n")
            except Exception as e:
                f.write(f"Error parsing JSON: {e}\n")
                f.write(f"Raw Content: {row['replyTo']}\n")

    conn.close()

if __name__ == "__main__":
    dump_replies()
