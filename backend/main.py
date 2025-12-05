import json
import os
import shutil
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from models import Message, IdeaAnalysis, FileInput
from websocket_manager import ConnectionManager
from ai_service import analyze_text, analyze_file_content
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase
if not firebase_admin._apps:
    # Get credentials path from env or default to file
    cred_path = os.getenv("FIREBASE_CREDENTIALS", "serviceAccountKey.json")
    if not os.path.exists(cred_path):
        print(f"Warning: Firebase credentials not found at {cred_path}")
    else:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

db = firestore.client()

app = FastAPI()

# Create uploads directory
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Helper Functions ---

def get_user(user_id: int):
    # Query by integer ID field, not document ID (unless we migrate IDs to strings)
    # For MVP, we'll search the collection. Ideally, use string IDs as doc IDs.
    users_ref = db.collection("users")
    query = users_ref.where("id", "==", user_id).limit(1).stream()
    for doc in query:
        return doc.to_dict()
    return None

def get_user_by_email(email: str):
    users_ref = db.collection("users")
    query = users_ref.where("email", "==", email).limit(1).stream()
    for doc in query:
        return doc.to_dict()
    return None

def create_user_doc(user_data):
    # Use email as doc ID or auto-gen. Let's use auto-gen for now but store ID.
    # To maintain integer IDs for frontend compatibility, we need to track max ID or just use timestamp/random int.
    # For simplicity in this migration, let's just use the provided ID.
    db.collection("users").add(user_data)

def update_user_doc(user_id: int, update_data):
    users_ref = db.collection("users")
    query = users_ref.where("id", "==", user_id).limit(1).stream()
    for doc in query:
        doc.reference.update(update_data)
        return

def get_chat_doc(chat_id: int):
    chats_ref = db.collection("chats")
    query = chats_ref.where("id", "==", chat_id).limit(1).stream()
    for doc in query:
        data = doc.to_dict()
        data['doc_id'] = doc.id # Store doc_id for subcollection access
        return data
    return None

# --- Endpoints ---

@app.post("/login")
async def login(user_data: dict):
    email = user_data.get("email")
    existing_user = get_user_by_email(email)
    
    if existing_user:
        return existing_user
    
    # Get new ID (naive approach: count documents - prone to race conditions but ok for MVP)
    # Better: Use Firestore UUIDs, but frontend expects ints? Let's check frontend.
    # Frontend seems to treat IDs as whatever backend sends.
    # Let's stick to ints for now to minimize frontend breakage.
    users_ref = db.collection("users")
    # Use timestamp for ID to avoid collisions
    new_id = int(datetime.now().timestamp() * 1000)

    new_user = {
        "id": new_id,
        "name": user_data.get("name", "User"),
        "email": email,
        "avatar": f"https://ui-avatars.com/api/?name={user_data.get('name', 'User')}&background=random",
        "status": "offline",
        "lastSeen": None
    }
    create_user_doc(new_user)
    return new_user

@app.put("/users/{user_id}")
async def update_user(user_id: int, user_data: dict):
    user = get_user(user_id)
    if not user:
        return {"error": "User not found"}
    
    updates = {}
    if "name" in user_data:
        updates["name"] = user_data["name"]
        updates["avatar"] = f"https://ui-avatars.com/api/?name={user_data['name']}&background=random"
    
    if updates:
        update_user_doc(user_id, updates)
        # Return updated user
        user.update(updates)
        return user
    return user

@app.get("/ideas")
async def get_ideas():
    ideas_ref = db.collection("ideas")
    return [doc.to_dict() for doc in ideas_ref.stream()]

@app.post("/ideas")
async def add_idea(idea: dict):
    # idea: {title, content, tags}
    new_idea = idea.copy()
    # Add ID
    ideas_ref = db.collection("ideas")
    # Use timestamp for ID
    new_id = int(datetime.now().timestamp() * 1000)
    new_idea["id"] = new_id
    new_idea["timestamp"] = datetime.now().isoformat()
    
    db.collection("ideas").add(new_idea)
    return new_idea

@app.delete("/ideas/{idea_id}")
async def delete_idea(idea_id: int):
    ideas_ref = db.collection("ideas")
    query = ideas_ref.where("id", "==", idea_id).limit(1).stream()
    for doc in query:
        doc.reference.delete()
        return {"message": "Idea deleted"}
    raise HTTPException(status_code=404, detail="Idea not found")

@app.get("/chats")
async def get_chats(user_id: int = None):
    chats_ref = db.collection("chats")
    all_chats = [doc.to_dict() for doc in chats_ref.stream()]
    
    if user_id:
        # Filter chats where user is a participant
        # Participants is a list of dicts {id, name, ...}
        user_chats = []
        for chat in all_chats:
            participants = chat.get("participants", [])
            # Check if user_id is in participants list
            if any(p.get("id") == user_id for p in participants):
                user_chats.append(chat)
        return user_chats
    
    return all_chats

@app.post("/chats")
async def create_chat(chat_data: dict):
    # chat_data: {name, type, participants, avatar}
    chats_ref = db.collection("chats")
    # Use timestamp for ID
    new_id = int(datetime.now().timestamp() * 1000)
    
    new_chat = {
        "id": new_id,
        "name": chat_data["name"],
        "type": chat_data.get("type", "group"),
        "participants": chat_data.get("participants", []),
        "avatar": chat_data.get("avatar", f"https://ui-avatars.com/api/?name={chat_data['name']}&background=random"),
        "members": len(chat_data.get("participants", [])),
        "lastMessage": "Tap to start chatting",
        "timestamp": datetime.now().isoformat(),
        "isPrivate": chat_data.get("isPrivate", False),
        "createdBy": chat_data.get("createdBy", None)
    }
    db.collection("chats").add(new_chat)
    return new_chat

@app.get("/chats/public")
async def get_public_chats():
    chats_ref = db.collection("chats")
    # Filter for public groups
    # Note: Firestore filtering might require an index. For MVP, filter in memory if dataset is small.
    # Ideally: chats_ref.where("isPrivate", "==", False).where("type", "==", "group").stream()
    
    all_chats = [doc.to_dict() for doc in chats_ref.stream()]
    public_chats = [
        c for c in all_chats 
        if c.get("type") == "group" and not c.get("isPrivate", False)
    ]
    return public_chats

@app.post("/chats/join")
async def join_chat(request: dict):
    chat_id = request.get("chat_id")
    user = request.get("user")
    
    chat_doc_data = get_chat_doc(chat_id)
    
    if not chat_doc_data:
        # Auto-create if not exists (legacy behavior)
        new_chat = {
            "id": chat_id,
            "name": f"Group {chat_id}",
            "type": "group",
            "participants": [user],
            "avatar": f"https://ui-avatars.com/api/?name=Group {chat_id}&background=random",
            "members": 1,
            "lastMessage": "Tap to start chatting",
            "timestamp": datetime.now().isoformat()
        }
        db.collection("chats").add(new_chat)
        return {"message": "Joined new chat", "chat": new_chat}
    
    # Update existing chat
    participants = chat_doc_data.get("participants", [])
    if not any(p.get("id") == user["id"] for p in participants):
        participants.append(user)
        
        # Update Firestore
        chats_ref = db.collection("chats")
        query = chats_ref.where("id", "==", chat_id).limit(1).stream()
        for doc in query:
            doc.reference.update({
                "participants": participants,
                "members": len(participants)
            })
            
    return {"message": "Joined chat", "chat": chat_doc_data}

@app.get("/chats/{chat_id}/messages")
async def get_messages(chat_id: int):
    chat_doc_data = get_chat_doc(chat_id)
    if not chat_doc_data:
        return []
    
    # Get messages from subcollection
    # Need the doc_ref to access subcollection
    chats_ref = db.collection("chats")
    query = chats_ref.where("id", "==", chat_id).limit(1).stream()
    for doc in query:
        messages_ref = doc.reference.collection("messages")
        # Order by timestamp or ID? ID for now as it was sequential
        # But Firestore IDs are strings. We should store a timestamp or sequence ID.
        # Let's sort by 'id' assuming we store it as int
        msgs = [m.to_dict() for m in messages_ref.order_by("id").stream()]
        return msgs
    return []

@app.post("/chats/{chat_id}/messages")
async def add_message(chat_id: int, message: Message):
    chat_doc_data = get_chat_doc(chat_id)
    if not chat_doc_data:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    chats_ref = db.collection("chats")
    query = chats_ref.where("id", "==", chat_id).limit(1).stream()
    
    for doc in query:
        messages_ref = doc.reference.collection("messages")
        
        # Generate ID using timestamp
        new_id = int(datetime.now().timestamp() * 1000)
        
        msg_dict = message.dict()
        msg_dict["id"] = new_id
        msg_dict["isPinned"] = False # Default
        
        messages_ref.add(msg_dict)
        
        # Update last message in chat
        doc.reference.update({
            "lastMessage": msg_dict.get("text", "Sent a file") if msg_dict.get("type") != "file" else "Sent a file",
            "timestamp": msg_dict.get("time") # Note: time format might differ from ISO
        })
        
        return msg_dict
        
    raise HTTPException(status_code=404, detail="Chat doc not found")

@app.delete("/chats/{chat_id}/messages")
async def clear_chat_messages(chat_id: int):
    chats_ref = db.collection("chats")
    query = chats_ref.where("id", "==", chat_id).limit(1).stream()
    
    for doc in query:
        messages_ref = doc.reference.collection("messages")
        # Delete all documents in subcollection
        # Note: Firestore requires deleting docs individually
        batch = db.batch()
        count = 0
        for msg in messages_ref.stream():
            batch.delete(msg.reference)
            count += 1
            if count >= 400: # Commit every 400 deletes
                batch.commit()
                batch = db.batch()
                count = 0
        
        if count > 0:
            batch.commit()
            
        # Update last message
        doc.reference.update({
            "lastMessage": "Chat cleared",
            "timestamp": datetime.now().isoformat()
        })
        
        return {"message": "Chat cleared"}
    
    raise HTTPException(status_code=404, detail="Chat not found")

@app.delete("/chats/{chat_id}")
async def delete_chat(chat_id: int):
    chats_ref = db.collection("chats")
    query = chats_ref.where("id", "==", chat_id).limit(1).stream()
    
    for doc in query:
        # 1. Delete messages subcollection
        messages_ref = doc.reference.collection("messages")
        batch = db.batch()
        count = 0
        for msg in messages_ref.stream():
            batch.delete(msg.reference)
            count += 1
            if count >= 400:
                batch.commit()
                batch = db.batch()
                count = 0
        if count > 0:
            batch.commit()
            
        # 2. Delete chat document
        doc.reference.delete()
        return {"message": "Chat deleted"}
        
    raise HTTPException(status_code=404, detail="Chat not found")

@app.post("/chats/{chat_id}/messages/{message_id}/pin")
async def pin_message(chat_id: int, message_id: int):
    chats_ref = db.collection("chats")
    query = chats_ref.where("id", "==", chat_id).limit(1).stream()
    
    for doc in query:
        messages_ref = doc.reference.collection("messages")
        msg_query = messages_ref.where("id", "==", message_id).limit(1).stream()
        
        for msg_doc in msg_query:
            msg_data = msg_doc.to_dict()
            new_status = not msg_data.get("isPinned", False)
            msg_doc.reference.update({"isPinned": new_status})
            
            msg_data["isPinned"] = new_status
            return msg_data
            
    raise HTTPException(status_code=404, detail="Message not found")

@app.put("/chats/{chat_id}/messages/{message_id}")
async def update_message(chat_id: int, message_id: int, updates: dict):
    chats_ref = db.collection("chats")
    query = chats_ref.where("id", "==", chat_id).limit(1).stream()
    
    for doc in query:
        messages_ref = doc.reference.collection("messages")
        msg_query = messages_ref.where("id", "==", message_id).limit(1).stream()
        
        for msg_doc in msg_query:
            msg_doc.reference.update(updates)
            updated_data = msg_doc.to_dict()
            updated_data.update(updates)
            return updated_data
            
    raise HTTPException(status_code=404, detail="Message not found")

@app.delete("/chats/{chat_id}/messages/{message_id}")
async def delete_message(chat_id: int, message_id: int):
    chats_ref = db.collection("chats")
    query = chats_ref.where("id", "==", chat_id).limit(1).stream()
    
    for doc in query:
        messages_ref = doc.reference.collection("messages")
        msg_query = messages_ref.where("id", "==", message_id).limit(1).stream()
        
        for msg_doc in msg_query:
            msg_doc.reference.delete()
            return {"message": "Message deleted"}
            
    raise HTTPException(status_code=404, detail="Message not found")



@app.post("/chats/{chat_id}/participants")
async def add_participant(chat_id: int, user_data: dict):
    email = user_data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
        
    user_to_add = get_user_by_email(email)
    if not user_to_add:
        raise HTTPException(status_code=404, detail="User not found")
        
    chats_ref = db.collection("chats")
    query = chats_ref.where("id", "==", chat_id).limit(1).stream()
    
    for doc in query:
        chat_data = doc.to_dict()
        participants = chat_data.get("participants", [])
        
        # Check if already in chat
        if any(p.get("id") == user_to_add["id"] for p in participants):
             raise HTTPException(status_code=400, detail="User already in chat")
             
        participants.append(user_to_add)
        
        doc.reference.update({
            "participants": participants,
            "members": len(participants)
        })
        
        return {"message": "User added", "user": user_to_add}
            
    raise HTTPException(status_code=404, detail="Chat not found")

@app.get("/chats/{chat_id}/participants")
async def get_participants(chat_id: int):
    chat = get_chat_doc(chat_id)
    if chat:
        return chat.get("participants", [])
    return []

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    return {"url": f"http://localhost:8000/uploads/{file.filename}"}

@app.post("/analyze-message")
async def analyze_message_endpoint(analysis_request: IdeaAnalysis):
    is_idea, confidence = analyze_text(analysis_request.text)
    
    if is_idea:
        # Save to Firestore ideas
        new_idea = {
            "title": f"Idea from {analysis_request.sender}",
            "content": analysis_request.text,
            "tags": ["AI Detected"],
            "timestamp": datetime.now().isoformat()
        }
        # Add ID
        ideas_ref = db.collection("ideas")
        count = len(list(ideas_ref.stream()))
        new_idea["id"] = count + 1
        
        db.collection("ideas").add(new_idea)
        
    return {"is_idea": is_idea, "confidence": confidence}

from file_extractor import extract_text

@app.post("/analyze-file")
async def analyze_file_endpoint(file_input: FileInput):
    file_path = f"uploads/{file_input.filename}"
    
    try:
        # Extract text content
        extracted_text = extract_text(file_path)
        
        if not extracted_text or "Unsupported" in extracted_text:
            if not extracted_text:
                extracted_text = f"File: {file_input.filename}"
                
        # Analyze the extracted text
        analysis = analyze_text(extracted_text)
        
        # Force is_idea to True since user explicitly requested it
        analysis.is_idea = True
        
        if analysis.is_idea:
             new_idea = {
                "title": f"File Idea: {file_input.filename}",
                "content": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
                "full_content": extracted_text,
                "tags": ["File", "AI Detected", analysis.category or "General"],
                "timestamp": datetime.now().isoformat(),
                "priority": analysis.priority,
                "viability_score": analysis.viability_score,
                "deadline": analysis.deadline,
                "action_suggestion": analysis.action_suggestion
            }
             ideas_ref = db.collection("ideas")
             count = len(list(ideas_ref.stream()))
             new_idea["id"] = count + 1
             
             db.collection("ideas").add(new_idea)
             
        return analysis
    except Exception as e:
        print(f"Error analyzing file: {e}")
        # Fallback to simple analysis
        return {"is_idea": False, "error": str(e)}


# WebSocket for real-time (Optional: Integrate with Firestore listeners later)
manager = ConnectionManager()

@app.websocket("/ws/{chat_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int, user_id: int):
    await manager.connect(websocket, chat_id, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Here we could save to Firestore too, but we use REST for saving currently
            # Just broadcast for now
            await manager.broadcast(data, chat_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id, user_id)
