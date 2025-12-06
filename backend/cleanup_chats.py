import sqlite3
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Init Firebase (Copy-paste from main.py logic or simplified)
# Assuming serviceAccountKey.json is available
if not firebase_admin._apps:
    cred_path = os.getenv("FIREBASE_CREDENTIALS", "serviceAccountKey.json")
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    else:
        print("No firebase creds, skipping firestore cleanup")

def cleanup():
    # 1. SQLite Cleanup
    conn = sqlite3.connect('teamchat.db')
    cursor = conn.cursor()
    
    print("Deleting ID 1 and 2 from SQLite...")
    cursor.execute("DELETE FROM messages WHERE chat_id IN (1, 2)")
    cursor.execute("DELETE FROM chats WHERE id IN (1, 2)")
    conn.commit()
    print(f"Deleted {cursor.rowcount} chats from SQLite.")
    conn.close()

    # 2. Firestore Cleanup
    try:
        db = firestore.client()
        chats_ref = db.collection("chats")
        for chat_id in [1, 2]:
            query = chats_ref.where("id", "==", chat_id).stream()
            for doc in query:
                print(f"Deleting Firestore doc {doc.id} (Chat ID {chat_id})")
                doc.reference.delete()
    except Exception as e:
        print(f"Firestore cleanup error (might be expected if no creds): {e}")

if __name__ == "__main__":
    cleanup()
