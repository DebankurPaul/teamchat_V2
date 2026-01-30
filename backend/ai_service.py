import os
import requests
import json
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load .env from the backend directory
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def analyze_content(content: str):
    if not GROQ_API_KEY:
        print("Warning: GROQ_API_KEY not found. Using dummy analysis.")
        return False, 0.0, "", ""

    if not content or len(content.strip()) < 10:
        return False, 0.0, "", ""

    system_prompt = """
    You are an expert Idea Extractor. Your job is to analyze the user's input (which could be a message or file content) and determine if it contains a Startup Idea, Business Concept, or Project Idea.
    
    Output JSON ONLY:
    {
        "is_idea": boolean,
        "confidence": float (0.0 to 1.0),
        "summary": "Short 1-sentence summary of the idea",
        "category": "Technology" | "Health" | "Finance" | "Education" | "Lifestyle" | "Other"
    }
    """

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content[:15000]} 
        ],
        "temperature": 0.1,
        "response_format": {"type": "json_object"}
    }

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            print(f"Groq API Error ({response.status_code}): {response.text}")
            return False, 0.0, "", ""
            
        result = response.json()
        content_str = result['choices'][0]['message']['content']
        data = json.loads(content_str)
        
        return data.get("is_idea", False), data.get("confidence", 0.0), data.get("summary", ""), data.get("category", "General")

    except Exception as e:
        print(f"Groq Analysis Error: {e}")
        return False, 0.0, "", ""
