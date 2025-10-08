import os
import json
from django.http import HttpResponse

# Path to user DB
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Main/
USER_DB = os.path.join(BASE_DIR, 'data', 'user.json')


def view_users_page(request):
    """Render a scrollable table of all users."""
    from django.template import engines
    django_engine = engines['django']
    template = django_engine.get_template('view_users.html')

    # Load users
    users = []
    if os.path.exists(USER_DB):
        with open(USER_DB, 'r') as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = []

    context = {'users': users}
    return HttpResponse(template.render(context))
