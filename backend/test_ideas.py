import requests
import json

BASE_URL = "http://localhost:8000"

def test_ideas():
    # 1. Test Analyze Message (Create Idea)
    print("Testing /analyze-message...")
    msg_payload = {
        "text": "We should use Rust for the performance critical modules.",
        "sender": "TestUser",
        "is_idea": True # This field helps backend validation if model requires it
    }
    # Note: IdeaAnalysis model in models.py: is_idea: bool, text missing? 
    # Wait, let's check models.py again. I recall seeing IdeaAnalysis.
    
    # Let's try sending and see.
    try:
        response = requests.post(f"{BASE_URL}/analyze-message", json=msg_payload)
        if response.status_code == 200:
            print("Analyze Success:", response.json())
        else:
            print("Analyze Failed:", response.text)
    except Exception as e:
        print(f"Request Error: {e}")

    # 2. Test Get Ideas
    print("Testing /ideas GET...")
    response = requests.get(f"{BASE_URL}/ideas")
    if response.status_code == 200:
        ideas = response.json()
        print(f"Fetched {len(ideas)} ideas.")
        if len(ideas) > 0:
            print("Sample Idea:", ideas[0])
            # 3. Test Delete
            idea_id = ideas[0]['id']
            print(f"Testing Delete Idea {idea_id}...")
            del_res = requests.delete(f"{BASE_URL}/ideas/{idea_id}")
            print("Delete Status:", del_res.json())
    else:
        print("Fetch Failed:", response.text)

if __name__ == "__main__":
    test_ideas()
