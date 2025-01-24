from typing import Dict, Optional
import json
import os

# In a production environment, this should be replaced with a proper database
USERS_FILE = "data/users.json"

def load_users() -> Dict:
    """
    Load users from the JSON file
    """
    if not os.path.exists(USERS_FILE):
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        return {}
    
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users: Dict) -> None:
    """
    Save users to the JSON file
    """
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def create_user(wallet_address: str) -> Dict:
    """
    Create a new user
    """
    users = load_users()
    
    if wallet_address in users:
        return users[wallet_address]
    
    user = {
        "wallet_address": wallet_address,
        "created_at": str(datetime.datetime.now()),
        "models": [],
        "datasets": []
    }
    
    users[wallet_address] = user
    save_users(users)
    
    return user

def get_user(wallet_address: str) -> Optional[Dict]:
    """
    Get user by wallet address
    """
    users = load_users()
    return users.get(wallet_address)

def update_user(wallet_address: str, updates: Dict) -> Optional[Dict]:
    """
    Update user information
    """
    users = load_users()
    
    if wallet_address not in users:
        return None
    
    users[wallet_address].update(updates)
    save_users(users)
    
    return users[wallet_address]
