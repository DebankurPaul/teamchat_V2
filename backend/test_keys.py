import requests
import json
import uuid

BASE_URL = "http://localhost:8000"

def test_keys():
    # 1. Upload Keys
    user_id = 99999 # Test ID
    pub_key_mock = {"kty": "EC", "crv": "P-256", "x": "mock-x", "y": "mock-y"}
    
    print("Testing /keys POST...")
    response = requests.post(f"{BASE_URL}/keys", json={
        "user_id": user_id,
        "public_key": json.dumps(pub_key_mock),
        "pre_key_bundle": None
    })
    
    if response.status_code == 200:
        print("Upload Success:", response.json())
    else:
        print("Upload Failed:", response.text)
        return

    # 2. Get Keys
    print(f"Testing /keys/{user_id} GET...")
    response = requests.get(f"{BASE_URL}/keys/{user_id}")
    
    if response.status_code == 200:
        data = response.json()
        print("Fetch Success:", data)
        # Verify
        if data["public_key"] == json.dumps(pub_key_mock):
            print("Verification PASSED: stored key matches uploaded key.")
        else:
            print("Verification FAILED: Keys mismatch.")
    else:
        print("Fetch Failed:", response.text)

if __name__ == "__main__":
    test_keys()
