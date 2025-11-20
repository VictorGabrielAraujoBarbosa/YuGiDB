class Deck:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card_id):
        self.cards = [c for c in self.cards if c != card_id]

    def to_dict(self):
        return {
            "name": self.name,
            "cards": [c for c in self.cards]
        }

    def __repr__(self):
        return f"<Deck {self.name} ({len(self.cards)} cartas)>"
