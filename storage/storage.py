import json
import os
from models.deck import Deck

DEFAULT_FOLDER = "data/decks"

def save_deck(deck, folder=DEFAULT_FOLDER):
    """Salva o deck em data/decks/<nome>.json"""
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{deck.name}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(deck.to_dict(), f, indent=2, ensure_ascii=False)


def load_deck(name, db, folder=DEFAULT_FOLDER):
    """Carrega um deck salvo de data/decks/<nome>.json"""
    path = os.path.join(folder, f"{name}.json")

    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    deck = Deck(raw["name"])
    for cid in raw["cards"]:
        card = db.get(cid)
        if card:
            deck.add_card(card)

    return deck

