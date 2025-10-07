import os
import json
import base64
import django
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path
from django.core.management import execute_from_command_line
from django.template import engines
from django.views.decorators.csrf import csrf_exempt
from backend.view_users import view_users_page

# Backend functions
from backend.user import add_user
from backend.add_admin import add_admin
from backend.remove_users import remove_users_page, remove_user
from backend.remove_admins import remove_admins_page, remove_admin
from backend.view_admins import view_admins_page

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Points to Main/
ADMIN_DB = os.path.join(BASE_DIR, 'data', 'admins.json')
USER_DB = os.path.join(BASE_DIR, 'data', 'user.json')

# --- Django Settings ---
settings.configure(
    DEBUG=True,
    SECRET_KEY='local-dev-key',
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=['*'],
    MIDDLEWARE=[],
    INSTALLED_APPS=[
        'django.contrib.staticfiles',
    ],
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'frontend')],
        'APP_DIRS': True,
    }],
    STATIC_URL='/static/',
    STATICFILES_DIRS=[os.path.join(BASE_DIR, 'frontend/static')],
)

# --- Helper Functions ---
def decrypt_password(password):
    decoded_bytes = base64.b64decode(password)
    return decoded_bytes.decode('utf-8')

def check_credentials(email, password, db_file):
    if not os.path.exists(db_file):
        print(f"Database not found: {db_file}")
        return False

    with open(db_file, 'r') as file:
        try:
            entries = json.load(file)
        except json.JSONDecodeError:
            print(f"Error reading database: {db_file}")
            return False

    email_lower = email.strip().lower()
    for entry in entries:
        if entry['email'].strip().lower() == email_lower:
            if decrypt_password(entry['password']) == password:
                return True
            else:
                return False
    return False

# --- Views ---
def index(request):
    template = engines['django'].get_template('index.html')
    return HttpResponse(template.render())

@csrf_exempt
def admin_login(request):
    template = engines['django'].get_template('Admin_login.html')
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if check_credentials(email, password, ADMIN_DB):
            return HttpResponseRedirect("/admin_portal/")
        else:
            return HttpResponse(template.render({"error": "Invalid credentials"}))
    return HttpResponse(template.render())

@csrf_exempt
def user_login(request):
    template = engines['django'].get_template('User_login.html')
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if check_credentials(email, password, USER_DB):
            return HttpResponseRedirect("/store_front/")
        else:
            return HttpResponse(template.render({"error": "Invalid credentials"}))
    return HttpResponse(template.render())

def store_front(request):
    template = engines['django'].get_template('store_front.html')
    return HttpResponse(template.render())

def add_user_page(request):
    template = engines['django'].get_template('add_user.html')
    return HttpResponse(template.render())

@csrf_exempt
def submit(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")
        email = request.POST.get("email")
        raw_password = request.POST.get("password")
        add_user(first_name, last_name, age, email, raw_password)
        return HttpResponse("<h2>User added successfully!</h2><p><a href='/add_user/'>Add another</a></p>")
    return HttpResponseRedirect("/add_user/")

def add_admin_page(request):
    template = engines['django'].get_template('add_admin.html')
    return HttpResponse(template.render())

@csrf_exempt
def submit_admin(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")
        email = request.POST.get("email")
        raw_password = request.POST.get("password")
        add_admin(first_name, last_name, age, email, raw_password)
        return HttpResponseRedirect("/admin_portal/")
    return HttpResponseRedirect("/add_admin/")

def admin_portal(request):
    template = engines['django'].get_template('admin_portal.html')
    return HttpResponse(template.render())

# --- URL Patterns ---
urlpatterns = [
    path('', index),
    path('admin_login/', admin_login),
    path('admin_portal/', admin_portal),
    path('user_login/', user_login),
    path('store_front/', store_front),
    path('add_user/', add_user_page),
    path('add_admin/', add_admin_page),
    path('submit/', submit),
    path('submit_admin/', submit_admin),
    path('remove_users/', remove_users_page),
    path('remove_user/', remove_user),
    path('remove_admins/', remove_admins_page),
    path('remove_admin/', remove_admin),
    path('view_users/', view_users_page),
    path('view_admins/', view_admins_page),

]

# --- Run Server ---
if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '__main__')
    django.setup()
    execute_from_command_line(['server.py', 'runserver', '8000'])
