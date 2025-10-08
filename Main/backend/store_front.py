# backend/store_front.py
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STOCK_FILE = os.path.join(BASE_DIR, 'data', 'stock.json')

def load_games():
    """Load all games from stock.json"""
    if not os.path.exists(STOCK_FILE):
        return []
    with open(STOCK_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def filter_games_for_user(user_age):
    """Return games with flag for restricted based on user age"""
    games = load_games()
    for game in games:
        game['restricted'] = user_age < game.get('age', 0)
    return games
