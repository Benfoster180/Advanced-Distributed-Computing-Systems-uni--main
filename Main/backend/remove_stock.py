import os
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# --- Path to stock DB ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STOCK_DB = os.path.join(BASE_DIR, 'data', 'stock.json')


def remove_stock_page(request):
    """Render the Remove Stock page with dropdown of game names."""
    from django.template import engines
    django_engine = engines['django']
    template = django_engine.get_template('remove_stock.html')

    # Load games from JSON
    if os.path.exists(STOCK_DB):
        with open(STOCK_DB, 'r') as f:
            try:
                games = json.load(f)
            except json.JSONDecodeError:
                games = []
    else:
        games = []

    # ✅ Extract only needed fields
    simplified_games = [
        {"game_name": game.get("game_name", "Unknown"), "stock": game.get("stock", 0)}
        for game in games
    ]

    return HttpResponse(template.render({'games': simplified_games}))


@csrf_exempt
def remove_stock(request):
    """Handle removing the selected game from stock."""
    if request.method == "POST":
        game_name = request.POST.get("game_name")
        quantity_to_remove = int(request.POST.get("quantity", 0))

        if not game_name or quantity_to_remove <= 0:
            return HttpResponse("<h2>Invalid input!</h2><p><a href='/remove_stock/'>Back</a></p>")

        if os.path.exists(STOCK_DB):
            with open(STOCK_DB, 'r') as f:
                try:
                    games = json.load(f)
                except json.JSONDecodeError:
                    games = []
        else:
            games = []

        updated_games = []
        message = ""

        for game in games:
            if game['game_name'] == game_name:
                current_stock = int(game['stock'])

                # Remove all or more than available
                if quantity_to_remove >= current_stock:
                    message = f"<h2>Removed all {current_stock} copies of '{game_name}'.</h2>"
                    # Do NOT append (remove from DB)
                else:
                    game['stock'] = current_stock - quantity_to_remove
                    updated_games.append(game)
                    message = (
                        f"<h2>Removed {quantity_to_remove} from '{game_name}'. "
                        f"Remaining: {game['stock']}.</h2>"
                    )
            else:
                updated_games.append(game)

        # Save updates
        os.makedirs(os.path.dirname(STOCK_DB), exist_ok=True)
        with open(STOCK_DB, 'w') as f:
            json.dump(updated_games, f, indent=4)

        return HttpResponse(f"{message}<p><a href='/remove_stock/'>Back</a></p>")

    return HttpResponse("<h2>Invalid request</h2><p><a href='/remove_stock/'>Back</a></p>")
