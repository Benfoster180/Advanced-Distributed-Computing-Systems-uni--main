import os
import json

# Path to stock DB
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Main/
STOCK_DB = os.path.join(BASE_DIR, 'data', 'stock.json')


def add_game(game_name, game_type, age_rating, platform, price_per_day, cover_url, stock):
    """Add a new game to the stock database."""
    os.makedirs(os.path.dirname(STOCK_DB), exist_ok=True)

    # Load existing games
    if os.path.exists(STOCK_DB):
        with open(STOCK_DB, 'r') as f:
            try:
                games = json.load(f)
            except json.JSONDecodeError:
                games = []
    else:
        games = []

    # New game entry
    new_game = {
        "game_name": game_name,
        "type": game_type,
        "age_rating": int(age_rating),
        "platform": platform,
        "price_per_day": int(price_per_day),
        "cover_url": cover_url,
        "stock": int(stock)
    }

    # Add and save
    games.append(new_game)
    with open(STOCK_DB, 'w') as f:
        json.dump(games, f, indent=4)
