import requests
import json

BASE_URL = "http://localhost:8000"

def test_profile_settings():
    # 1. Register/Login a test user
    print("Creating test user...")
    user_payload = {"email": "test_settings@example.com", "password": "password123", "name": "Test User"}
    # Try login first
    id = None
    try:
        resp = requests.post(f"{BASE_URL}/login", json=user_payload)
        if resp.status_code == 200:
            id = resp.json()["id"]
        else:
            # Register
            resp = requests.post(f"{BASE_URL}/register", json=user_payload)
            if resp.status_code == 200:
                id = resp.json()["id"]
            else:
                print(f"Failed to auth: {resp.text}")
                return
    except Exception as e:
        print(f"Connection error: {e}")
        return

    print(f"User ID: {id}")

    # 2. Test Update Profile
    print("Testing Update Profile (PUT /users/{id})...")
    new_name = "Updated Test User"
    resp = requests.put(f"{BASE_URL}/users/{id}", json={"name": new_name})
    if resp.status_code == 200:
        print("Profile update success")
    else:
        print(f"Profile update failed: {resp.status_code} {resp.text}")

    # 3. Test Update Settings
    print("Testing Update Settings (POST /users/{id}/settings)...")
    settings = {"readReceipts": False, "lastSeen": False}
    resp = requests.post(f"{BASE_URL}/users/{id}/settings", json=settings)
    if resp.status_code == 200:
        print("Settings update success")
        print(resp.json())
    else:
        print(f"Settings update failed: {resp.status_code} {resp.text}")

    # 4. Verify Fetch Settings
    print("Testing Get Settings (GET /users/{id}/settings)...")
    resp = requests.get(f"{BASE_URL}/users/{id}/settings")
    if resp.status_code == 200:
        fetched = resp.json()
        print(f"Fetched Settings: {fetched}")
        if fetched.get("readReceipts") == False:
            print("PASS: Settings persisted")
        else:
            print("FAIL: Settings mismatch")
    else:
        print(f"Get Settings failed: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    test_profile_settings()
