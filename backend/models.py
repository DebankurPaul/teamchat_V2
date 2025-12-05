from pydantic import BaseModel
from typing import Optional

class Message(BaseModel):
    text: Optional[str] = None
    sender: str
    type: str = "text"
    filename: Optional[str] = None
    fileUrl: Optional[str] = None
    size: Optional[str] = None
    time: Optional[str] = None
    status: Optional[str] = None
    replyTo: Optional[dict] = None
    isForwarded: bool = False
    isPinned: bool = False
    callRoomName: Optional[str] = None
    callStatus: Optional[str] = None
    isVoice: bool = False

class IdeaAnalysis(BaseModel):
    is_idea: bool
    category: Optional[str] = None
    priority: Optional[str] = None
    viability_score: int = 0
    deadline: Optional[str] = None
    action_suggestion: Optional[str] = None

class FileInput(BaseModel):
    filename: str
    content_preview: str
