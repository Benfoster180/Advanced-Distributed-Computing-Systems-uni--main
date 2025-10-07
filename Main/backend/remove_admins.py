import os
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Correct path to admins.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Main/
ADMIN_DB = os.path.join(BASE_DIR, 'data', 'admins.json')

def remove_admins_page(request):
    """Render the Remove Admins page with dropdown of emails."""
    from django.template import engines
    django_engine = engines['django']
    template = django_engine.get_template('remove_admin.html')

    # Load admins for dropdown
    if os.path.exists(ADMIN_DB):
        with open(ADMIN_DB, 'r') as f:
            try:
                admins = json.load(f)
            except json.JSONDecodeError:
                admins = []
    else:
        admins = []

    emails = [admin['email'] for admin in admins]
    return HttpResponse(template.render({'emails': emails}))

@csrf_exempt
def remove_admin(request):
    """Handle removing the selected admin."""
    if request.method == "POST":
        email_to_remove = request.POST.get("email")
        if os.path.exists(ADMIN_DB):
            with open(ADMIN_DB, 'r') as f:
                try:
                    admins = json.load(f)
                except json.JSONDecodeError:
                    admins = []

            # Remove admin with matching email
            admins = [a for a in admins if a['email'] != email_to_remove]

            # Save updated list
            os.makedirs(os.path.dirname(ADMIN_DB), exist_ok=True)
            with open(ADMIN_DB, 'w') as f:
                json.dump(admins, f, indent=4)

        return HttpResponse("<h2>Admin removed successfully!</h2><p><a href='/remove_admins/'>Back</a></p>")

    return HttpResponse("<h2>Invalid request</h2><p><a href='/remove_admins/'>Back</a></p>")
