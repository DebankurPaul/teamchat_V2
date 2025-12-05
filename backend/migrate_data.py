import json
import firebase_admin
from firebase_admin import credentials, firestore
import os

# 1. Initialize Firebase
if not os.path.exists("serviceAccountKey.json"):
    print("Error: serviceAccountKey.json not found!")
    exit(1)

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 2. Load Data
DATA_FILE = "data.json"
if not os.path.exists(DATA_FILE):
    print(f"Error: {DATA_FILE} not found!")
    exit(1)

with open(DATA_FILE, "r") as f:
    data = json.load(f)

print(f"Loaded data from {DATA_FILE}")

# 3. Migrate Users
users = data.get("users", [])
print(f"Migrating {len(users)} users...")
users_ref = db.collection("users")
for user in users:
    # Use Firestore auto-ID or specific ID? 
    # To keep things simple and consistent with our new main.py which queries by 'id' field,
    # we can just add the document.
    users_ref.add(user)
print("Users migrated.")

# 4. Migrate Ideas
ideas = data.get("ideas", [])
print(f"Migrating {len(ideas)} ideas...")
ideas_ref = db.collection("ideas")
for idea in ideas:
    ideas_ref.add(idea)
print("Ideas migrated.")

# 5. Migrate Chats & Messages
chats = data.get("chats", [])
messages_map = data.get("messages", {})

print(f"Migrating {len(chats)} chats...")
chats_ref = db.collection("chats")

for chat in chats:
    chat_id = chat.get("id")
    
    # Add Chat Document
    # We let Firestore generate the document ID, but we store the 'id' field inside.
    # (This matches our main.py logic)
    _, chat_doc_ref = chats_ref.add(chat)
    
    # Add Messages for this chat
    # messages_map keys might be strings in JSON, but chat_id is int. Handle both.
    chat_msgs = messages_map.get(str(chat_id)) or messages_map.get(chat_id) or []
    
    if chat_msgs:
        print(f"  - Migrating {len(chat_msgs)} messages for chat {chat_id}...")
        messages_ref = chat_doc_ref.collection("messages")
        for msg in chat_msgs:
            messages_ref.add(msg)

print("Chats and messages migrated.")
print("Migration complete! 🚀")
