import os
import json
import base64
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import engines
from backend import globals as g  # ✅ clean import for shared globals

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_DB = os.path.join(BASE_DIR, "data", "user.json")


# --- Utility ---
def decrypt_password(password):
    """Decode a base64 password."""
    decoded_bytes = base64.b64decode(password)
    return decoded_bytes.decode("utf-8")


def get_user_by_credentials(email, password, user_db=USER_DB):
    """Return the user dict if credentials are correct, else None."""
    if not os.path.exists(user_db):
        print("❌ User database not found.")
        return None

    with open(user_db, "r") as file:
        try:
            users = json.load(file)
        except json.JSONDecodeError:
            print("❌ Error reading user database.")
            return None

    email_lower = email.strip().lower()
    for user in users:
        if user["email"].strip().lower() == email_lower:
            if decrypt_password(user["password"]) == password:
                print("✅ User login successful!")
                return user
            else:
                print("❌ Incorrect password.")
                return None

    print("❌ User not found.")
    return None


# --- View ---
@csrf_exempt
def user_login(request):
    """Handle user login and store info globally."""
    django_engine = engines["django"]
    template = django_engine.get_template("User_login.html")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = get_user_by_credentials(email, password)
        if user:
            # ✅ Store user info globally (overwrite previous)
            g.CURRENT_USER = {
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "age": user["age"],
                "email": user["email"],
            }

            print("🟢 Logged in user stored globally:", g.CURRENT_USER)
            return HttpResponseRedirect("/store_front/")
        else:
            return HttpResponse(template.render({"error": "Invalid credentials"}))

    return HttpResponse(template.render())
