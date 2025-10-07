import os
import json
from django.http import HttpResponse

# --- Path to admins DB ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Main/
ADMIN_DB = os.path.join(BASE_DIR, 'data', 'admins.json')


def view_admins_page(request):
    """Render a table listing all admins."""
    from django.template import engines
    django_engine = engines['django']
    template = django_engine.get_template('view_admins.html')

    # Load admins from JSON
    if os.path.exists(ADMIN_DB):
        with open(ADMIN_DB, 'r') as f:
            try:
                admins = json.load(f)
            except json.JSONDecodeError:
                admins = []
    else:
        admins = []

    return HttpResponse(template.render({'admins': admins}))
