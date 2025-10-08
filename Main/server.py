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
from django.shortcuts import render

# --- Import backend functions ---
from backend.user import add_user
from backend.add_admin import add_admin
from backend.remove_users import remove_users_page, remove_user
from backend.remove_admins import remove_admins_page, remove_admin
from backend.view_admins import view_admins_page
from backend.view_users import view_users_page
from backend.add_game import add_game
from backend.remove_stock import remove_stock_page, remove_stock
from backend.store_front import filter_games_for_user
from backend.globals import CURRENT_USER, BASKET

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ADMIN_DB = os.path.join(BASE_DIR, "data", "admins.json")
USER_DB = os.path.join(BASE_DIR, "data", "user.json")

# --- Django Settings ---
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="local-dev-key",
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=["*"],
        MIDDLEWARE=[],
        INSTALLED_APPS=[
            "django.contrib.staticfiles",
        ],
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [os.path.join(BASE_DIR, "frontend")],
                "APP_DIRS": True,
            }
        ],
        STATIC_URL="/static/",
        STATICFILES_DIRS=[os.path.join(BASE_DIR, "frontend/static")],
    )

django.setup()

# --- Helper Functions ---
def decrypt_password(password):
    decoded_bytes = base64.b64decode(password)
    return decoded_bytes.decode("utf-8")


def get_user_by_credentials(email, password, db_file):
    if not os.path.exists(db_file):
        return None

    with open(db_file, "r") as file:
        try:
            entries = json.load(file)
        except json.JSONDecodeError:
            return None

    email_lower = email.strip().lower()
    for entry in entries:
        if entry["email"].strip().lower() == email_lower:
            if decrypt_password(entry["password"]) == password:
                return entry
            else:
                return None
    return None

# --- Views ---
def index(request):
    template = engines["django"].get_template("index.html")
    return HttpResponse(template.render())


@csrf_exempt
def admin_login(request):
    template = engines["django"].get_template("Admin_login.html")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if get_user_by_credentials(email, password, ADMIN_DB):
            return HttpResponseRedirect("/admin_portal/")
        else:
            return HttpResponse(template.render({"error": "Invalid credentials"}))
    return HttpResponse(template.render())


@csrf_exempt
def user_login(request):
    template = engines["django"].get_template("User_login.html")
    global CURRENT_USER
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = get_user_by_credentials(email, password, USER_DB)
        if user:
            CURRENT_USER = {
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "age": user["age"],
                "email": user["email"],
            }
            return HttpResponseRedirect("/store_front/")
        else:
            return HttpResponse(template.render({"error": "Invalid credentials"}))
    return HttpResponse(template.render())


def store_front(request):
    # get games filtered for CURRENT_USER
    user_age = getattr(CURRENT_USER, "age", 0)
    games = filter_games_for_user(user_age)

    # Group games by platform
    platforms = {}
    for game in games:
        platforms.setdefault(game["platform"], []).append(game)

    return render(request, "store_front.html", {
        "user": CURRENT_USER,
        "platforms": platforms
    })


@csrf_exempt
def submit_add_basket(request):
    """Add a game to global basket"""
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        if name and price:
            BASKET.append({"name": name, "price": price})
    return HttpResponseRedirect("/store_front/")


# --- User/Admin/Game Pages ---
def add_user_page(request):
    template = engines["django"].get_template("add_user.html")
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
    template = engines["django"].get_template("add_admin.html")
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
    template = engines["django"].get_template("admin_portal.html")
    return HttpResponse(template.render())


def add_game_page(request):
    template = engines["django"].get_template("add_game.html")
    return HttpResponse(template.render())


@csrf_exempt
def submit_game(request):
    if request.method == "POST":
        game_name = request.POST.get("game_name")
        game_type = request.POST.get("game_type")
        age_rating = request.POST.get("age_rating")
        platform = request.POST.get("platform")
        price_per_day = request.POST.get("price_per_day")
        cover_url = request.POST.get("cover_url")
        stock = request.POST.get("stock")
        add_game(game_name, game_type, age_rating, platform, price_per_day, cover_url, stock)
        return HttpResponse("<h2>Game added successfully!</h2><p><a href='/add_game/'>Add another</a></p>")
    return HttpResponseRedirect("/add_game/")


# --- URL Patterns ---
urlpatterns = [
    path("", index),
    path("admin_login/", admin_login),
    path("admin_portal/", admin_portal),
    path("user_login/", user_login),
    path("store_front/", store_front),
    path("submit_add_basket/", submit_add_basket),
    path("add_user/", add_user_page),
    path("add_admin/", add_admin_page),
    path("submit/", submit),
    path("submit_admin/", submit_admin),
    path("remove_users/", remove_users_page),
    path("remove_user/", remove_user),
    path("remove_admins/", remove_admins_page),
    path("remove_admin/", remove_admin),
    path("view_users/", view_users_page),
    path("view_admins/", view_admins_page),
    path("add_game/", add_game_page),
    path("submit_game/", submit_game),
    path("remove_stock/", remove_stock_page),
    path("submit_remove_stock/", remove_stock),
]

# --- Run Server ---
if __name__ == "__main__":
    execute_from_command_line(["server.py", "runserver", "8000"])
