
import requests
import time

API_URL = "http://localhost:8000"

def test_username_flow():
    # 1. Login/Create User
    print("1. Creating User...")
    phone = f"+1555{int(time.time())}"
    login_payload = {
        "phone": phone,
        "idToken": "mock_token",
        "name": "Test User"
    }
    
    # Mocking login requires backend running in dev mode or mock mode on frontend
    # Since we are testing backend API directly, we can hit /login
    
    try:
        response = requests.post(f"{API_URL}/login", json=login_payload)
        response.raise_for_status()
        user = response.json()
        print(f"User created: ID={user['id']}, Username={user.get('username')}")
        
        user_id = user['id']
        
        if user.get('username'):
            print("User already has username (unexpected for new user)")
            
        # 2. Set Username
        print("\n2. Setting Username...")
        username = f"user_{int(time.time())}"
        set_payload = {
            "user_id": user_id,
            "username": username
        }
        
        response = requests.post(f"{API_URL}/set_username", json=set_payload)
        response.raise_for_status()
        data = response.json()
        print(f"Set Username Response: {data}")
        
        # 3. Verify Persistence
        print("\n3. Verifying Persistence...")
        # Login again to check if username is returned
        response = requests.post(f"{API_URL}/login", json=login_payload)
        user_updated = response.json()
        print(f"User on re-login: Username={user_updated.get('username')}")
        
        assert user_updated.get('username') == username
        print("SUCCESS: Username persisted.")
        
        # 4. specific Duplicate Test
        print("\n4. Testing Duplicate Username...")
        # Create another user
        phone2 = f"+1555{int(time.time())+1}"
        login_payload2 = { "phone": phone2, "idToken": "mock_token", "name": "Test User 2" }
        response = requests.post(f"{API_URL}/login", json=login_payload2)
        user2 = response.json()
        
        # Try to set same username
        set_payload2 = {
            "user_id": user2['id'],
            "username": username # Same as above
        }
        
        response = requests.post(f"{API_URL}/set_username", json=set_payload2)
        if response.status_code == 400:
            print("SUCCESS: Duplicate username rejected.")
        else:
            print(f"FAILURE: Duplicate username accepted or other error. Status: {response.status_code}")
            
    except Exception as e:
        print(f"Test Failed: {e}")

if __name__ == "__main__":
    test_username_flow()
