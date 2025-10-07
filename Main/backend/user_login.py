import os
import json
import base64
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import engines

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_DB = os.path.join(BASE_DIR, 'data', 'user.json')

def decrypt_password(password):
    decoded_bytes = base64.b64decode(password)
    return decoded_bytes.decode('utf-8')

def check_user_credentials(email, password, user_db=USER_DB):
    """Check user login credentials (case-insensitive)."""
    if not os.path.exists(user_db):
        print("User database not found.")
        return False

    with open(user_db, 'r') as file:
        try:
            users = json.load(file)
        except json.JSONDecodeError:
            print("Error reading user database.")
            return False

    email_lower = email.strip().lower()
    for user in users:
        if user['email'].strip().lower() == email_lower:
            if decrypt_password(user['password']) == password:
                print("User login successful!")
                return True
            else:
                print("Incorrect password.")
                return False

    print("User not found.")
    return False

@csrf_exempt
def user_login(request):
    django_engine = engines['django']
    template = django_engine.get_template('User_login.html')

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if check_user_credentials(email, password):
            return HttpResponse("<h2>Welcome, user!</h2><p><a href='/add_user/'>Add another user</a></p>")
        else:
            return HttpResponse(template.render({"error": "Invalid credentials"}))

    return HttpResponse(template.render())
