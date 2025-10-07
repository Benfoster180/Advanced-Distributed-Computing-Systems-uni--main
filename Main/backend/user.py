import json, os, threading, socketserver, time, base64

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
user_db = os.path.join(BASE_DIR, 'data', 'user.json')

def decrypt_password(password):
    decoded_bytes = base64.b64decode(password)
    decrypted_password = decoded_bytes.decode('utf-8')
    return decrypted_password


def add_user(first_name, last_name, age, email, raw_password, path=user_db):

    def encode_password(password):
        password_bytes = password.encode('utf-8')
        encode_bytes = base64.b64encode(password_bytes)
        encryprted_password = encode_bytes.decode('utf-8')
        return encryprted_password

    password = encode_password(raw_password) #Encrypt password


    user = {"first_name": first_name, "last_name": last_name, "age": age ,"email": email, "password": password}


    # Load existing users
    if os.path.exists(user_db):
        with open(user_db, 'r') as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = []
    else:
        users = []

    # Append and save
    users.append(user)
    os.makedirs(os.path.dirname(user_db), exist_ok=True)
    with open(user_db, 'w') as f:
        json.dump(users, f, indent=4)

    print("User added successfully!")



