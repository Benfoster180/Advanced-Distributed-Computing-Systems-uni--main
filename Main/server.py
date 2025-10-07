import os
import django
import base64
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import path
from django.core.management import execute_from_command_line
from django.template import engines
from django.views.decorators.csrf import csrf_exempt
from backend.user import add_user  # your add_user function

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Settings ---
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
        'DIRS': ['frontend'],  # updated path
        'APP_DIRS': True,
    }],
    STATIC_URL='/static/',  # THIS IS REQUIRED
    STATICFILES_DIRS=[os.path.join(BASE_DIR, 'frontend/static')],
)

# --- Views ---
def index(request):
    django_engine = engines['django']
    template = django_engine.get_template('add_user.html')
    return HttpResponse(template.render())

@csrf_exempt
def submit(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")
        email = request.POST.get("email")
        raw_password = request.POST.get("password")

        # Call your backend add_user function
        add_user(first_name, last_name, age, email, raw_password)

        return HttpResponse("<h2>User added successfully!</h2><p><a href='/'>Add another</a></p>")

# --- URLs ---
urlpatterns = [
    path('', index),
    path('submit/', submit),
]

# --- Run server ---
if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '__main__')
    django.setup()
    execute_from_command_line(['server.py', 'runserver', '8000'])
