import re
from datetime import datetime, timedelta
from models import IdeaAnalysis

def analyze_text(text: str) -> IdeaAnalysis:
    text = text.lower()
    
    # 1. Auto-detect Idea
    idea_keywords = ["idea", "suggestion", "what if", "propose", "should we"]
    is_idea = any(keyword in text for keyword in idea_keywords)
    
    if not is_idea:
        return IdeaAnalysis(is_idea=False)
    
    # 2. Smart Categorization
    category = "General"
    if any(w in text for w in ["blog", "post", "article"]):
        category = "Blog"
    elif any(w in text for w in ["social", "instagram", "twitter", "linkedin"]):
        category = "Social"
    elif any(w in text for w in ["event", "meetup", "party", "retreat"]):
        category = "Event"
    elif any(w in text for w in ["campaign", "launch", "ad"]):
        category = "Campaign"
        
    # 3. Priority Scoring
    priority = "Low"
    if any(w in text for w in ["urgent", "asap", "immediately", "critical"]):
        priority = "High"
    elif any(w in text for w in ["soon", "next week", "important"]):
        priority = "Medium"
        
    # 4. Viability Score (Simple heuristic based on length/detail)
    word_count = len(text.split())
    viability_score = min(10, max(1, word_count // 3))
    
    # 5. Deadline Extraction (Regex)
    deadline = None
    deadline_match = re.search(r"(by|on|before) (monday|tuesday|wednesday|thursday|friday|saturday|sunday|tomorrow|next week)", text)
    if deadline_match:
        # Simplified date logic for demo
        deadline = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d") 
        
    # 6. Action Suggestions
    action_suggestion = "Create a draft"
    if category == "Event":
        action_suggestion = "Set a date and budget"
    elif category == "Campaign":
        action_suggestion = "Define target audience"
        
    return IdeaAnalysis(
        is_idea=True,
        category=category,
        priority=priority,
        viability_score=viability_score,
        deadline=deadline,
        action_suggestion=action_suggestion
    )

def analyze_file_content(filename: str, content_preview: str) -> IdeaAnalysis:
    text = (filename + " " + content_preview).lower()
    
    category = "General"
    if any(w in text for w in ["report", "doc", "pdf"]):
        category = "Document"
    if any(w in text for w in ["budget", "finance", "cost"]):
        category = "Finance"
    elif any(w in text for w in ["design", "mockup", "ui", "ux"]):
        category = "Design"
        
    priority = "Medium"
    if "final" in text or "urgent" in text:
        priority = "High"
        
    # Extract deadline
    deadline = None
    if "q4" in text:
        deadline = "2025-12-31"
    elif "next week" in text:
        deadline = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        
    # Generate a better suggestion based on content
    action_suggestion = f"Review {filename}"
    if len(content_preview) > 50:
        # Return a larger chunk of the content as the "extracted idea"
        # We'll limit to 2000 chars to keep the UI responsive, but it's much more than before.
        action_suggestion = f"Extracted Content:\n\n{content_preview[:15000]}..." if len(content_preview) > 15000 else f"Extracted Content:\n\n{content_preview}"
            
    return IdeaAnalysis(
        is_idea=True,
        category=category,
        priority=priority,
        viability_score=8, 
        deadline=deadline,
        action_suggestion=action_suggestion
    )
