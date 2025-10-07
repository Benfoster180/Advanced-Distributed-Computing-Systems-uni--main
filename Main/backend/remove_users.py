import os
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# --- Path to user DB ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Main/
USER_DB = os.path.join(BASE_DIR, 'data', 'user.json')


def remove_users_page(request):
    """Render the Remove Users page with a dropdown of emails."""
    from django.template import engines  # Import after settings configured
    django_engine = engines['django']
    template = django_engine.get_template('remove_users.html')

    # Load users from JSON
    if os.path.exists(USER_DB):
        with open(USER_DB, 'r') as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = []
    else:
        users = []

    # Extract emails for dropdown
    emails = [user['email'] for user in users]

    return HttpResponse(template.render({'emails': emails}))


@csrf_exempt
def remove_user(request):
    """Handle removing the selected user from the DB."""
    if request.method == "POST":
        email_to_remove = request.POST.get("email")
        if not email_to_remove:
            return HttpResponse("<h2>No user selected!</h2><p><a href='/remove_users/'>Back</a></p>")

        if os.path.exists(USER_DB):
            with open(USER_DB, 'r') as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    users = []

            # Remove selected user
            users = [u for u in users if u['email'] != email_to_remove]

            # Save updated list
            os.makedirs(os.path.dirname(USER_DB), exist_ok=True)
            with open(USER_DB, 'w') as f:
                json.dump(users, f, indent=4)

        return HttpResponse("<h2>User removed successfully!</h2><p><a href='/remove_users/'>Back</a></p>")

    return HttpResponse("<h2>Invalid request</h2><p><a href='/remove_users/'>Back</a></p>")
