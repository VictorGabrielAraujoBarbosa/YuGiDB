import json
import os
from .card import Card

class CardDatabase:
    def __init__(self, path="database/pt"):
        self.cards = {}
        self.load_from_folder(path)

    def load_from_folder(self, folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                full_path = os.path.join(folder_path, filename)

                with open(full_path, encoding="utf-8") as f:
                    data = json.load(f)

                    # Se o arquivo contém 1 carta
                    if isinstance(data, dict):
                        card = Card(data)
                        self.cards[card.id] = card

                    # Se contém várias cartas
                    elif isinstance(data, list):
                        for entry in data:
                            card = Card(entry)
                            self.cards[card.id] = card

    def get(self, card_id):
        return self.cards.get(card_id)

    def search(self, text):
        text = text.lower()
        return [
            card for card in self.cards.values()
            if text in card.name.lower()
        ]
