import json
import os
import base64

# --- Absolute path to Main/data/admins.json ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one level from backend/
ADMIN_DB = os.path.join(BASE_DIR, 'data', 'admins.json')

def decrypt_password(password):
    """Decode a base64-encoded password."""
    decoded_bytes = base64.b64decode(password)
    return decoded_bytes.decode('utf-8')

def add_admin(first_name, last_name, age, email, raw_password, path=ADMIN_DB):
    """Add a new admin to the admins.json file."""

    def encode_password(password):
        """Encode the password using base64."""
        return base64.b64encode(password.encode('utf-8')).decode('utf-8')

    password = encode_password(raw_password)

    admin = {
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "email": email,
        "password": password
    }

    # Load existing admins
    if os.path.exists(path):
        with open(path, 'r') as f:
            try:
                admins = json.load(f)
            except json.JSONDecodeError:
                admins = []
    else:
        admins = []

    # Append new admin
    admins.append(admin)

    # Ensure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Save back to JSON
    with open(path, 'w') as f:
        json.dump(admins, f, indent=4)

    print("Admin added successfully!")
