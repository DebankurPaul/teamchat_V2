import firebase_admin
from firebase_admin import credentials, firestore
import os

# Check if file exists
if not os.path.exists("serviceAccountKey.json"):
    print("Error: serviceAccountKey.json not found!")
    exit(1)

# Initialize
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase initialized successfully.")
except Exception as e:
    print(f"Error initializing Firebase: {e}")
    exit(1)

# Test Write
try:
    doc_ref = db.collection("test_collection").document("test_doc")
    doc_ref.set({"message": "Hello Firebase!"})
    print("Write successful.")
except Exception as e:
    print(f"Error writing to Firestore: {e}")

# Test Read
try:
    doc = doc_ref.get()
    if doc.exists:
        print(f"Read successful: {doc.to_dict()}")
    else:
        print("Error: Document not found.")
except Exception as e:
    print(f"Error reading from Firestore: {e}")
